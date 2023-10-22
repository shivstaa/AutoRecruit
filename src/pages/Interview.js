import React, { useRef, useState, useEffect } from 'react';

const modalOverlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  backgroundColor: 'rgba(0, 0, 0, 0.5)',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  zIndex: 1000,
};

const modalContentStyle = {
  backgroundColor: '#ffffff',
  padding: '20px',
  borderRadius: '4px',
  width: '80%',
  maxWidth: '500px',
};

function QuestionModal({ question, onClose }) {
  if (!question) {
    return null;
  }

  return (
    <div style={modalOverlayStyle}>
      <div style={modalContentStyle}>
        <p>{question}</p>
        <button onClick={onClose}>I am ready, Answer this question</button>
      </div>
    </div>
  );
}
const Interview = () => {
  const videoRef = useRef(null);
  let mediaStream = null;
  let webSocket = null;

  const [transcript, setTranscript] = useState('');
  const [question, setQuestion] = useState('');
  const [sessionID, setSessionID] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalQuestion, setModalQuestion] = useState('');

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setTranscript('');
  };

  const handleNextQuestion = () => {
    if (webSocket && webSocket.readyState === WebSocket.OPEN) {
      webSocket.send(JSON.stringify({ action: 'next_question', transcript, session_id: sessionID }));
      openModal();  // Open the modal when requesting the next question
    }
  };
  const getSessionID = () => {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('session_id');
  };

  useEffect(() => {
    setSessionID(getSessionID());
  }, []);

  const handleTranscriptMessage = (message) => {
    try {
      const data = JSON.parse(message.data);
      if (data.action === 'new_question') {
        setModalQuestion(data.question.question);  // Update the modal question when a new question is received
      } else {
        setTranscript(prevTranscript => prevTranscript + ' ' + data.transcript);
      }
    } catch (error) {
      const received = message.data;
      setTranscript(prevTranscript => prevTranscript + ' ' + received);
    }
  };

  const startStreaming = async () => {
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      });
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }

      // Initialize WebSocket connection
      webSocket = new WebSocket(`ws://localhost:8000/listen/${sessionID}/`);
      // Include session ID in the WebSocket URL or as a message after connecting
      webSocket.onopen = () => {
        // Handle WebSocket open event
        console.log("WebSocket connection opened");
        // Optionally send session ID over WebSocket after connecting
        // webSocket.send(JSON.stringify({ action: 'start_session', session_id: sessionID }));

        // Send data over WebSocket
        const mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.ondataavailable = (event) => {
          if (webSocket && webSocket.readyState === WebSocket.OPEN) {
            webSocket.send(event.data);
          }
        };
        mediaRecorder.start(150); // Sending data in 100ms chunks
      };
      webSocket.onmessage = handleTranscriptMessage;
    } catch (error) {
      console.error("Error accessing media devices.", error);
    }
  };

  const stopStreaming = () => {
    if (mediaStream) {
      let tracks = mediaStream.getTracks();
      tracks.forEach((track) => track.stop());
    }
    if (webSocket) {
      webSocket.close();
    }
    handleNextQuestion();  // Trigger next question when stopping streaming
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <video ref={videoRef} className="mb-4" autoPlay muted></video>
      <div>
        <button onClick={startStreaming} className="mr-4 px-4 py-2 bg-blue-500 text-white rounded">Start Streaming</button>
        <button onClick={stopStreaming} className="px-4 py-2 bg-red-500 text-white rounded">Stop Streaming</button>
        <button onClick={handleNextQuestion} className="px-4 py-2 bg-green-500 text-white rounded">Next Question</button>
        {isModalOpen && <QuestionModal question={modalQuestion} onClose={closeModal} />}
      </div>
      <div id="transcript">{transcript}</div>
      <div id="question">{question}</div>
    </div>
  );
};

export default Interview;