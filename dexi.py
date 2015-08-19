from itertools import product
from subprocess import check_output
import random
import string
import os.path
import os

NOT_CORRECT_LINES = "Function should be represented in at least 3 lines!"
NOT_NUMBER_MULTIPLICITIES_ARG = ("Number of function arguments ({0}) and number "
                                 "of multiplicities ({1}) should be equal!")
MULTIPLICITIES_INT = "Multiplicities should be integers! Muliplicity {0} is not!"
INPUT_OUTPUT_NOT_MATCHING = ("The input space size ({0}) does not match output "
                             "space size ({1})!")
FUNCTION_OUTPUT_INT = "All function outputs should be integers!"
FUNCTION_EVALUATIONS_FLOAT = "All function evaluations should be floats {0}!"
PROBLEM_DERIVATIVES = "There was a problem constructing derivatives!"
NOT_CORRECT_ARGUMENTS_EVAL = "Number of function arguments ({0}) does not match number of supplied evaluation arguments ({1}) - {2}."

def parse_function(f_rep):
    f_rep = f_rep.replace("\r", "")
    split = f_rep.split("\n")
    
    if len(split) < 3:
        return None, None, None, False, NOT_CORRECT_LINES

    function_outputs = split[0]
    output_size = len(function_outputs)
    arguments = split[1].replace(" ","").split(",")
    multip = split[2].replace(" ","").split(",")

    req_evaluations = [] 
    if len(split) > 3:
        for e in split[3:]:
            evaluation = e.replace(" ","").split(",")
            if len(evaluation) != len(arguments):
                return None, None, None, False, NOT_CORRECT_ARGUMENTS_EVAL.format(len(arguments), len(evaluation), map(str, evaluation))

            for e in evaluation:
                try:
                    float(e)
                except:
                    return None, None, None, False, FUNCTION_EVALUATIONS_FLOAT.format(map(str,evaluation))

            req_evaluations.append(evaluation)

    for output in function_outputs:
        try:
            int(output)
        except:
            return None, None, None, False, FUNCTION_OUTPUT_INT
            
    if len(arguments) != len(multip):
        return None, None, None, False, NOT_NUMBER_MULTIPLICITIES_ARG.format(len(arguments), len(multip))
    
    i = 1
    for mutiplicity in multip:
        try:
            int(mutiplicity)
        except:
            return None, None, None, False, MULTIPLICITIES_INT.format(i)
        i+=1

    input_sizes = map(int, multip)
    input_size = reduce(lambda x,y: x*y, input_sizes)
    
    if input_size != output_size:
        return None, None, None, False, INPUT_OUTPUT_NOT_MATCHING.format(input_size, output_size)

    input_space = [xrange(size) for size in input_sizes]

    function = []
    i = 0
    for point in product(*input_space):
        tmp = [point, int(function_outputs[i])]
        function.append(tmp)
        i += 1

    return function, arguments, req_evaluations, True, ""

def _mathematica_derivatives(function, req_evaluations):
    input_size = len(function[0][0])
    defined_points_size = len(function)

    contents = []
    out_index = 1
    problem_rep = "func=Interpolation[{{{0}}}]"
    format_eval = "N[d{{0}}[{0}]]"

    evaluations = []
    points = []
    for point in function:
        inputs = ",".join(map(str, point[0]))
        output = str(point[1])
        points.append("{{{{{0}}},{1}}}".format(inputs, output))
        evaluations.append(format_eval.format(inputs))
    joined = ",".join(points)
    problem = problem_rep.format(joined)
    contents.append(problem)
    out_index += 1

    arguments = [chr(ord("a") + i) for i in xrange(input_size)]
    formatted_args = ",".join(arguments)

    contents.append("eval=Function[{{{0}}},func[{0}]]".format(formatted_args))
    out_index += 1

    for arg in arguments:
        derivative = "d{1}=Function[{{{0}}},Evaluate[D[eval[{0}],{1}]]]".format(formatted_args, arg)
        contents.append(derivative)
        out_index += 1

    for arg in arguments:
        for evaluation in evaluations:
            contents.append(evaluation.format(arg))

    func_eval_prot = "eval[{0}]"
    for req_eval in req_evaluations:
        contents.append(func_eval_prot.format(",".join(req_eval)))

    _file_name_len = 10
    _possible_chars = string.ascii_letters + string.digits
    file_name = "".join([random.choice(_possible_chars) for _ in xrange(_file_name_len)] + [".m"])
    while os.path.isfile(file_name):
        file_name = "".join([random.choice(_possible_chars) for _ in xrange(_file_name_len)] + [".m"])
    _file = file(file_name, "w")
    for line in contents:
        _file.write(line)
        _file.write("\n")
    _file.close()
    out = check_output("math -script < {0}".format(file_name), shell=True)   
    os.remove(file_name)
    
    derivatives = []
    proto = "Out[{0}]= "
    actual = proto.format(out_index)
    computed = 0
    sum_computed = 0.0
    found = 0
    expected = len(arguments) * len(function)
    finished_derivatives = False
    evals = []
    for line in out.split("\n"):
        if actual in line:
            computed += 1
            if found >= expected:
                evals.append(float(line.replace(actual, "")))
            else:
                found += 1
                derivative = float(line.replace(actual, ""))
                derivatives.append(_format_number(derivative))
                sum_computed += derivative
                if computed == defined_points_size:
                    derivatives.append(_format_number(sum_computed / defined_points_size))
                    computed = 0
                    sum_computed = 0.0
            out_index += 1
            actual = proto.format(out_index)

    evaluations = []
    for i in xrange(len(evals)):
        evaluations.append((req_evaluations[i], str(evals[i])))

    return derivatives, evaluations

def _format_number(num):
    return "{0:.2f}".format(num)

def get_derivatives(function, req_evaluations):
    derivatives, evaluations = _mathematica_derivatives(function, req_evaluations)
    if derivatives:
        return derivatives, evaluations, True, ""
    derivatives = [0] * (len(function) * len(function[0][0]))
    evaluations = [0] * len(req_evaluations)
    return derivatives, evaluations, False, PROBLEM_DERIVATIVES
