# the title of the app
_TITLE = "DEXi Function to Derivatives - DEVELOPMENT"

# the subtitle appearing in the banner
_SUBTITLE = "This is a web-service which enables the users to input a DEXi type function (rule-based), and receive back the values of the first (partial) derivatives in the defined points. It also allows for evaluation of other non-integer points in the domain of the function and plotting the functions with less than three arguments."

# the GPL license
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
        "along with this program.  If not, see <a href=\"http://www.gnu.org/licenses/\">licenses</a>.")

# the about box
_ABOUT = ("This is an application which enables the users to input a DEXi type function, and produces the values of first partial derivatives in the function's defined points.\n"
          "The functions is defined in three lines: the first line gives the float output for the corresponding sorted input values (the values can be concatenated together, if they are all less than 10 and at least 0 and integers, otherwise they must be comma separated). The inputs are sorted firstly by the first attribute, then second, etc. The second line of the function gives the names of the input attributes, delimited by a comma. The last line gives the sizes of the respective input's scales, which are also integral (comma delimited).\n"
          "Any subsequent lines are interpreted as additional inputs to the constructed function, which can also be floats! These points are evaluated against the constructed interpolating function.\n"
          "Functions with one or two arguments are also displayed while evaluating!\n"
          "For exact syntax check the examples above.\n"
          "The app was developed using <a href=\"http://flask.pocoo.org/\">flask</a> for serving and GUI (integrating python scripts) and <a href=\"http://www.scipy.org/\">scipy</a> is used in the backend for constructing the interpolating functions (using splines) and evaluating the constructed functions. Previously, this was done using <a href=\"http://www.wolfram.com/mathematica/\">mathematica</a> and the functions is still in place. \n"
          "You can check the code and possibly contribute at <a href=\"https://github.com/nejctrdin/DEXiFunctionDerivatives\">github</a>.")

# examples put onto the page
# each example is a 2-tuple, firstly the description and then the function
_EXAMPLE1 = ("Linear in one variable", "012 first 3")
_EXAMPLE2 = ("Linear in two variables", "012123234 first,second 3,3")
_EXAMPLE3 = ("Monotone function", "000000001000111122112333344 first,second,third 3,3,3")
_EXAMPLE4 = ("Random function", "423120124321201212013024421 first,second,third 3,3,3")
_EXAMPLE5 = ("Large example", "333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333001001111122222222122122222222233233223223233233333333000000011011222222112112222222222222222222222223333333 v1,v2,v3,v4,v5,v6 2,2,3,3,2,3")
_EXAMPLE6 = ("Linear in two variables with inputs", "012123234 first,second 3,3 1.5,2 3.3,4")
_EXAMPLE7 = ("first*second + first", "0,0,0,0,0,0,0,0,0,0,1,2,3,4,5,6,7,8,9,10,2,4,6,8,10,12,14,16,18,20,3,6,9,12,15,18,21,24,27,30,4,8,12,16,20,24,28,32,36,40,5,10,15,20,25,30,35,40,45,50,6,12,18,24,30,36,42,48,54,60,7,14,21,28,35,42,49,56,63,70,8,16,24,32,40,48,56,64,72,80,9,18,27,36,45,54,63,72,81,90 first,second 10,10")
_EXAMPLE8 = ("Minimum of arguments", "0000001111012220123301234 first,second 5,5")
_EXAMPLE9 = ("Maximum of arguments", "0123411234222343333444444 first,second 5,5")
_EXAMPLE10 = ("Product of arguments", "0,0,0,0,0,0,1,2,3,4,0,2,4,6,8,0,3,6,9,12,0,4,8,12,16 first,second 5,5")
_EXAMPLE11 = ("first+second + 1.5", "1.5,2.5,2.5,3.5 first,second 2,2")
_EXAMPLE12 = ("first*second - second", "0,-1,-2,-3,-4,0,0,0,0,0,0,1,2,3,4,0,2,4,6,8,0,3,6,9,12 first,second 5,5")

# the joined examples
_EXAMPLES = [_EXAMPLE1, _EXAMPLE2, _EXAMPLE3, _EXAMPLE4, _EXAMPLE5, _EXAMPLE6,
             _EXAMPLE7, _EXAMPLE8, _EXAMPLE9, _EXAMPLE10, _EXAMPLE11, _EXAMPLE12]
