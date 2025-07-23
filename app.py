# app.py

from flask import Flask, request, jsonify
from model_backend import predict_revenue

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "🎯 Flask Sales Prediction API is running! Use /predict (POST) to get revenue."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Extract input values
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        units_sold = data.get('units_sold')

        # Check if any value is missing
        if None in [year, month, day, units_sold]:
            return jsonify({'error': 'Missing input values'}), 400

        # Predict using backend model
        result = predict_revenue(year, month, day, units_sold)

        return jsonify({
            'year': year,
            'month': month,
            'day': day,
            'units_sold': units_sold,
            'predicted_revenue': round(result, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
