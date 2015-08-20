import unittest
import dexi
import os

class TestDexi(unittest.TestCase):

    _EMPTY_FUNCTION = ""
    _INCORRECT_EVAL_ARGS = "012\nf\n3\n1,2"
    _INCORRECT_EVAL_ARGS_TYPE = "012\nf\n3\na"
    _INCORRECT_FUN_OUTPUT = "a12\nf\n3"
    _INCORRECT_MULTIPLICITIES = "012012123\nf,s\n4,3,3"
    _INCORRECT_MULTIPLICITIES_TYPE = "012012123\nf,s\n4,3a"
    _INCORRECT_N_INPUT_OUTPUT = "012012123\nf,s\n4,3"
    _SMALL_TEST = "012\nf\n3\n1\n2\n3"
    _MEDIUM_TEST = "012123234\nf,s\n3,3\n1,1\n2,2\n3,3.5"
    _LARGE_TEST = "423120124321201212013024421\nf,s,t\n3,3,3\n1,2,3\n0.1,0.2,0.3"

    def test_empty(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._EMPTY_FUNCTION)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "Function should be represented in at least 3 lines!")

    def test_eval_arguments(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_EVAL_ARGS)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "Number of function arguments (1) does not match number of supplied evaluation arguments (2) - ['1', '2'].")

    def test_eval_arguments_type(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_EVAL_ARGS_TYPE)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "All function evaluations should be floats ['a']!")

    def test_func_output_type(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_FUN_OUTPUT)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "All function outputs should be integers!")

    def test_multiplicities(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_MULTIPLICITIES)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "Number of function arguments (2) and number of multiplicities (3) should be equal!")

    def test_multiplicities_type(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_MULTIPLICITIES_TYPE)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "Multiplicities should be integers! Muliplicity 2 is not!")

    def test_input_output_size(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_N_INPUT_OUTPUT)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "The input space size (12) does not match output space size (9)!")

    def test_small(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._SMALL_TEST)
        self.assertEqual(function, [[(0,), 0], [(1,), 1], [(2,), 2]])
        self.assertEqual(arguments, ["f"])
        self.assertEqual(evaluations, [["1"], ["2"], ["3"]])
        self.assertEqual(success, True)
        self.assertEqual(message, "")

        derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations)
        self.assertEqual(derivatives, ["1.00"] * 4);
        self.assertEqual(evals, [(["1"], "1.0"), (["2"], "2.0"), (["3"], "3.0")])
        self.assertNotEqual(image, "")
        self.assertRegexpMatches(image, "[A-Za-z0-9]+.png")
        self.assertEqual(success, True)
        self.assertEqual(message, "")
        os.remove("".join(["static/images/", image]))

    def test_medium(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._MEDIUM_TEST)
        self.assertEqual(function, [[(0, 0), 0], [(0, 1), 1], [(0, 2), 2], [(1, 0), 1], [(1, 1), 2],
                                    [(1, 2), 3], [(2, 0), 2], [(2, 1), 3], [(2, 2), 4]])
        self.assertEqual(arguments, ["f", "s"])
        self.assertEqual(evaluations, [["1", "1"], ["2", "2"], ["3", "3.5"]])
        self.assertEqual(success, True)
        self.assertEqual(message, "")

        derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations)
        self.assertEqual(derivatives, ["1.00"] * 20);
        self.assertEqual(evals, [(["1", "1"], "2.0"), (["2", "2"], "4.0"), (["3", "3.5"], "6.5")])
        self.assertNotEqual(image, "")
        self.assertRegexpMatches(image, "[A-Za-z0-9]+.png")
        self.assertEqual(success, True)
        self.assertEqual(message, "")
        os.remove("".join(["static/images/", image]))

    def test_large(self):
        function, arguments, evaluations, success, message = dexi.parse_function(self._LARGE_TEST)
        self.assertEqual(function, [[(0, 0, 0), 4], [(0, 0, 1), 2], [(0, 0, 2), 3], [(0, 1, 0), 1], [(0, 1, 1), 2],
                                    [(0, 1, 2), 0], [(0, 2, 0), 1], [(0, 2, 1), 2], [(0, 2, 2), 4], [(1, 0, 0), 3],
                                    [(1, 0, 1), 2], [(1, 0, 2), 1], [(1, 1, 0), 2], [(1, 1, 1), 0], [(1, 1, 2), 1],
                                    [(1, 2, 0), 2], [(1, 2, 1), 1], [(1, 2, 2), 2], [(2, 0, 0), 0], [(2, 0, 1), 1],
                                    [(2, 0, 2), 3], [(2, 1, 0), 0], [(2, 1, 1), 2], [(2, 1, 2), 4], [(2, 2, 0), 4],
                                    [(2, 2, 1), 2], [(2, 2, 2), 1]])
        self.assertEqual(arguments, ["f", "s", "t"])
        self.assertEqual(evaluations, [["1", "2", "3"], ["0.1", "0.2", "0.3"]])
        self.assertEqual(success, True)
        self.assertEqual(message, "")

        derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations)
        self.assertEqual(derivatives, ["0.00", "0.50", "-4.00", "2.50", "-4.00", "0.00", "0.50", "-2.00", "-2.50",
                                       "-2.00", "-0.50", "0.00", "-0.50", "0.00", "2.00", "1.50", "0.00", "-1.50",
                                       "-4.00", "-1.50", "4.00", "-3.50", "4.00", "4.00", "2.50", "2.00", "-0.50",
                                       "-0.11", "-4.50", "0.00", "-6.50", "-1.50", "0.00", "0.50", "1.50", "0.00",
                                       "7.50", "-1.50", "-3.50", "-0.50", "-0.50", "-0.50", "0.50", "0.50", "2.50",
                                       "1.50", "-2.00", "1.50", "3.00", "2.00", "0.50", "-1.00", "6.00", "-0.50",
                                       "-5.00", "0.00", "-3.50", "-0.50", "2.50", "2.50", "-0.50", "-3.50", "0.50",
                                       "1.50", "2.50", "-1.00", "-1.00", "-1.00", "-3.50", "-0.50", "2.50", "-2.00",
                                       "0.00", "2.00", "0.50", "1.50", "2.50", "2.00", "2.00", "2.00", "-2.50",
                                       "-1.50", "-0.50", "0.11"])
        self.assertEqual(evals, [(["1", "2", "3"], "5.0"), (["0.1", "0.2", "0.3"], "2.73124")])
        self.assertEqual(image, "")
        self.assertEqual(success, True)
        self.assertEqual(message, "")

    def test_error_2argument(self):
        self.assertRaisesRegexp(
                ValueError,
                "Multiplicity of the first attribute must be more than 0.",
                dexi.create_2argument_function, -1, 5, None)
        self.assertRaisesRegexp(
                ValueError,
                "Multiplicity of the second attribute must be more than 0.",
                dexi.create_2argument_function, 2, -1, None)
        self.assertRaises(TypeError, dexi.create_2argument_function, 1, 5, None)

        self.assertRaises(TypeError, dexi.create_2argument_function, 1, 5, lambda x: x)

        self.assertRaises(TypeError, dexi.create_2argument_function, 1, 5, lambda x,y,z: x + y + z)

    def test_2argument(self):
        func = dexi.create_2argument_function(2, 2, min)
        self.assertEqual(func, "0,0,0,1 first,second 2,2")

        func = dexi.create_2argument_function(2, 2, max)
        self.assertEqual(func, "0,1,1,1 first,second 2,2")

        func = dexi.create_2argument_function(2, 2, lambda x,y: x + y)
        self.assertEqual(func, "0,1,1,2 first,second 2,2")

        func = dexi.create_2argument_function(2, 2, lambda x,y: x * y)
        self.assertEqual(func, "0,0,0,1 first,second 2,2")


if __name__ == "__main__":
    unittest.main()
