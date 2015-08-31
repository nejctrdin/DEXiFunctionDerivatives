from flask import Flask
from flask import request
from flask import render_template
from dexi import parse_function
from dexi import get_derivatives
from dexi import _format_number
from dexi import _create_animation
from time import time
import content
from sys import argv

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

_MISSING_ARGUMENTS = "Cannot create function animation. Missing arguments in request."
_COULD_NOT_PARSE_FUNCTION = "Could not parse function! {0}"

@app.route("/")
def index():
    # serving index page with title, subtitle, about, examples and license
    entries = {"title": content._TITLE,
               "subtitle": content._SUBTITLE,
               "about": content._ABOUT,
               "examples": content._EXAMPLES,
               "license": content._GPL
    }
    # render the page with a template
    return render_template("index.html", entries=entries)

@app.route("/get_derivatives", methods=["POST"])
def derivatives():
    # the path which serves post requests for creating derivatives
    raw_function = ""
    if "names" in request.form:
        # if "names" is in the request, it means it was called from the already
        # created derivatives - the user changed the inputs and retried the
        # derivative creation
        values = {}
        # we read the fields in the request and parse out those that start with a v
        for field in request.form:
            if field[0] == "v":
                # the values and the entries are put into a dictionary
                # before that the keys have "v"s removed and cast to int
                tmp_f = int(field.replace("v",""))
                values[tmp_f] = request.form[field]

        value_list = []
        # we sort the keys of the dictionary, to get the initial order
        # and put the values into a value list
        for field in sorted(values):
            value_list.append(values[field])

        # function is described in three lines
        function_description = []
        # output values joined, delimited with a comma
        function_description.append(",".join(value_list))
        # names are delimited by a comma (already in the request)
        function_description.append(request.form["names"])
        # multiplicities are delimited by a comma (already in the request)
        function_description.append(request.form["multiplicity"])

        # the raw function is represented as a new-line delimitied string
        raw_function = str("\n".join(function_description))

    elif "function" in request.form:
        # if function is present in request, we read it directly
        # parsing is done afterwards
        raw_function = request.form["function"]
    else:
        # if neither of them are present, we return error status
        entries = {"raw_function": raw_function,
                   "ok": False,
                   "message": "Unsupported operation!",
                   "title": content._TITLE,
                   "subtitle": content._SUBTITLE,
                   "about": content._ABOUT,
                   "license": content._GPL,
        }
        # render the derivatives page
        return render_template("derivatives.html", entries=entries)

    # we are interested in the time that took for generating the derivatives,
    # evaluations and images
    t = time()

    # we parse the function, getting the actual function, arguments, needed evaluations
    # success status and possible message
    function, arguments, evaluations, success, message = parse_function(raw_function)

    # variables are prepared for filling in - these are defaults if anything goes wrong
    raw_function = raw_function.replace("\r", "")
    raw_function = raw_function.split("\n")
    derivatives = None
    success1 = False
    message1 = ""
    multiplicities = ""
    names = ""
    image = ""
    if success:
        # if the previous step succeeded we can construct the function, get derivatives,
        # evaluations and the possible image
        names = ",".join(arguments)
        multiplicities = raw_function[2]
        derivatives, evaluations, image, success1, message1 = get_derivatives(function, evaluations, arguments)
        print "Query needed {0}s to execute!".format(_format_number(time() - t))

    # form a dictionary to return to the user
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
               "multiplicities": multiplicities,
               "evaluations": evaluations,
               "image": image
    }

    # the derivatives page is rendered
    return render_template("derivatives.html", entries=entries)

@app.route("/get_animation", methods=["POST"])
def animation():
    raw_function = ""
    if "names" in request.form:
        # if "names" is in the request, it means it was called from the already
        # created derivatives - the user changed the inputs and retried the
        # derivative creation
        values = {}
        # we read the fields in the request and parse out those that start with a v
        for field in request.form:
            if field[0] == "v":
                # the values and the entries are put into a dictionary
                # before that the keys have "v"s removed and cast to int
                tmp_f = int(field.replace("v",""))
                values[tmp_f] = request.form[field]

        value_list = []
        # we sort the keys of the dictionary, to get the initial order
        # and put the values into a value list
        for field in sorted(values):
            value_list.append(values[field])

        # function is described in three lines
        function_description = []
        # output values joined, delimited with a comma
        function_description.append(",".join(value_list))
        # names are delimited by a comma (already in the request)
        function_description.append(request.form["names"])
        # multiplicities are delimited by a comma (already in the request)
        function_description.append(request.form["multiplicity"])

        # the raw function is represented as a new-line delimitied string
        raw_function = str("\n".join(function_description))

    else:
        return _MISSING_ARGUMENTS

    # we are interested in the time that took for generating the animation
    t = time()
    # we parse the function, getting the actual function, arguments, needed evaluations
    # success status and possible message
    function, arguments, evaluations, success, message = parse_function(raw_function)

    if success:
        # if the previous step succeeded we can construct the function, get derivatives,
        # evaluations and the possible image
        anim_file_name = _create_animation(function, arguments)
        print "Function animation needed {0}s to execute!".format(_format_number(time() - t))
    else:
        return _COULD_NOT_PARSE_FUNCTION.format(message)

    # the derivatives page is rendered
    return anim_file_name 

if __name__ == "__main__":
    _HOST = "0.0.0.0"
    # parse arguments
    if len(argv) == 2:
        # if license must be displayed
        if argv[1] == "license":
            print content._GPL
        else:
            # otherwise treat the argument as port number
            app.run(host=_HOST, port=int(argv[1]))
    else:
        # otherwise just run the app on the app-decided port
        app.run(host=_HOST)
