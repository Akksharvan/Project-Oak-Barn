import xgboost
import pandas

from flask import Flask
from flask import request
from flask import jsonify

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = xgboost.Booster(model_file='/Users/akksharvan/workspace/Project-Oak-Barn/Version 1/models/xgb_model.model')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    input_data = pd.DataFrame(data, index=[0])
    prediction = model.predict(xgb.DMatrix(input_data))

    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)