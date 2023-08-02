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
  const fetchNextQuestion = async () => {
    try {
      const response = await fetch('"question": "http://127.0.0.1:8000/question/'); // Replace API_ENDPOINT_URL with the actual API endpoint
      const data = await response.json();
      console.error(data);
      return data// Assuming the API returns the question in the "question" field
    } catch (error) {
      console.error('Error fetching next question:', error);
    }
  };
export const getNextQuestion = () => {
    return new Promise((resolve) => {
      
      setTimeout(() => {
        resolve(fetchNextQuestion);
      }, 1000); 
    });
  };
  