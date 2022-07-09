# import numpy as np
# import pandas as pd

# from matplotlib.figure import Figure
# from sklearn.linear_model import LinearRegression

# import base64
# from io import BytesIO

# def closing_date_to_days(dataframe):
#     temp_list = []
#     for value in dataframe["closing_date"]:
#         time = value - pd.Timestamp(1950, 1, 1)
#         temp_list.append(time.days)
    
#     temp_series = pd.Series(temp_list)
#     dataframe["closing_date"] = temp_series

# zip_code = 27519
# data_location = "data/{}.csv".format(zip_code)
# date_columns = ["list_date", "closing_date"]

# df = pd.read_csv(data_location, parse_dates = date_columns)
# closing_date_to_days(df)

# X = df[["closing_date", "beds"]].to_numpy()
# y = df[["sold_price"]]

# regression = LinearRegression()
# regression.fit(X, y)

# prediction = regression.predict([[27000, 3]])[0][0]
# score = regression.score(X, y)

# message = "Prediction = {:,.2f}\nScore = {}".format(prediction, score)
# print(message)