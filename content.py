_TITLE = "DEXi function to derivatives"
_SUBTITLE = "This is a web-service which enables the users to input a DEXi type function (rule-based), and receive back the values of the first (partial) derivatives in the defined points."
_GPL = ("Copyright (C) 2015  Nejc Trdin\n\n"
        "This program is free software: you can redistribute it and/or modify "
        "it under the terms of the GNU General Public License as published by "
        "the Free Software Foundation, either version 3 of the License, or "
        "(at your option) any later version.\n\n"

        "This program is distributed in the hope that it will be useful, "
        "but WITHOUT ANY WARRANTY; without even the implied warranty of "
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
        "GNU General Public License for more details.\n\n"

        "You should have received a copy of the GNU General Public License "
        "along with this program.  If not, see <http://www.gnu.org/licenses/>.")

_ABOUT = "This is an application which enables the users to input a DEXi type function, and produces the values of first partial derivatives in the function's defined points.\nThe functions is defined in three lines: the first line gives the integer output for the corresponding sorted input values. The inputs are sorted firstly by the first attribute, then second, etc. The second line of the function gives the names of the input attributes, delimited by a comma. The last line gives the sizes of the respective input's scales, which are also integral.\nYou can check the code and possibly contribute at <a href=\"https://github.com/nejctrdin/DEXiFunctionDerivatives\">github</a>."

_EXAMPLE1 = ("Linear in one variable", "012 first 3")
_EXAMPLE2 = ("Linear in two variables", "012123234 first,second 3,3")
_EXAMPLE3 = ("Monotone function", "000000001000111122112333344 first,second,third 3,3,3")


_EXAMPLES = [_EXAMPLE1, _EXAMPLE2, _EXAMPLE3]
