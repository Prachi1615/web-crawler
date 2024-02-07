// src/components/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const handleAskQuestion = async () => {
    try {
      const response = await axios.post('http://localhost:3001/answer-question', { question });
      setAnswer(response.data.pythonResult.answer);
    } catch (error) {
      console.error('Error calling Node.js server:', error);
    }
  };

  return (
    <div className="app-container">
      <h1>Question Answering App</h1>
      <label>
        Ask a Question:
        <input type="text" value={question} onChange={(e) => setQuestion(e.target.value)} />
      </label>
      <br />
      <button onClick={handleAskQuestion}>Ask Question</button>
      <br />
      {answer && (
        <div>
          <h2>Answer:</h2>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
