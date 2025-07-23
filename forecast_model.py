# forecast_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Load merged CSV file
df = pd.read_csv("datasets/Merged_SalesData.csv")

# Step 2: Parse 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Step 3: Drop rows with missing or invalid data
df.dropna(subset=['Date', 'Units Sold', 'Revenue'], inplace=True)

# Step 4: Feature Engineering: extract Year, Month, Day from Date
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

# Step 5: Prepare features (X) and target (y)
X = df[['Year', 'Month', 'Day', 'Units Sold']]
y = df['Revenue']

# Step 6: Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 7: Train Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 8: Predict and Evaluate
y_pred = model.predict(X_test)

print("✅ Model Training Complete")
print("🔍 Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("📊 R² Score:", r2_score(y_test, y_pred))

# Step 9: Forecast for future inputs
future_data = pd.DataFrame({
    'Year': [2025, 2025, 2025],
    'Month': [7, 8, 9],
    'Day': [1, 1, 1],
    'Units Sold': [400, 500, 600]
})

future_data['Predicted Revenue'] = model.predict(future_data)
print("\n📅 Future Revenue Forecast:")
print(future_data)
