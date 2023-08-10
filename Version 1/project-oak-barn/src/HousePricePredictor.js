import React, { useState } from 'react';
import axios from 'axios';

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
      const response = await axios.post('http://127.0.0.1:5000/predict', formData);
      setPrediction(response.data.prediction);
    } catch (error) {
      console.error('Prediction error:', error);
    }
  };

  return (
    <div>
      <h1>House Price Predictor</h1>
      <div>
        <label>Beds:</label>
        <input
          type="number"
          name="beds"
          value={formData.beds}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <label>Full Baths:</label>
        <input
          type="number"
          name="full_bath"
          value={formData.full_bath}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <label>Living Area Above Ground:</label>
        <input
          type="number"
          name="living_area_above_ground"
          value={formData.living_area_above_ground}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <label>Living Area:</label>
        <input
          type="number"
          name="living_area"
          value={formData.living_area}
          onChange={handleInputChange}
        />
      </div>
      <div>
        <label>Year Built:</label>
        <input
          type="number"
          name="year_built"
          value={formData.year_built}
          onChange={handleInputChange}
        />
      </div>
      <button onClick={handlePredict}>Predict</button>
      {prediction !== null && (
        <div>
          <h2>Prediction Result</h2>
          <p>Predicted Price: ${prediction}</p>
        </div>
      )}
    </div>
  );
};

export default HousePricePredictor;