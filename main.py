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
    head_html = generate_head_html()
    foot_html = generate_foot_html()

    form_html = generate_form_html("zip_code", "time_in_days", "living_area_in_square_feet", "year_built", "number_of_beds", "full_baths", "half_baths")

    final_html = head_html + form_html + foot_html
    return final_html

@app.route("/prediction/")
def prediction():
    head_html = generate_head_html()
    foot_html = generate_foot_html()

    zip_code = str(escape(request.args.get("zip_code", "")))
    time = str(escape(request.args.get("time_in_days", "")))
    living_area = str(escape(request.args.get("living_area_in_square_feet", "")))
    year_built = str(escape(request.args.get("year_built", "")))
    beds = str(escape(request.args.get("number_of_beds", "")))
    full_bath = str(escape(request.args.get("full_baths", "")))
    half_bath = str(escape(request.args.get("half_baths", "")))

    criteria_dict = {
        "zip_code": int(zip_code),
        "time": int(time),
        "living_area": int(living_area), 
        "year_built": int(year_built),
        "beds": int(beds),
        "full_bath": int(full_bath),
        "half_bath": int(half_bath)
        }
    
    df = pd.read_csv("Real Estate Data.csv", parse_dates = ["closing_date"])
    df = clean_data(df)

    df = comparable_homes_df(df, criteria_dict = criteria_dict)
    prediction, score, image = linear_graph(df, criteria_dict["time"])

    back_button = generate_button_html("Back")

    final_html = head_html + prediction + score + image + back_button + foot_html
    return final_html

def comparable_homes_df(dataframe, criteria_dict):
    comparable_dataframe_rows = []

    for index, row in dataframe.iterrows():
        if criteria_dict["zip_code"] != row["zip_code"]:
            continue
        elif ((criteria_dict["living_area"] * 0.75) > row["living_area"]) or ((criteria_dict["living_area"] * 1.25) < row["living_area"]):
            continue
        elif ((criteria_dict["year_built"] - 20) > row["year_built"]) or ((criteria_dict["year_built"] + 20) < row["year_built"]):
            continue
        elif ((criteria_dict["beds"] - 2) > row["beds"]) or ((criteria_dict["beds"] + 2) < row["beds"]):
            continue
        elif ((criteria_dict["full_bath"] - 2) > row["full_bath"]) or ((criteria_dict["full_bath"] + 2) < row["full_bath"]):
            continue
        elif ((criteria_dict["half_bath"] - 1) > row["half_bath"]) or ((criteria_dict["half_bath"] + 1) < row["half_bath"]):
            continue
        else:
            comparable_row = row.to_numpy()
            comparable_dataframe_rows.append(comparable_row)

    comparable_dataframe = pd.DataFrame(comparable_dataframe_rows)

    comparable_dataframe_columns = dataframe.columns.to_numpy()
    comparable_dataframe.columns = comparable_dataframe_columns

    return comparable_dataframe

def convert_closing_date_to_days(dataframe, column_ID):
    temp_list = []

    for index, value in dataframe[column_ID].items():
        temp_list.append(value.days)

    temp_series = pd.Series(temp_list)
    dataframe[column_ID] = temp_series

def clean_data(dataframe):
    temp_df = dataframe

    time_series = temp_df["closing_date"] - pd.Timestamp(1950, 1, 1)
    temp_df["days_since_1950"] = time_series

    convert_closing_date_to_days(temp_df, "days_since_1950")
    temp_df.drop(columns = "closing_date")
    return temp_df

def linear_graph(dataframe, time = 0):
    df = dataframe
    x = np.array(df["days_since_1950"]).reshape(-1, 1)
    y = np.array(df["sold_price"]).reshape(-1, 1)

    today = pd.Timestamp.now() - pd.Timestamp(1950, 1, 1)

    reg = linear_model.LinearRegression()
    reg.fit(x, y)

    prediction = "<p>Predicted Price After {} Days: ${:,.2f}".format(time, round(reg.predict([[today.days + time]])[0][0], 2))
    score = "<p>Prediction Score: {}%</p>".format(round(reg.score(x, y)*100, 2))

    fig = Figure()
    ax = fig.subplots()
    ax.plot(x, reg.predict(x), "black")

    buf = BytesIO()
    fig.savefig(buf, format = "png")

    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_image = "<img src = 'data:image/png;base64, {}'/>".format(fig_data)
    
    return (prediction, score, fig_image)

def generate_form_html(*criteria_list):
    generated_form_html = "<form action = \"/prediction\" method = \"get\">"

    for criteria in criteria_list:
        temp_html = "<label for = \"{}\">{}:</label>".format(criteria, criteria.title().replace("_", " "))

        if criteria == "zip_code":
            temp_html += "<select id = \"{}\" name = \"{}\">".format(criteria, criteria)
            temp_html += "<option value = \"27519\">27519</option>"
            temp_html += "</select>"
        else:
            temp_html += "<input type = \"text\" id = \"{}\" name = \"{}\">".format(criteria, criteria)
        
        new_line_html = "<br>"
        
        generated_form_html += temp_html + new_line_html

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