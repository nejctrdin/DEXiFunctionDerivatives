from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash
from dexi import parse_function
from dexi import get_derivatives
 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_derivatives", methods=["POST"])
def derivatives():
    raw_function = request.form["function"]
    function, arguments, success, message = parse_function(raw_function)
    raw_function = raw_function.replace("\r", "")
   
    derivatives, success1, message1 = [None] * 3

    if success:
        derivatives, success1, message1 = get_derivatives(function)
        
    entries = {"raw_function": raw_function,
               "ok": success and success1,
               "message": " ".join([message, message1]),
               "function": function,
               "arguments": arguments,
               "derivatives": derivatives
    }

    return render_template("derivatives.html", entries=entries)

if __name__ == "__main__":
    app.run()
