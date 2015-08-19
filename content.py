_TITLE = "DEXi Function to Derivatives"
_SUBTITLE = "This is a web-service which enables the users to input a DEXi type function (rule-based), and receive back the values of the first (partial) derivatives in the defined points. It also allows for evaluation of other non-integer points in the domain of the function."
_GPL = ("Copyright (C) 2015  Nejc Trdin\n\n"
        "This program is free software: you can redistribute it and/or modify\n"
        "it under the terms of the GNU General Public License as published by\n"
        "the Free Software Foundation, either version 3 of the License, or\n"
        "(at your option) any later version.\n\n"

        "This program is distributed in the hope that it will be useful,\n"
        "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
        "GNU General Public License for more details.\n\n"

        "You should have received a copy of the GNU General Public License\n"
        "along with this program.  If not, see <http://www.gnu.org/licenses/>.")

_ABOUT = ("This is an application which enables the users to input a DEXi type function, and produces the values of first partial derivatives in the function's defined points.\n"
          "The functions is defined in three lines: the first line gives the integer output for the corresponding sorted input values. The inputs are sorted firstly by the first attribute, then second, etc. The second line of the function gives the names of the input attributes, delimited by a comma. The last line gives the sizes of the respective input's scales, which are also integral (comma delimited).\n"
          "Any subsequent lines are interpreted as additional inputs to the constructed function, which can also be floats!\n"
          "For exact syntax check the examples above.\n"
          "The app was developed using <a href=\"http://flask.pocoo.org/\">flask</a> for serving and GUI (integrating python scripts) and <a href=\"http://www.wolfram.com/mathematica/\">mathematica</a> is used in the backend for constructing the interpolating functions (using splines) and evaluating the constructed functions.\n"
          "You can check the code and possibly contribute at <a href=\"https://github.com/nejctrdin/DEXiFunctionDerivatives\">github</a>.")

_EXAMPLE1 = ("Linear in one variable", "012 first 3")
_EXAMPLE2 = ("Linear in two variables", "012123234 first,second 3,3")
_EXAMPLE3 = ("Monotone function", "000000001000111122112333344 first,second,third 3,3,3")
_EXAMPLE4 = ("Random function", "423120124321201212013024421 first,second,third 3,3,3")
_EXAMPLE5 = ("Large example", "333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333001001111122222222122122222222233233223223233233333333000000011011222222112112222222222222222222222223333333 v1,v2,v3,v4,v5,v6 2,2,3,3,2,3")
_EXAMPLE6 = ("Linear in two variables with inputs", "012123234 first,second 3,3 1.5,2 3.3,4")

_EXAMPLES = [_EXAMPLE1, _EXAMPLE2, _EXAMPLE3, _EXAMPLE4, _EXAMPLE5, _EXAMPLE6]
