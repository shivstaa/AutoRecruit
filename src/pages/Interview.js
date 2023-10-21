import React, { useRef, useState, useEffect } from 'react';


const Interview = () => {
    const [recording, setRecording] = useState(false);
    const [videoURLs, setVideoURLs] = useState([]);
    const videoRef = useRef(null);
    let mediaRecorder = useRef(null);
    let chunks = useRef([]);

    const handleData = () => {
        if (chunks.current.length) {
            let blob = new Blob(chunks.current, { type: "video/webm" });
            let url = URL.createObjectURL(blob);
            setVideoURLs(prevURLs => [...prevURLs, url]);
            chunks.current = [];
        }
    };

    const startCapture = async () => {
        if (mediaRecorder.current) return;
    
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
    
            videoRef.current.srcObject = stream;
    
            if (MediaRecorder.isTypeSupported('video/webm')) {
                mediaRecorder.current = new MediaRecorder(stream, { mimeType: "video/webm" });
            } else {
                console.error("MIME type not supported");
                return;
            }
    
            mediaRecorder.current.ondataavailable = (e) => {
                chunks.current.push(e.data);
                handleData(); // Immediately handle the data
            };
    
            mediaRecorder.current.start(10000); // Collect data every 10 seconds
            setRecording(true);
    
        } catch (error) {
            console.error("Error starting capture:", error);
        }
    };
    

    const stopCapture = () => {
        if (mediaRecorder.current && mediaRecorder.current.state !== "inactive") {
            mediaRecorder.current.stop();
            handleData();
            videoRef.current.srcObject.getTracks().forEach(track => track.stop());
            setRecording(false);
        }
    };

    useEffect(() => {
        return () => {
            if (videoRef.current && videoRef.current.srcObject) {
                videoRef.current.srcObject.getTracks().forEach(track => track.stop());
            }
        };
    }, []);

    return (
        <div className="flex flex-col items-center mt-4">
            <video ref={videoRef} autoPlay muted className="border p-4"></video>            <div className="mt-4">
                {!recording ? (
                    <button
                        className="bg-blue-500 text-white px-6 py-2 rounded"
                        onClick={startCapture}
                    >
                        Start
                    </button>
                ) : (
                    <button
                        className="bg-red-500 text-white px-6 py-2 rounded"
                        onClick={stopCapture}
                    >
                        Stop
                    </button>
                )}
            </div>
            <div className="mt-4">
                {videoURLs.map((url, index) => (
                    <div key={index} className="mt-4">
                        <video controls src={url} className="border p-4"></video>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Interview;