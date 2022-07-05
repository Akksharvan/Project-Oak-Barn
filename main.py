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
    df = pd.read_csv("Real Estate Data.csv", parse_dates = ["Closing Date"])
    df = clean_data(df)
    image = linear_graph(df)

    zip_code = str(escape(request.args.get("zip_code", "")))
    zip_code_html = generate_form_html("zip_code")

    final_html = zip_code_html + zip_code + image
    return final_html

def convert_closing_date_to_days(dataframe, column_ID):
    temp_list = []

    for index, value in dataframe[column_ID].items():
        temp_list.append(value.days)

    temp_series = pd.Series(temp_list)
    dataframe[column_ID] = temp_series

def comparable_homes_df(dataframe, zip_code = "12345"):
    comparable_dataframe = dataframe
    return comparable_dataframe

def clean_data(dataframe):
    temp_df = dataframe

    time_series = temp_df["Closing Date"] - pd.Timestamp(1950, 1, 1)
    temp_df["Days Since 1950"] = time_series

    convert_closing_date_to_days(temp_df, "Days Since 1950")
    temp_df.drop(columns = "Closing Date")
    return temp_df

def linear_graph(dataframe):
    df = comparable_homes_df(dataframe)
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

def generate_form_html(criteria):
    generated_form_html = """<form action = "" method = get>
                            <label for = "{}">{}: </label>
                            <input type = "text" id = "{}" name = "{}">
                            <input type = "submit" value = "Submit">
                        </form>""".format(criteria, criteria.upper().replace("_", " "), criteria, criteria)
    
    return generated_form_html

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)