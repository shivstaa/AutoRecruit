import React, { useRef, useState, useEffect } from "react";

const Interview = () => {
  const videoRef = useRef(null);
  let mediaStream = null;
  let webSocket = null;

  const [transcript, setTranscript] = useState("");
  const [question, setQuestion] = useState("");
  const [sessionID, setSessionID] = useState(null); // New state to hold session ID

  const getSessionID = () => {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("session_id");
  };

  useEffect(() => {
    // Set session ID on component mount
    setSessionID(getSessionID());
  }, []);

  const handleKeypress = (event) => {
    if (
      event.keyCode === 32 &&
      webSocket &&
      webSocket.readyState === WebSocket.OPEN
    ) {
      // Spacebar keycode
      webSocket.send(
        JSON.stringify({
          action: "save_transcript",
          transcript,
          session_id: sessionID,
        })
      );
      setTranscript(""); // Reset transcript for the next chunk of conversation
    }
  };

  const handleTranscriptMessage = (message) => {
    try {
      // Attempt to parse the message data as JSON
      const data = JSON.parse(message.data);
      if (data.action === "new_question") {
        console.log(data.question.question);
        setQuestion(data.question.question);
      } else if (data.action === "new_transcript") {
        // Assume the message contains transcript text if the action is 'new_transcript'
        setTranscript(
          (prevTranscript) => prevTranscript + " " + data.transcript
        );
      }
    } catch (error) {
      // If parsing as JSON fails, treat the message data as plain text
      const received = message.data;
      setTranscript((prevTranscript) => prevTranscript + " " + received);
    }
  };

  useEffect(() => {
    document.addEventListener("keypress", handleKeypress);
    return () => {
      document.removeEventListener("keypress", handleKeypress);
    };
  }, [transcript, sessionID]); // Include sessionID as a dependency

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
        mediaRecorder.start(5000); // Sending data in 5s chunks
      };
      webSocket.onmessage = handleTranscriptMessage;
    } catch (error) {
      console.error("Error accessing media devices.", error);
    }
  };

  const stopStreaming = () => {
    const confirmation = window.confirm(
      "Are you sure you want to stop the interview?"
    );
    if (confirmation) {
      if (mediaStream) {
        let tracks = mediaStream.getTracks();
        tracks.forEach((track) => track.stop());
      }
      if (webSocket) {
        webSocket.close();
      }
    }
    initiateAnalysis();
  };
  
  const initiateAnalysis = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/session/${sessionID}/analysis/initiate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any other headers required by your Django backend here
        },
        // Include credentials if your API requires authentication
        credentials: 'include',
      });
  
      if (response.ok) {
        const data = await response.json();
        if (data.status === 'Analysis started') {
          // Redirect to the analysis status page
          window.location.href = data.analysis_url;
        }
      } else {
        console.error("Failed to initiate analysis", response.statusText);
      }
    } catch (error) {
      console.error("Failed to initiate analysis", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <video ref={videoRef} className="mb-4" autoPlay muted></video>
      <div>
        <button
          onClick={startStreaming}
          className="mr-4 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Start Streaming
        </button>
        <button
          onClick={stopStreaming}
          className="px-4 py-2 bg-red-500 text-white rounded"
        >
          Stop Streaming
        </button>
      </div>
      <div id="transcript">{transcript}</div>
      <div id="question">{question}</div>
    </div>
  );
};

export default Interview;
