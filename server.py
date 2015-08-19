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
import content
from sys import argv

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.route("/")
def index():
    entries = {"title": content._TITLE,
               "subtitle": content._SUBTITLE,
               "about": content._ABOUT,
               "examples": content._EXAMPLES,
               "license": content._GPL
    }
    return render_template("index.html", entries=entries)

@app.route("/get_derivatives", methods=["POST"])
def derivatives():
    raw_function = ""
    if "names" in request.form:
        values = {}
        for field in request.form:
            if field[0] == "v":
                tmp_f = int(field.replace("v",""))
                values[tmp_f] = request.form[field]

        value_list = []
        for field in sorted(values):
            value_list.append(values[field])

        function_description = []
        function_description.append("".join(value_list))
        function_description.append(request.form["names"])
        function_description.append(request.form["multiplicity"])
        raw_function = str("\n".join(function_description))
    elif "function" in request.form:
        raw_function = request.form["function"]
    else:
        entries = {"raw_function": raw_function,
                   "ok": False,
                   "message": "Unsupported operation!",
                   "title": content._TITLE,
                   "subtitle": content._SUBTITLE,
                   "about": content._ABOUT,
                   "license": content._GPL,
        }
        return render_template("derivatives.html", entries=entries)

    t = time()
    function, arguments, success, message = parse_function(raw_function)
    raw_function = raw_function.replace("\r", "")
    raw_function = raw_function.split("\n")
    derivatives = None
    success1 = False
    message1 = ""
    multiplicities = ""
    names = ""
    if success:
        names = ",".join(arguments)
        multiplicities = raw_function[2]
    if success:
        derivatives, success1, message1 = get_derivatives(function)
        print "Query needed {0}s to execute!".format(_format_number(time() - t))

    entries = {"raw_function": raw_function,
               "ok": success and success1,
               "message": " ".join([message, message1]),
               "function": function,
               "arguments": arguments,
               "derivatives": derivatives,
               "title": content._TITLE,
               "subtitle": content._SUBTITLE,
               "about": content._ABOUT,
               "license": content._GPL,
               "names": names,
               "multiplicities": multiplicities
    }

    return render_template("derivatives.html", entries=entries)

if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1] == "license":
            print content._GPL
        else:
            app.run(port=int(argv[1]))
    else:
        app.run()
