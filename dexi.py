import matplotlib
matplotlib.use("Agg")
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from itertools import product
#from subprocess import check_output
from scipy.misc import derivative
import random
import string
import os

# different error statuses given back to the user in case of problems
NOT_CORRECT_LINES = "Function should be represented in at least 3 lines!"
NOT_NUMBER_MULTIPLICITIES_ARG = ("Number of function arguments ({0}) and number "
                                 "of multiplicities ({1}) should be equal!")
MULTIPLICITIES_INT = "Multiplicities should be integers! Muliplicity {0} is not!"
INPUT_OUTPUT_NOT_MATCHING = ("The input space size ({0}) does not match output "
                             "space size ({1})!")
FUNCTION_OUTPUT_FLOAT = "All function outputs should be floats!"
FUNCTION_EVALUATIONS_FLOAT = "All function evaluations should be floats {0}!"
PROBLEM_DERIVATIVES = "There was a problem constructing derivatives!"
NOT_CORRECT_ARGUMENTS_EVAL = "Number of function arguments ({0}) does not match number of supplied evaluation arguments ({1}) - {2}."

DEFAULT_IMAGE_PATH = "/home/nejctrdin/DFD/static/images/"

def parse_function(f_rep):
    # the function that parses the input string

    # removing the \r chars and splitting the function by new lines
    f_rep = f_rep.replace("\r", "")
    lines = f_rep.split("\n")

    split = []
    for line in lines:
        if line != "":
            split.append(line)
    
    if len(split) < 3:
        # function must be at least three lines long
        return None, None, None, False, NOT_CORRECT_LINES

    function_outputs = split[0]
    if "," in function_outputs:
        # see if function outputs are comma delimited
        function_outputs = function_outputs.split(",")

    # get the output size, arguments and multiplicities
    output_size = len(function_outputs)
    arguments = split[1].replace(" ","").split(",")
    multip = split[2].replace(" ","").split(",")

    # test that function outputs can be cast to integers
    for output in function_outputs:
        try:
            float(output)
        except:
            return None, None, None, False, FUNCTION_OUTPUT_FLOAT
           
    # test that length of arguments is the same as the length of the multiplicities
    if len(arguments) != len(multip):
        return None, None, None, False, NOT_NUMBER_MULTIPLICITIES_ARG.format(len(arguments), len(multip))

    # check that multiplicities can be cast to integers
    i = 1
    for mutiplicity in multip:
        try:
            int(mutiplicity)
        except:
            return None, None, None, False, MULTIPLICITIES_INT.format(i)
        i+=1

    # get the input space from the multiplicities
    input_sizes = map(int, multip)
    input_size = reduce(lambda x,y: x*y, input_sizes)

    # check that input space matches the size of the output space
    if input_size != output_size:
        return None, None, None, False, INPUT_OUTPUT_NOT_MATCHING.format(input_size, output_size)

    # possible evaluations
    req_evaluations = []
    if len(split) > 3:
        # iterate over all evaluations appearing after the third line
        for e in split[3:]:
            # split them
            evaluation = e.replace(" ","").split(",")

            # see if the length is the same as the length of arguments
            if len(evaluation) != len(arguments):
                return None, None, None, False, NOT_CORRECT_ARGUMENTS_EVAL.format(len(arguments), len(evaluation), map(str, evaluation))

            for e in evaluation:
                # check that the evaluations can be cast to floats
                try:
                    float(e)
                except:
                    return None, None, None, False, FUNCTION_EVALUATIONS_FLOAT.format(map(str,evaluation))

            # finally add them to the list
            req_evaluations.append(evaluation)

    # create the input space
    input_space = [xrange(size) for size in input_sizes]

    # define the function
    function = []
    i = 0
    for point in product(*input_space):
        tmp = [point, float(function_outputs[i])]
        function.append(tmp)
        i += 1

    # return the function, arguments, requested evaluations, status and message
    return function, arguments, req_evaluations, True, ""

