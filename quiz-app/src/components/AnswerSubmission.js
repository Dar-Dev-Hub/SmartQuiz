import React, { useState, useEffect } from 'react';
import { Typography, List, ListItem, ListItemText, Radio, Button } from '@mui/material';
import { Box } from '@mui/system';

const shuffleArray = (array) => {
  // Create a copy of the original array
  const shuffledArray = array.slice();
  // Loop through the array and swap each element with a random element
  for (let i = shuffledArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
  }
  return shuffledArray;
};

const AnswerSubmission = ({ questionId, handleAnswerSubmission, questionData }) => {
  const [selectedChoice, setSelectedChoice] = useState(null);
  const [shuffledChoices, setShuffledChoices] = useState([]);

  useEffect(() => {
    // Shuffle the choices when the question data changes
    setShuffledChoices(shuffleArray(questionData.choices));
  }, [questionData.choices]);

  const handleChoiceSelection = (choiceId) => {
    setSelectedChoice(choiceId);
  };

  const handleSubmit = () => {
    if (selectedChoice) {
      // Determine if the selected choice is correct
      const selectedChoiceData = questionData.choices.find(
        (choice) => choice.id === selectedChoice
      );
      const isCorrect = selectedChoiceData.is_correct;

      // Call the handleAnswerSubmission function with the selected choice and correctness
      handleAnswerSubmission(questionId, selectedChoice, isCorrect);
    }
  };

  return (
    <Box sx={{ padding: '20px' }}>
    <Typography variant="h2" gutterBottom>
      Select your answer:
    </Typography>
    <List>
      {shuffledChoices.map((choice) => (
        <ListItem key={choice.id} button onClick={() => handleChoiceSelection(choice.id)}>
          <Radio
            edge="start"
            checked={selectedChoice === choice.id}
            disableRipple
            inputProps={{ 'aria-labelledby': `label-${choice.id}` }}
          />
          <ListItemText id={`label-${choice.id}`} primary={choice.content} />
        </ListItem>
      ))}
    </List>
    <Button variant="contained" color="primary" onClick={handleSubmit}>
      Submit
    </Button>
  </Box>
);
};

export default AnswerSubmission;
