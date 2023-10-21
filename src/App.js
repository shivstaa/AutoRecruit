import './App.css';
import React from 'react';

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom'

import Login from './pages/Login';

function App() {
  return (
    <Router>
    <div>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to='/login'>Login</Link>
          </li>
        </ul>
      </nav>

      <Routes>
        <Route path="/login" element={<Login/>}/>
      </Routes>
    </div>
  </Router>
  );
}

export default App;
