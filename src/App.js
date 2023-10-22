import "./App.css";
import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import Interview from "./pages/Interview";
import { AuthProvider } from "./components/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import useTypeWriter from "react-typewriter-hook";

function StartInterviewButton() {
  const navigate = useNavigate();
  return (
    <button 
      className="bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-600 hover:to-indigo-700 text-white px-8 py-3 rounded-lg shadow-lg transform hover:scale-105 transition-transform"
      onClick={() => navigate("/profile")}
    >
      Start Interview
    </button>
  );
}

function Content() {
  const magicSentence = "Welcome to beview.ai";
  const name = useTypeWriter(magicSentence);

  const [stopAnimation, setStopAnimation] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const timer = setTimeout(() => {
      setStopAnimation(true);
    }, 4750);

    return () => clearTimeout(timer); // Cleanup the timer on component unmount
  }, []);

  useEffect(() => {
    const handleMouseMove = (event) => {
      // Only track if on the left side of the page
      if (event.clientX <= window.innerWidth / 2) {
        setMousePosition({
          x: event.clientX,
          y: event.clientY
        });
      } else {
        setMousePosition({
          x: window.innerWidth / 2, // Center value to stop rotation
          y: window.innerHeight / 2 // Center value to stop rotation
        });
      }
    };

    document.addEventListener('mousemove', handleMouseMove);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);


  const rotationX = (mousePosition.y / window.innerHeight - 0.5) * 20;
  const rotationY = (mousePosition.x / window.innerWidth - 0.5) * 20;

  return (
    <div className="text-white container mx-auto mt-10 px-4 md:px-0">
      <div className="max-w-2xl mx-auto text-center mb-12">
        <h1 className={`text-5xl font-bold mb-6 leading-relaxed ${stopAnimation ? '' : 'animate-pulse'}`}>{name}</h1>
        <p className="text-xl mb-10 leading-relaxed">A short catchy subheadline about what makes your service special</p>
        <StartInterviewButton/>
      </div>

      <div className="flex flex-wrap mt-20 mb-20 items-center p-10 rounded-lg shadow-lg hover:shadow-animation transition-shadow duration-300">
        <div className="w-full md:w-1/2 px-4 mb-8 md:mb-0">
          <h2 className="text-4xl font-semibold mb-6">Discover our Features</h2>
          <p>An engaging description about the key features of your application. Make sure to highlight the benefits and what sets it apart.</p>
        </div>
        <div className="w-full md:w-1/2 px-4">
          <img src="path-to-your-gif.gif" alt="App GIF" className="rounded-md shadow-lg w-full"/>
        </div>
      </div>

      <div className="flex flex-wrap mt-20 mb-20 items-center p-10 rounded-lg shadow-lg hover:shadow-animation transition-shadow duration-300">
        <div className="w-full md:w-1/2 px-4 mb-8 md:mb-0" style={{ perspective: '1000px' }}>
          <img 
            src="yapper2.png" 
            alt="App Image" 
            width="450" 
            height="450" 
            className="rounded-md transform transition-transform duration-300 hover:scale-105 shadow-md hover:shadow-lg"
            style={{
              transform: `rotateX(${rotationX}deg) rotateY(${rotationY}deg)`,
              transition: 'box-shadow 0.5s ease, transform 0.5s ease'
            }}
          />
        </div>
        <div className="w-full md:w-1/2 px-4">
          <h2 className="text-4xl font-semibold mb-6">Real-Time Communication</h2>
          <p className="pb-4">A compelling section that outlines why someone should opt for your service. Highlight trust factors, benefits, or unique selling propositions here.</p>
          
          <StartInterviewButton/>
        </div>
      </div>
    </div>
  );
}

function Home() { 
  return (
    <div className="h-screen bg-gradient-to-b from-purple-500 to-indigo-600 overflow-auto">
      <Navbar />
      <Content />
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/profile" element={<ProtectedRoute />}>
            <Route index element={<Profile />} />
          </Route>
          <Route path="/interview" element={<Interview />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;