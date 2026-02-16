import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from statsmodels.tsa.arima.model import ARIMA

# 1. Create a fresh Random Forest Model
# We simulate 10 features to match your "Live Intelligence" inputs
X = np.random.rand(100, 10)
y = np.random.randint(0, 2, 100)
rf = RandomForestClassifier(n_estimators=10).fit(X, y)
joblib.dump(rf, "rf_abandonment_model.pkl")

# 2. Create a fresh ARIMA Model
data = [50, 52, 48, 45, 55, 60, 62, 58, 55, 65, 70, 68, 62, 58]
arima_model = ARIMA(data, order=(1, 1, 1)).fit()
joblib.dump(arima_model, "arima_model.pkl")

print("✅ Success! Fresh .pkl files created in your folder.")