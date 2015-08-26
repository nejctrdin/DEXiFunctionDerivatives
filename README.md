# DFD - DEXiFunctionDerivatives
This is an online application which enables the users to input a <a href="http://kt.ijs.si/MarkoBohanec/dexi.html">DEXi</a> type function, and produces the values of first partial derivatives in the function's defined points.

The functions is defined in three lines: the first line gives the float output for the corresponding sorted input values (the values can be concatenated together - as in *dxi* file - if they are all less than 10 and at least 0 and integer, otherwise they must be comma separated). The inputs are sorted firstly by the first attribute, then second, etc. The second line of the function gives the names of the input attributes, delimited by a comma. The last line gives the sizes of the respective input's scales, which are also integral.

Any subsequent lines are interpreted as additional inputs to the constructed function, which can also be floats!

Functions with one or two arguments are also displayed while evaluating!

The application uses *flask* to serve the web pages and does the needed preprocessing of the inputs. The derivatives of the supplied functions are interpolated with splines, using *scipy*, and the derivatives are also computed based on the interpolated function. Previously, the interpolation and computation of derivatives was done using *mathematica* - these were removed in commit 17f8e21006463275279b4f4490a6d86ea702043a.

You can check the code and possibly contribute at <a href="https://github.com/nejctrdin/DEXiFunctionDerivatives">github</a>.

## Build Status
[![Build Status](https://travis-ci.org/nejctrdin/DFD.svg?branch=develop)](https://travis-ci.org/nejctrdin/DFD)
[![Coverage Status](https://coveralls.io/repos/nejctrdin/DFD/badge.svg?branch=develop&service=github)](https://coveralls.io/github/nejctrdin/DFD?branch=develop)

## Prerequisites
To run the server you need <a href="http://flask.pocoo.org/">flask</a> and at least <a href="http://www.scipy.org/">scipy 0.14</a>. If you wish to use the mathematica backend, you need <a href="http://www.wolfram.com/mathematica/">mathematica</a> installed (specifically, `math` must be in your path).

## Usage

```bash
python server.py [port|license]
```

Then go to `localhost:5000` and input the desired function, for which you require the derivatives.

You can also run it using *gunicorn* for paralell execution.

```bash
gunicorn server:app -w workers -b address:port server:app
```

## License

```
Copyright (C) 2015  Nejc Trdin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
```
