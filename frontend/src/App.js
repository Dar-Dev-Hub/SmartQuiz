import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './Navbar';
import { getNextQuestion } from './api'; 
import Overlay from './Overlay'; 

const TOTAL_QUESTIONS = 30; 

const App = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [score, setScore] = useState(0);
  const [loading, setLoading] = useState(true);
  const [initialLoading, setInitialLoading] = useState(true); 
  const [quizCompleted, setQuizCompleted] = useState(false); 

  useEffect(() => {
    fetchQuestions(); // questions from the API 
  }, []);

  const fetchQuestions = async () => {
    try {
      setLoading(true); 
      const fetchedQuestions = await getNextQuestion();
      console.log('Fetched questions:', fetchedQuestions); // Log the fetched questions to see the response
      setQuestions(fetchedQuestions);
      setLoading(false);
      setInitialLoading(false); 
    } catch (error) {
      console.error('Error fetching questions:', error);
      setLoading(false); 
      setInitialLoading(false);
    }
  };

  const handleAnswerSubmit = () => {
    const currentQuestion = questions[currentQuestionIndex];
    if (answer.toLowerCase() === currentQuestion.correctAnswer.toLowerCase()) {
      setScore(score + 1);
    }

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setAnswer('');
    } else {
      // Quiz completed, set the flag to true
      setQuizCompleted(true);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleAnswerSubmit();
    }
  };

  if (initialLoading) {
    return (
      <div>
        <Navbar />
        <div className="container">
          <p>Loading...</p>
        </div>
        <div className="footer">
          Powered by React and AI | © 2023 QuizApp Inc.
        </div>
      </div>
    );
  }

  const progress = (currentQuestionIndex / TOTAL_QUESTIONS) * 100;

  return (
    <div>
      <Navbar />
      {quizCompleted ? (
        <Overlay score={score} />
      ) : (
        <div className="container">
          <div className="progress-bar">
            <div className="progress" style={{ width: `${progress}%` }}></div>
          </div>
          <p className="question">{questions[currentQuestionIndex].question}</p>
          <input
            type="text"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter your answer"
          />
          <button onClick={handleAnswerSubmit}>Submit Answer</button>
        </div>
      )}
      <div className="footer">
        Powered by React and AI | © 2023 QuizApp Inc.
      </div>
    </div>
  );
};

export default App;
