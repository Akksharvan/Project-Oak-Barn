import xgboost
import pandas as pd

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = xgboost.Booster(model_file='/Users/akksharvan/workspace/Project-Oak-Barn/Version 1/models/xgb_model.model')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_data = pd.DataFrame(data, index = [0])

    app.logger.info(input_data)

    dmatrix = xgboost.DMatrix(input_data)
    prediction = model.predict(dmatrix)

    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
