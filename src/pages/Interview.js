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
  const mediaStreamRef = useRef(null);
  const webSocketRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  
  const [transcript, setTranscript] = useState('');
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
    if (webSocketRef.current && webSocketRef.current.readyState === WebSocket.OPEN) {
      webSocketRef.current.send(JSON.stringify({ action: 'next_question', transcript, session_id: sessionID }));
      openModal();
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
        setModalQuestion(data.question.question);
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
      mediaStreamRef.current = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = mediaStreamRef.current;
      }

      webSocketRef.current = new WebSocket(`ws://localhost:8000/listen/${sessionID}/`);
      webSocketRef.current.onopen = () => {
        console.log("WebSocket connection opened");
        mediaRecorderRef.current = new MediaRecorder(mediaStreamRef.current);
        mediaRecorderRef.current.ondataavailable = (event) => {
          if (webSocketRef.current && webSocketRef.current.readyState === WebSocket.OPEN) {
            webSocketRef.current.send(event.data);
          }
        };
        mediaRecorderRef.current.start(150);
      };
      webSocketRef.current.onmessage = handleTranscriptMessage;
    } catch (error) {
      console.error("Error accessing media devices.", error);
    }
  };

  const stopStreaming = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
    if (mediaStreamRef.current) {
      let tracks = mediaStreamRef.current.getTracks();
      tracks.forEach((track) => track.stop());
    }
    if (webSocketRef.current) {
      webSocketRef.current.close();
    }
    handleNextQuestion();
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
    </div>
  );
};

export default Interview;
