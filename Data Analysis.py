import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

#name

# Function Used for Cleaner Code
def convertTimeColumnToDays(dataframe, column_ID):
    temp_list = []

    for index, value in dataframe[column_ID].items():
        temp_list.append(value.days)


    temp_series = pd.Series(temp_list)
    dataframe[column_ID] = temp_series

# Function Used to Create List of Comparable Homes from DataFrame
def comparable_homes(dataframe, address):
    comparable_homes_df = dataframe
    
    return comparable_homes_df

# Initializing Primary DataFrame From .csv File
df_cols = ["Sold Price"]
df = pd.read_csv("Real Estate Data.csv", parse_dates = ["Closing Date"])

# Changing Closing Date Column to Days Since 1950
timeSeries = df["Closing Date"] - pd.Timestamp(1950, 1, 1)
df["Days Since 1950"] = timeSeries
convertTimeColumnToDays(df, "Days Since 1950")
df.drop(columns = "Closing Date")

# Linear Regression
x = df[["Days Since 1950"]]
y = df[["Sold Price"]]

reg = linear_model.LinearRegression()
reg.fit(x, y)


fig, ax = plt.subplots()
ax.plot(df["Days Since 1950"], reg.predict(x), "g")

plt.show()