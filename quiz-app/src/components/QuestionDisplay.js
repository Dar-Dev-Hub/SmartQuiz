import React from 'react';
import { Typography } from '@mui/material';
import { Box } from '@mui/system';
const QuestionDisplay = ({ questionData }) => {
  return (
    <Box sx={{ padding: '20px' }}>
      <Typography variant="h2" gutterBottom>
        Question:
      </Typography>
      <Typography variant="body1" gutterBottom>
        {questionData.content}
      </Typography>
      <Typography variant="body2" gutterBottom>
        Current Question Level: {questionData.level}
        </Typography>
    </Box>
  );
};

export default QuestionDisplay;