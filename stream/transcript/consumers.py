import json
from channels.generic.websocket import AsyncWebsocketConsumer
from dotenv import load_dotenv
from deepgram import Deepgram
from typing import Dict
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from core.models import Session, Conversation
import os

load_dotenv()


class TranscriptConsumer(AsyncWebsocketConsumer):
    dg_client = Deepgram(os.getenv('DEEPGRAM_API_KEY'))
    channel_layer = get_channel_layer()

    @database_sync_to_async
    def save_conversation(self, session_id, speaker, text):
        session = Session.objects.get(pk=session_id)
        Conversation.objects.create(
            session=session, speaker=speaker, text=text)

    async def get_transcript(self, data: Dict) -> None:
        if 'channel' in data:
            transcript = data['channel']['alternatives'][0]['transcript']

            if transcript:
                await self.save_conversation(self.session_id, 'user', transcript)
                await self.send(transcript)

    async def connect_to_deepgram(self):
        try:
            self.socket = await self.dg_client.transcription.live({'punctuate': True, 'interim_results': False})
            self.socket.registerHandler(self.socket.event.CLOSE, lambda c: print(
                f'Connection closed with code {c}.'))
            self.socket.registerHandler(
                self.socket.event.TRANSCRIPT_RECEIVED, self.get_transcript)

        except Exception as e:
            raise Exception(f'Could not open socket: {e}')


    async def connect(self):
        # This could be a constant, or it could be based on some aspect of the WebSocket
        # For example, it could include the user id, or some other identifier.
        self.room_group_name = 'transcript_group'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.connect_to_deepgram()
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, bytes_data):
        # Assuming 'save_transcript' action will be sent as text data
        try:
            text_data = bytes_data.decode('utf-8')
            data = json.loads(text_data)
            if data.get('action') == 'save_transcript':
                transcript = data.get('transcript')
                if transcript:
                    await self.save_conversation(self.session_id, 'user', transcript)
        except:
            # Assuming anything that isn't text data is binary audio data
            self.socket.send(bytes_data)

    async def send_question(self, question_text):
        await self.send(json.dumps({
            'action': 'new_question',
            'question': question_text,
        }))


    async def send_question_event(self, event):
        question_text = event['question']
        await self.send_question(question_text)