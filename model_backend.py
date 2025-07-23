# model_backend.py

import pandas as pd
from sklearn.linear_model import LinearRegression

# Function to train and predict revenue
def predict_revenue(year, month, day, units_sold):
    # Load dataset
    df = pd.read_csv("datasets/Merged_SalesData.csv")

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop missing values
    df = df.dropna(subset=['Date', 'Units Sold', 'Revenue'])

    # Extract year, month, day from Date
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Features and Target
    X = df[['Year', 'Month', 'Day', 'Units Sold']]
    y = df['Revenue']

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Prepare input for prediction
    input_data = pd.DataFrame({
        'Year': [year],
        'Month': [month],
        'Day': [day],
        'Units Sold': [units_sold]
    })

    # Return predicted revenue
    return model.predict(input_data)[0]

# 🧪 Test the function below (you can remove this when integrating)
if __name__ == "__main__":
    predicted = predict_revenue(2025, 7, 1, 500)
    print("📈 Predicted Revenue:", predicted)
