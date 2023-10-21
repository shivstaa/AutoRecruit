import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Profile from './pages/Profile';
import Interview from './pages/Interview';
function StartInterviewButton() {
  const navigate = useNavigate();
  return <button onClick={() => navigate('/profile')}>Start Interview</button>;
}

function Home() {
  return (
    <div>
      <Navbar />  {/* <-- Use the Navbar component here */}
      <StartInterviewButton />
    </div>
  );
}

function App() {
  return (
    <main>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/interview" element={<Interview />} />
        </Routes>
      </Router>
    </main>
  );
}

export default App;
