from email import header
from inspect import formatannotation
from flask import Flask
from flask import request, escape
import fontTools

import pandas as pd

import base64
from io import BytesIO

from matplotlib.figure import Figure
from sklearn import linear_model

app = Flask(__name__)

@app.route("/")
def index():
    head = generate_head_html()
    foot = generate_foot_html()

    form_html = generate_form_html("zip_code", "time_in_days", "living_area_in_square_feet", "year_built", "number_of_beds", "full_baths", "half_baths")

    final_html = head + form_html + foot
    return final_html

@app.route("/prediction/")
def prediction():
    head = generate_head_html()
    foot = generate_foot_html()

    zip_code = str(escape(request.args.get("zip_code", "")))
    time = str(escape(request.args.get("time_in_days", "")))
    living_area = str(escape(request.args.get("living_area_in_square_feet", "")))
    year_built = str(escape(request.args.get("year_built", "")))
    beds = str(escape(request.args.get("number_of_beds", "")))
    full_bath = str(escape(request.args.get("full_baths", "")))
    half_bath = str(escape(request.args.get("half_baths", "")))

    df = pd.read_csv("Real Estate Data.csv", parse_dates = ["Closing Date"])
    df = clean_data(df)

    # df = comparable_homes_df(df)
    score, image = linear_graph(df)

    back_button = generate_button_html("Back")

    final_html = head + score + image + back_button + foot
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
    df = dataframe
    x = df[["Days Since 1950"]]
    y = df[["Sold Price"]]

    reg = linear_model.LinearRegression()
    reg.fit(x, y)
    score = "<p>Prediction Score: {}%</p>".format(str(round(reg.score(x, y)*100, 2)))

    fig = Figure()
    ax = fig.subplots()
    ax.plot(x, reg.predict(x), "black")

    buf = BytesIO()
    fig.savefig(buf, format = "png")

    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_image = "<img src = 'data:image/png;base64, {}'/>".format(fig_data)
    
    return (score, fig_image)

def generate_form_html(*criteria_list):
    generated_form_html = "<form action = \"/prediction\" method = \"get\">"

    for criteria in criteria_list:
        temp_html = "<label for = \"{}\">{}: </label>".format(criteria, criteria.title().replace("_", " "))
        temp_html_two = "<input type = \"text\" id = \"{}\" name = \"{}\">".format(criteria, criteria)
        new_line_html = "<br>"
        generated_form_html += temp_html + temp_html_two + new_line_html

    generated_form_html += "<input type = \"submit\" value = \"Submit\"> </form>"
    
    return generated_form_html

def generate_button_html(button_label):
    button_html = "<a href = \"/\">"
    button_html += "<form action = \"/\">"
    button_html += "<input class = \"btn\" type = \"button\" value = \"{}\">".format(button_label)
    button_html += "</form>"
    button_html += "</a>"

    return button_html

def generate_head_html():
    head = "<!DOCTYPE html>"
    head += "<html>"
    head += "<head>"
    head += "<title>House Price Predictor</title>"
    head += "<link rel = \"stylesheet\" href = \"/static/styles/styles.css\">"
    head += "</head>"
    head += "<body>"
    return head

def generate_foot_html():
    foot = "</body>"
    foot += "</html>"
    return foot

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)