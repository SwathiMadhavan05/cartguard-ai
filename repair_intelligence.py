import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

print("🧠 Upgrading AI Logic...")

# 1. Create a Realistic Training Dataset
# Features: [Items, Value, Time, Platform, 0, 0, 0, 0, 0, 0]
data = []
# Create 500 "Good" sessions (Low price, high time)
for _ in range(500):
    data.append([np.random.randint(2, 8), np.random.uniform(20, 100), np.random.uniform(5, 15), 0, 0,0,0,0,0,0, 0]) # 0 = Purchase

# Create 500 "Bad" sessions (High price, very low time)
for _ in range(500):
    data.append([1, np.random.uniform(1000, 2000), np.random.uniform(0.1, 1.0), 1, 0,0,0,0,0,0, 1]) # 1 = Abandon

df = pd.DataFrame(data)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# 2. Train the model to recognize the pattern
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# 3. Save the "Intelligent" model
joblib.dump(rf, "rf_abandonment_model.pkl")
print("✅ Intelligence Upgrade Complete! Now try your negative inputs in the app.")