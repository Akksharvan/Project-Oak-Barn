import pandas as pd
import xgboost as xgb

from sklearn.model_selection import train_test_split

training_data = pd.read_csv('/Users/akksharvan/workspace/Project-Oak-Barn/Version 1/data/27519.csv')

X = training_data.drop(['sold_price', 'sold_price_per_sq_ft'], axis=1)
y = training_data['sold_price']

X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

xgb_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)

xgb_model.fit(X_train, y_train,
              eval_set=[(X_valid, y_valid)],
              early_stopping_rounds=10,
              verbose=True)

xgb_model.save_model('xgb_model.model')