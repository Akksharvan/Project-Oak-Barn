import React from 'react';
import './App.css';

import HousePricePredictor from './HousePricePredictor';

function App() {
  return (
    <div className = "app-container">
      <header className = "app-header">
        <h1>Modern House Price Predictor</h1>
      </header>
      <main className = "app-content">
        <HousePricePredictor />
      </main>
      <footer className = "app-footer">
        <p>&copy; 2023 House Price Predictor</p>
      </footer>
    </div>
  );
}

export default App;