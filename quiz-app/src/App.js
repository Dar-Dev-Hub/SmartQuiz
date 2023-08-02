import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/Login';
import QuizPage from './components/QuizPage';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [jwtToken, setJwtToken] = useState('');

  useEffect(() => {
    // Check if the user is already logged in
    const token = localStorage.getItem('jwtToken');
    if (token) {
      setIsLoggedIn(true);
      setJwtToken(token);
    }
  }, []);
  
  const handleLogin = async (username, password) => {
    try {
      // Make a request to obtain the JWT token
      const response = await axios.post('http://localhost:8000/api/token/', {
        username,
        password,
      });

      if (response.status === 200) {
        const token = response.data.access;
        localStorage.setItem('jwtToken', token);
        setIsLoggedIn(true);
        setJwtToken(token);
      }
    } catch (error) {
      console.error('Failed to log in', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('jwtToken');
    setIsLoggedIn(false);
    setJwtToken('');
  };

  return (
    <div>
      {isLoggedIn ? (
        <QuizPage jwtToken={jwtToken} onLogout={handleLogout} />
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
};

export default App;
