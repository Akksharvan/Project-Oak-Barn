import React, { useState } from 'react';
import axios from 'axios';

import './HousePricePredictor.css';

const InputField = ({ label, name, value, onChange }) => (
  <div className="input-field">
    <label htmlFor={name}>{label}</label>
    <input
      type = "number"
      id = {name}
      name = {name}
      value = {value}
      onChange = {onChange}
    />
  </div>
);

const PredictionResult = ({ prediction }) => (
  <div className = "prediction-result">
    <h2>Prediction Result</h2>
    <p>Predicted Price: ${prediction}</p>
  </div>
);

const HousePricePredictor = () => {
  const [formData, setFormData] = useState({
    beds: 0,
    full_bath: 0,
    living_area_above_ground: 0,
    living_area: 0,
    year_built: 0,
  });

  const [prediction, setPrediction] = useState(null);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handlePredict = async () => {
    try {
      const response = await axios.post("https://projectoakbarnapi--akksharvan.repl.co/predict", formData);
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error('Prediction error:', error);
    }
  };

  return (
    <div className = "predictor-container">
      <h1 className = "predictor-title">House Price Predictor</h1>
      <div className = "input-container">
        <InputField
          label = "Beds:"
          name = "beds"
          value = {formData.beds}
          onChange = {handleInputChange}
        />
      </div>
      <div className = "input-container">
      <InputField
          label = "Full Bath:"
          name = "full_bath"
          value = {formData.full_bath}
          onChange = {handleInputChange}
        />
      </div>
      <div className = "input-container">
      <InputField
          label = "Living Area Above Ground:"
          name = "living_area_above_ground"
          value = {formData.living_area_above_ground}
          onChange = {handleInputChange}
        />
      </div>
      <div className = "input-container">
      <InputField
          label = "Total Living Area:"
          name = "living_area"
          value = {formData.living_area}
          onChange = {handleInputChange}
        />
      </div>
      <div className = "input-container">
      <InputField
          label = "Year Built:"
          name = "year_built"
          value = {formData.year_built}
          onChange = {handleInputChange}
        />
      </div>
      <button className="predict-button" onClick={handlePredict}>
        Predict
      </button>
      {prediction !== null && <PredictionResult prediction={prediction} />}
    </div>
  );
};

export default HousePricePredictor;