def _scipy_derivatives(function, req_evaluations, arguments, output_image=True):
    # the function expects a correct form of a function as parsed above and evaluation points
    # then it constructs an interpolating function using scipy interpolate utility, parses the
    # results and returns them

    # input size (number of arguments) and number of points
    input_size = len(function[0][0])
    # size of the function
    defined_points_size = len(function)

    # get the multiplicities of the arguments
    max_values = [-1] * input_size
    for point, output in function:
        for i in xrange(len(point)):
            max_values[i] = max(max_values[i], point[i])

    # create the space for the function inputs
    space = [np.array(xrange(max_val + 1)) for max_val in max_values]
    fun = []

    # create the mesh for function inputs
    for point, output in function:
        current = fun
        for i in xrange(len(point)):
            if len(current) - 1 < point[i]:
                current.append([])
            current = current[point[i]]
        current.append(output)
    data = np.array(fun)

    # create the interpolating spline
    interpolating = RegularGridInterpolator(tuple(space),
            data,
            bounds_error=False,
            fill_value=None
    )

    # an inline function for computing partial derivatives
    def partial_derivative(func, var=0, point=[]):
        args = point[:]
        def wraps(x):
            args[var] = x
            return func(args)
        return derivative(wraps, point[var], dx=1e-6)

    # list of derivatives
    derivatives = []
    SUM = 0.0
    N = 0
    for i in xrange(input_size):
        for point, _ in function:
            # add the derivatives
            d = partial_derivative(interpolating, i, list(point))[0][0]
            derivatives.append(_format_number(d))
            SUM += d
            N+=1
        # finally add the average
        derivatives.append(_format_number(SUM/N))
        SUM = 0.0
        N = 0

    # fill the required evaluations
    evaluations = []
    for ev in req_evaluations:
        e = interpolating(map(float, ev))[0][0]
        evaluations.append((ev, _format_number(e)))

    # create the filename for the possible image
    image_file_name = ""
    image_dir = DEFAULT_IMAGE_PATH

    if input_size < 3:
        # we create a list of possible characters that form the file names
        _possible_chars = string.ascii_letters + string.digits
        # we can draw an image if there are 1 or 2 arguments
        _image_file_name_len = 10
        # create a file name, that is not present in the directory
        image_file_name = "dexi.py"
        while os.path.isfile(image_file_name):
            image_file_name = "".join([image_dir] + [random.choice(_possible_chars) for _ in xrange(_image_file_name_len)] + [".png"])

        if input_size == 1:
            # if input size is 1, we have a 2D image
            fig = plt.figure()
            X = np.arange(-1, max_values[0] + 1.1, 0.1)
            ax = fig.add_subplot(111)
            ax.set_xlabel(arguments[0])
            ax.set_ylabel("Output")

            Y = []
            for x in X:
                Y.append(interpolating([x])[0][0])
            plt.plot(X, Y)
            if output_image:
                plt.savefig(image_file_name)
        else:
            # otherwise we have a 3D image
            fig = plt.figure()
            ax = fig.gca(projection="3d")
            X = np.arange(-1, max_values[0] + 1.1, 0.1)
            Y = np.arange(-1, max_values[1] + 1.1, 0.1)
            X, Y = np.meshgrid(X, Y)
            ax.set_xlabel(arguments[0])
            ax.set_ylabel(arguments[1])
            ax.set_zlabel("Output")
            ax.view_init(azim=-160)
            Z = []
            for i in xrange(len(X)):
                current = []
                for j in xrange(len(X[i])):
                    x = X[i][j]
                    y = Y[i][j]
                    current.append(interpolating([x, y])[0][0])
                Z.append(current)
            surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                                   linewidth=0.1, antialiased=True,
                                   shade=True, cmap=cm.jet)
            if output_image:
                plt.savefig(image_file_name)

    # return the derivatives, evaluations, and image file name
    return derivatives, evaluations, image_file_name.replace(image_dir, "")

def _format_number(num):
    # a function that formats a number as string with two digits after dot
    return "{0:.2f}".format(num)

def get_derivatives(function, req_evaluations, arguments, output_image=True):
    # the function which calls the interior function of this file
    derivatives, evaluations, image_file_name = _scipy_derivatives(function, req_evaluations, arguments, output_image)

    # depracated function which does the derivative processing in mathematica
    # derivatives, evaluations, image_file_name = _mathematica_derivatives(function, req_evaluations)

    return derivatives, evaluations, image_file_name, True, ""

def create_2argument_function(mul_f, mul_s, function):
    # function creates a by-point-defined function of 2 arguments with
    # multiplicities of the first and the second argument given
    # also the function expects a function which is applicable on two arguments

    # check if multiplicities are above 0
    if mul_f < 1:
        raise ValueError("Multiplicity of the first attribute must be more than 0.")

    if mul_s < 1:
        raise ValueError("Multiplicity of the second attribute must be more than 0.")

    # create iterators and apply function
    function_values = []
    for i in xrange(mul_f):
        for j in xrange(mul_s):
            function_values.append(str(function(i, j)))

    # format the function as per specification
    output = []
    output.append(",".join(function_values))
    output.append("first,second")
    output.append(",".join([str(mul_f), str(mul_s)]))

    # return the string representation of the function
    return " ".join(output)
