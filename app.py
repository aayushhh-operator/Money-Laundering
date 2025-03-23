from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
import pandas as pd
import joblib  # Import joblib instead of pickle

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load your pre-trained model (Assuming 'best_model.joblib' is the saved model)
best_model = joblib.load('Beast_model.pkl')  # Using joblib to load the model

# Define the mappings for features
Payment_currency = {
    'Albanian lek': 0,
    'Dirham': 1,
    'Euro': 2,
    'Indian Rupee': 3,
    'Mexican Peso': 4,
    'Moroccan Dirham': 5,
    'Naira': 6,
    'Pakistani rupee': 7,
    'Swiss franc': 8,
    'Turkish lira': 9,
    'UK pounds': 10,
    'US dollar': 11,
    'Yen': 12
}

Received_currency = {
    'Albanian lek': 0,
    'Dirham': 1,
    'Euro': 2,
    'Indian Rupee': 3,
    'Mexican Peso': 4,
    'Moroccan Dirham': 5,
    'Naira': 6,
    'Pakistani rupee': 7,
    'Swiss franc': 8,
    'Turkish lira': 9,
    'UK pounds': 10,
    'US dollar': 11,
    'Yen': 12
}

Sender_bank_location = {
    'Albania': 0,
    'Austria': 1,
    'France': 2,
    'Germany': 3,
    'India': 4,
    'Italy': 5,
    'Japan': 6,
    'Mexico': 7,
    'Morocco': 8,
    'Netherlands': 9,
    'Nigeria': 10,
    'Pakistan': 11,
    'Spain': 12,
    'Switzerland': 13,
    'Turkey': 14,
    'UAE': 15,
    'UK': 16,
    'USA': 17
}

Payment_type = {
    'ACH': 0,
    'Cash Deposit': 1,
    'Cash Withdrawl': 2,
    'Cheque': 3,
    'Credit Card': 4,
    'Cross-border': 5,
    'Debit Card': 6
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from form
    received_currency = request.form['Received_currency']
    payment_type = request.form['Payment_type']
    payment_currency = request.form['Payment_currency']
    receiver_bank_location = request.form['Receiver_bank_location']
    amount = float(request.form['Amount'])
    
    # Mapping the input values
    received_currency = Received_currency.get(received_currency, -1)
    payment_type = Payment_type.get(payment_type, -1)
    payment_currency = Payment_currency.get(payment_currency, -1)
    receiver_bank_location = Sender_bank_location.get(receiver_bank_location, -1)

    # Prepare input for prediction
    new_data = pd.DataFrame([{
        'Received_currency': received_currency,
        'Payment_type': payment_type,
        'Payment_currency': payment_currency,
        'Receiver_bank_location': receiver_bank_location,
        'Amount': amount
    }])

    # Predict using the loaded model
    prediction = best_model.predict(new_data)

    # Return result as JSON
    result = 'Suspicious' if prediction[0] == 1 else 'Not Suspicious'
    return jsonify({'prediction': result})

if __name__ == "__main__":
    app.run(debug=True)
