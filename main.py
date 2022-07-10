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

    form_html = generate_form_html("zip_code", "property_type", "time_in_days", "living_area_in_square_feet", "year_built", "number_of_beds", "full_baths", "half_baths")

    final_html = head_html + form_html + foot_html
    return final_html

@app.route("/prediction/")
def prediction():
    head_html = generate_head_html()
    foot_html = generate_foot_html()

    zip_code = str(escape(request.args.get("zip_code", "")))
    property_type = str(escape(request.args.get("property_type", "")))
    time = str(escape(request.args.get("time_in_days", "")))
    living_area = str(escape(request.args.get("living_area_in_square_feet", "")))
    year_built = str(escape(request.args.get("year_built", "")))
    beds = str(escape(request.args.get("number_of_beds", "")))
    full_bath = str(escape(request.args.get("full_baths", "")))
    half_bath = str(escape(request.args.get("half_baths", "")))

    criteria_dict = {
        "zip_code": int(zip_code),
        "property_type": str(property_type),
        "time": int(time),
        "living_area": int(living_area), 
        "year_built": int(year_built),
        "beds": int(beds),
        "full_bath": int(full_bath),
        "half_bath": int(half_bath)
        }
    
    data_location = get_data_location(criteria_dict["zip_code"])
    df = pd.read_csv(data_location, parse_dates = ["closing_date"])

    df = comparable_homes_df(df, criteria_dict = criteria_dict)
    prediction, score, image = linear_graph(df, criteria_dict["time"], criteria_dict["living_area"], criteria_dict["year_built"], criteria_dict["beds"], criteria_dict["full_bath"], criteria_dict["half_bath"])

    back_button = generate_button_html("Back")

    final_html = head_html + prediction + score + image + back_button + foot_html
    return final_html

def comparable_homes_df(dataframe, criteria_dict):
    comparable_dataframe_rows = []

    for index, row in dataframe.iterrows():
        if criteria_dict["property_type"] != row["property_type"]:
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
    comparable_dataframe.columns = dataframe.columns.to_numpy()

    return comparable_dataframe

def get_data_location(zip_code):
    data_location = "data/{}.csv".format(zip_code)
    return data_location

def linear_graph(dataframe, time, living_area, year_built, beds, full_bath, half_bath):
    df = dataframe
    iv_list = [time, living_area, year_built, beds, full_bath, half_bath]

    X = df[["days_since_1950", "living_area", "year_built", "beds", "full_bath", "half_bath"]].to_numpy()
    y = df[["sold_price"]].to_numpy()

    today = pd.Timestamp.now() - pd.Timestamp(1950, 1, 1)
    iv_list[0] = today.days + time

    reg = linear_model.LinearRegression()
    reg.fit(X, y)


    prediction = reg.predict([iv_list])[0][0]
    prediction = "<p>Predicted Price After {} Days: ${:,.2f}".format(time, prediction)

    score = reg.score(X, y) * 100
    score = "<p>Prediction Score: {:.2f}%</p>".format(score)

    # x_array = np.array([1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030])
    # y_array = np.array([])

    # for point in x_array:
    #     temp_y = intercept + (coefficient * point)
    #     y_array = np.append(y_array, temp_y)
    
    # print(x_array)
    # print(y_array)

    fig = Figure()
    ax = fig.subplots()
    # ax.plot(x_array, y_array, "black")

    buf = BytesIO()
    fig.savefig(buf, format = "png")

    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_image = "<img src = 'data:image/png;base64, {}'/>".format(fig_data)
    
    return (prediction, score, fig_image)

def generate_form_html(*criteria_list):
    generated_form_html = "<form action = \"/prediction\" method = \"get\">"

    for criteria in criteria_list:
        temp_html = "<label for = \"{}\">{}:</label>".format(criteria, criteria.title().replace("_", " "))

        if criteria == "zip_code" or criteria == "property_type":
            temp_html += "<select id = \"{}\" name = \"{}\">".format(criteria, criteria)
            if criteria == "zip_code":
                temp_html += "<option value = \"27519\">27519</option>"
            elif criteria == "property_type":
                temp_html += "<option value = \"Detached\">Detached</option>"
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