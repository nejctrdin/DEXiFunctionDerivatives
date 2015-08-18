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
from dexi import _format_number
from time import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_derivatives", methods=["POST"])
def derivatives():
    t = time()
    raw_function = request.form["function"]
    function, arguments, success, message = parse_function(raw_function)
    raw_function = raw_function.replace("\r", "")
    raw_function = raw_function.split("\n")
   
    derivatives = None
    success1 = False
    message1 = ""

    if success:
        derivatives, success1, message1 = get_derivatives(function)

    entries = {"raw_function": raw_function,
               "ok": success and success1,
               "message": " ".join([message, message1]),
               "function": function,
               "arguments": arguments,
               "derivatives": derivatives
    }

    print "Query needed {}s to execute!".format(_format_number(time() - t))

    return render_template("derivatives.html", entries=entries)

if __name__ == "__main__":
    app.run()
