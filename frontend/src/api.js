const questionData = [
    {
      question: 'What is the capital of France?',
      correctAnswer: 'Paris',
    },
    {
      question: 'What is 2 + 2?',
      correctAnswer: '4',
    },
  ];
  
  // fetch the next question
  export const getNextQuestion = () => {
    return new Promise((resolve) => {
      // remove this in a real API implementation
      setTimeout(() => {
        resolve(questionData);
      }, 1000); 
    });
  };
  