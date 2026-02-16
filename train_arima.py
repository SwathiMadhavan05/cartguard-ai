import pandas as pd
import joblib
from statsmodels.tsa.arima.model import ARIMA
import os

# 1. Load Data
daily = pd.read_csv('daily_abandons.csv')
daily['date'] = pd.to_datetime(daily['date'])
daily.set_index('date', inplace=True)

# 2. Prepare and Train
train_size = int(0.8 * len(daily))
train = daily['abandon_count'][:train_size]

model = ARIMA(train, order=(1,1,1))
fitted_model = model.fit()

# 3. Save Model (Using joblib for consistency)
joblib.dump(fitted_model, 'arima_model.pkl')

print("✅ NEW arima_model.pkl CREATED SUCCESSFULLY!")