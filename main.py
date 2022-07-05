from flask import Flask
from flask import request, escape

app = Flask(__name__)

@app.route("/")
def index():
    zip_code = str(escape(request.args.get("zip_code", "")))
    html = """<form action = "" method = get> 
                    <input type = "text" name = "zip_code">
                    <input type = "submit" value = "Display">
                </form>"""
    return html + zip_code


if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 8080, debug = True)