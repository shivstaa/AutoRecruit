import React, { useRef, useState, useEffect } from 'react';

const Interview = () => {
  const videoRef = useRef(null);
  let mediaStream = null;
  let webSocket = null;

  const [transcript, setTranscript] = useState('');
  const [question, setQuestion] = useState('');

  const handleKeypress = (event) => {
    if (event.keyCode === 32 && webSocket && webSocket.readyState === WebSocket.OPEN) {  // Spacebar keycode
      webSocket.send(JSON.stringify({ action: 'save_transcript', transcript }));
    }
  };
  const handleTranscriptMessage = (message) => {
    const data = JSON.parse(message.data);
    if (data.action === 'new_question') {
        setQuestion(data.question);
    } else {
        // Assume the message contains transcript text if no action is specified
        const received = message.data;
        setTranscript(prevTranscript => prevTranscript + ' ' + received);
    }
};


  useEffect(() => {
    document.addEventListener('keypress', handleKeypress);
    return () => {
      document.removeEventListener('keypress', handleKeypress);
    };
  }, [transcript]);

  const startStreaming = async () => {
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      
      // Initialize WebSocket connection
      webSocket = new WebSocket('ws://localhost:8000/listen')
      // webSocket = new WebSocket('ws://your_django_server_url/ws/some_path/');
      webSocket.onopen = () => {
        // Handle WebSocket open event
        console.log("WebSocket connection opened");
        
        // Send data over WebSocket
        const mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.ondataavailable = event => {
          if (webSocket && webSocket.readyState === WebSocket.OPEN) {
            webSocket.send(event.data);
          }
        };
        mediaRecorder.start(100); // Sending data in 100ms chunks
      };
      webSocket.onmessage = handleTranscriptMessage;
    } catch (error) {
      console.error('Error accessing media devices.', error);
    }
  };

  const stopStreaming = () => {
    if (mediaStream) {
      let tracks = mediaStream.getTracks();
      tracks.forEach(track => track.stop());
    }
    if (webSocket) {
      webSocket.close();
    }
  };


  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <video ref={videoRef} className="mb-4" autoPlay muted></video>
      <div>
        <button onClick={startStreaming} className="mr-4 px-4 py-2 bg-blue-500 text-white rounded">Start Streaming</button>
        <button onClick={stopStreaming} className="px-4 py-2 bg-red-500 text-white rounded">Stop Streaming</button>
      </div>
      <div id="transcript">{transcript}</div>
      <div id="question">{question}</div>
    </div>
  );
};

export default Interview;
