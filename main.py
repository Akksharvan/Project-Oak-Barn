from flask import Flask
from flask import request, escape

import numpy as np
import pandas as pd

import base64
from io import BytesIO

from matplotlib.figure import Figure
from sklearn import linear_model

app = Flask(__name__)

@app.route("/")
def index():
    image = process_data()

    zip_code = str(escape(request.args.get("zip_code", "")))
    html = """<form action = "" method = get> 
                    <input type = "text" name = "zip_code">
                    <input type = "submit" value = "Display">
                </form>"""
    return html + zip_code + image

def convert_closing_date_to_days(dataframe, column_ID):
    temp_list = []

    for index, value in dataframe[column_ID].items():
        temp_list.append(value.days)

    temp_series = pd.Series(temp_list)
    dataframe[column_ID] = temp_series

def comparable_homes_df(dataframe):
    comparable_dataframe = dataframe
    return comparable_dataframe

def process_data():
    df = pd.read_csv("Real Estate Data.csv", parse_dates = ["Closing Date"])

    time_series = df["Closing Date"] - pd.Timestamp(1950, 1, 1)
    df["Days Since 1950"] = time_series
    
    convert_closing_date_to_days(df, "Days Since 1950")
    df.drop(columns = "Closing Date")

    # Linear Regression
    x = df[["Days Since 1950"]]
    y = df[["Sold Price"]]

    reg = linear_model.LinearRegression()
    reg.fit(x, y)

    fig = Figure()
    ax = fig.subplots()
    ax.plot(x, reg.predict(x), "black")

    buf = BytesIO()
    fig.savefig(buf, format = "png")

    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_image = "<img src = 'data:image/png;base64, {}'/>".format(fig_data)
    
    return fig_image

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)