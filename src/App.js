import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Profile from './pages/Profile';
import Interview from './pages/Interview';
import { AuthProvider } from './components/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

function StartInterviewButton() {
  const navigate = useNavigate();
  return <button onClick={() => navigate('/profile')}>Start Interview</button>;
}

function Home() {
  return (
    <div>
      <Navbar />  
      <StartInterviewButton />
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