import './Overlay.css'; 
import React from 'react';

const Overlay = ({ score }) => {
  return (
    <div className="overlay">
      <p className="completion-message">Quiz Completed!</p>
      <p className="score">
        Score: <span>{score}</span>
      </p>
    </div>
  );
};

export default Overlay;
