import React, { useState, useEffect } from 'react';
import axios from 'axios';
import QuestionDisplay from './QuestionDisplay';
import AnswerSubmission from './AnswerSubmission';
import { CircularProgress, Typography, Button, LinearProgress, BottomNavigationAction, BottomNavigation } from '@mui/material';
import { ArrowBackRounded, Margin, Padding, Person2, PersonOffOutlined, QuestionAnswerRounded, QuizRounded, Timer10 } from '@mui/icons-material';
import { Box } from '@mui/system';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const QuizPage = ({ jwtToken, onLogout }) => {
  const [quizStarted, setQuizStarted] = useState(false);
  const [questionData, setQuestionData] = useState(null);
  const [quizSubmissionId, setQuizSubmissionId] = useState(null);
  const [isQuizCompleted, setIsQuizCompleted] = useState(false);
  const [questionsSubmitted, setQuestionsSubmitted] = useState(0);
  const [score, setScore] = useState(0);
  const totalQuestions = 20;
  const [UserLevel, setUserLevel] = useState(1);
  const [startTime, setStartTime] = useState(Date.now());
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    // Function to start the quiz and fetch the first question
    const startQuiz = async () => {
      try {
        const response = await axios.post(
          'http://localhost:8000/api/init-quiz/',
          {},
          { headers: { Authorization: `Bearer ${jwtToken}` } }
        );

        // Save the last question ID and quiz submission ID to local storage
        localStorage.setItem('lastQuestionId', response.data.question.id);
        localStorage.setItem('quizSubmissionId', response.data.quiz_submission_id);

        // Update state with the quiz submission ID and first question data
        setQuizSubmissionId(response.data.quiz_submission_id);
        setQuestionData(response.data.question);

        // Set quizStarted to true to indicate that the quiz has started
        setQuizStarted(true);
      } catch (error) {
        console.log('Failed to start the quiz:', error);
      }
    };

    // Check if the last question ID and quiz submission ID are available in local storage
    const lastQuestionId = localStorage.getItem('lastQuestionId');
    const quizSubmissionId = localStorage.getItem('quizSubmissionId');

    // Function to fetch the question data from the server using the last question ID
    const fetchQuestionData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/questions/${lastQuestionId}/`,
          { headers: { Authorization: `Bearer ${jwtToken}` } }
        );

        setQuestionData(response.data);

        // After fetching the question data, set the quiz submission ID and start the quiz
        setQuizSubmissionId(quizSubmissionId);
        setQuizStarted(true);
      } catch (error) {
        console.log('Failed to fetch question data:', error);
      }
    };

    // If the last question ID and quiz submission ID are available, fetch the question data
    if (lastQuestionId && quizSubmissionId) {
      console.log('Resuming the quiz...');
      console.log('Last question ID:', lastQuestionId);
      fetchQuestionData();
    } else {
      // If the last question ID and quiz submission ID are not available, start the quiz as usual
      console.log('Starting the quiz...');
      startQuiz();
      setStartTime(Date.now());
    }
  }, [jwtToken]);


  useEffect(() => {
    const interval = setInterval(() => {
      const currentTime = Date.now();
      setElapsedTime(currentTime - startTime);
    }, 1000);

    return () => clearInterval(interval);
  }, [startTime]);

  const formatElapsedTime = (milliseconds) => {
    const totalSeconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;

    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  const handleAnswerSubmission = async (questionId, choiceId, isCorrect) => {
    try {
      const response = await axios.post(
        `http://localhost:8000/api/quiz-submissions/${quizSubmissionId}/submit/`,
        { question: questionId, choice: choiceId, is_correct: isCorrect },
        { headers: { Authorization: `Bearer ${jwtToken}` } }
      );
      console.log('Answer submitted:', response.data);
      setScore(response.data.score);
      if (response.data.detail == "Quiz completed.") {
        setIsQuizCompleted(true);
        console.log('Quiz completed');
        setUserLevel(questionData.level);

        setQuestionsSubmitted(20)

      }
      else {

        if (response.data.next_question) {
          setUserLevel(response.data.next_question.level - 1);

          // If there is a next question, update state with the new question data
          setQuestionData(response.data.next_question);
          setQuestionsSubmitted((prev) => prev + 1); // Increment the number of questions submitted
          const msg = isCorrect ? ' ✔️ Correct answer!' : ' ❌ Wrong answer!';
          toast(msg, {
            position: "top-left",
            autoClose: 5,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "light",
          });
        } else {
          // If there is no next question, the quiz is completed
          setIsQuizCompleted(true);
        }
      }

    } catch (error) {
      console.log('Failed to submit answer:', error);
    }
  };

  const sidebarProgress = () => {
    // Calculate the percentage progress based on the number of questions submitted
    const progress = (questionsSubmitted / totalQuestions) * 100;

    return (
      <div className="sidebar-progress">
        <LinearProgress variant="determinate" value={progress} />
        <div className="progress-label">
          {questionsSubmitted}/{totalQuestions} Questions
        </div>
      </div>
    );
  };

  return (
    <Box sx={{ padding: '20px', textAlign: 'center' }}>
      {quizStarted ? (
        <div>
          {isQuizCompleted || questionsSubmitted === totalQuestions ? (
            <div>
              <Typography variant="h5" gutterBottom>
                Quiz completed! Your final score is {score}.
              </Typography>
              <Typography variant="h5" gutterBottom>
                According to this assessment, you should take the Mastery Course Level {UserLevel}
              </Typography>
              <Typography variant="h5" gutterBottom>
                You took {formatElapsedTime(elapsedTime)} to complete the quiz.
              </Typography>
              <Button variant="contained" color="primary" onClick={onLogout}>
                Logout
              </Button>
            </div>
          ) : (
            <div>
              <Box sx={{ marginBottom: '20px' }}>{sidebarProgress()}</Box>
              <QuestionDisplay questionData={questionData} />
              <AnswerSubmission
                questionId={questionData.id}
                handleAnswerSubmission={handleAnswerSubmission}
                questionData={questionData}
              />
              <Typography variant="h5" gutterBottom>
                Time Elapsed: {formatElapsedTime(elapsedTime)}
              </Typography>
            </div>
          )}
          <BottomNavigation
            sx={{
              position: 'fixed',
              bottom: 0,
              left: 0,
              right: 0,
              backgroundColor: '#f0f0f0',
              padding: '10px',
            }}
            showLabels
          >
            <BottomNavigationAction
              component={"a"}
              href={`http://localhost:8000/api/quiz-submissions/${quizSubmissionId}`}
              target='_blank'
              label={`Quiz ID - ${quizSubmissionId}`}
              icon={<QuizRounded />}
            />
            <BottomNavigationAction label="Logout" icon={<PersonOffOutlined />} onClick={onLogout} />
          </BottomNavigation>
          <ToastContainer />
        </div>
      ) : (
        <CircularProgress />
      )}
    </Box>
  );
};

export default QuizPage;
