import numpy as np
from flask import Flask, request, jsonify
from joblib import load

app = Flask(__name__)

# load the model and pre-processing objects
rbm = load('rbm_model.joblib')
scaler = load('scaler.joblib')
binarizer = load('binarizer.joblib')
regressor = load('regressor.joblib')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['data']
    data = np.reshape(data, (1, -1))
    data_scaled = scaler.transform(data)
    data_binarized = binarizer.transform(data_scaled)
    data_transformed = rbm.transform(data_binarized)
    prediction = regressor.predict(data_transformed)

    return jsonify(prediction.tolist())


if __name__ == '__main__':
    app.run(debug=True)
