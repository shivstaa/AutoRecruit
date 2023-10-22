import os
from dotenv import load_dotenv

import openai
from elevenlabs import set_api_key

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
set_api_key(os.getenv('ELEVENLABS_API_KEY'))