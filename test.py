import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

zip_code = 27519
data_location = "data/{}.csv".format(zip_code)
date_columns = ["list_date", "closing_date"]

df = pd.read_csv(data_location, parse_dates = date_columns)
na = df[["closing_date", "sold_price"]].to_numpy()

print("Correlation: ", df.corr(), "\n")
print(df[["closing_date", "sold_price"]])
print("\n")
print(na.shape)