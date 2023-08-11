import xgboost
import pandas as pd

from flask import Flask, request, jsonify
from flask_cors import CORS

from pathlib import Path

app = Flask(__name__)
CORS(app)

model_path = str(Path().absolute().absolute()) + "/models/price_predictor.model"
model = xgboost.Booster(model_file = model_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_data = pd.DataFrame(data, index = [0])

    for col in input_data.columns:
        input_data[col] = pd.to_numeric(input_data[col])

    prediction = model.predict(xgboost.DMatrix(input_data))
    return jsonify({'prediction': prediction.tolist()})
    

if __name__ == '__main__':
    app.run(debug=True)
