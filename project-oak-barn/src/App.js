import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputData, setInputData] = useState({});
  const [prediction, setPrediction] = useState(null);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setInputData({ ...inputData, [name]: value });
  };

  const handlePredict = async () => {
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputData),
      });

      const data = await response.json();
      setPrediction(data.prediction);
    } catch (error) {
      console.error('Error predicting:', error);
    }
  };

  return (
    <div className="App">
      <h1>Housing Price Predictor</h1>
      <div>
        <label>Living Area:</label>
        <input type="number" name="living_area" onChange={handleInputChange} />
      </div>
      {/* Add more input fields for other features */}
      <button onClick={handlePredict}>Predict</button>
      {prediction !== null && (
        <div>
          <h2>Predicted Price:</h2>
          <p>${prediction}</p>
        </div>
      )}
    </div>
  );
}

export default App;
