import unittest
import dexi
import os
import string

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
    _POSSIBLE_CHARS = string.ascii_letters + string.digits

    def test_empty(self):
        # test if empty function produces errors
        function, arguments, evaluations, success, message = dexi.parse_function(self._EMPTY_FUNCTION)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "Function should be represented in at least 3 lines!")

    def test_eval_arguments(self):
        # test if evaluation arguments have the same length as the inputs
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_EVAL_ARGS)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "Number of function arguments (1) does not match number of supplied evaluation arguments (2) - ['1', '2'].")

    def test_eval_arguments_type(self):
        # test if types of evaluation arguments can be cast to floats
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_EVAL_ARGS_TYPE)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "All function evaluations should be floats ['a']!")

    def test_func_output_type(self):
        # test if inputs to function can be cast to ints
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_FUN_OUTPUT)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "All function outputs should be floats!")

    def test_multiplicities(self):
        # test if the number of arguments matches the number of supplied multiplicities
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_MULTIPLICITIES)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "Number of function arguments (2) and number of multiplicities (3) should be equal!")

    def test_multiplicities_type(self):
        # test if multiplicities can be cast to integers
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_MULTIPLICITIES_TYPE)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "Multiplicities should be integers! Muliplicity 2 is not!")

    def test_input_output_size(self):
        # test if function output length is equal to the multiplied multiplicities
        function, arguments, evaluations, success, message = dexi.parse_function(self._INCORRECT_N_INPUT_OUTPUT)
        self.assertEqual(function, None)
        self.assertEqual(arguments, None)
        self.assertEqual(evaluations, None)
        self.assertEqual(success, False)
        self.assertEqual(message, "The input space size (12) does not match output space size (9)!")

    def test_small(self):
        # a small test case
        function, arguments, evaluations, success, message = dexi.parse_function(self._SMALL_TEST)
        self.assertEqual(function, [[(0,), 0], [(1,), 1], [(2,), 2]])
        self.assertEqual(arguments, ["f"])
        self.assertEqual(evaluations, [["1"], ["2"], ["3"]])
        self.assertEqual(success, True)
        self.assertEqual(message, "")

        derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations, False)
        self.assertEqual(derivatives, ["1.00"] * 4);
        self.assertEqual(evals, [(["1"], "1.00"), (["2"], "2.00"), (["3"], "3.00")])

        self.assertNotEqual(image, "")
        self.assertEqual(image[-4:], ".png")
        for c in image[:-4]:
            self.assertTrue(c in self._POSSIBLE_CHARS)

        self.assertEqual(success, True)
        self.assertEqual(message, "")

    def test_medium(self):
        # medium test case
        function, arguments, evaluations, success, message = dexi.parse_function(self._MEDIUM_TEST)
        self.assertEqual(function, [[(0, 0), 0], [(0, 1), 1], [(0, 2), 2], [(1, 0), 1], [(1, 1), 2],
                                    [(1, 2), 3], [(2, 0), 2], [(2, 1), 3], [(2, 2), 4]])
        self.assertEqual(arguments, ["f", "s"])
        self.assertEqual(evaluations, [["1", "1"], ["2", "2"], ["3", "3.5"]])
        self.assertEqual(success, True)
        self.assertEqual(message, "")

        derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations, False)
        self.assertEqual(derivatives, ["1.00"] * 20);
        self.assertEqual(evals, [(["1", "1"], "2.00"), (["2", "2"], "4.00"), (["3", "3.5"], "6.50")])
        self.assertNotEqual(image, "")

        self.assertEqual(image[-4:], ".png")
        for c in image[:-4]:
            self.assertTrue(c in self._POSSIBLE_CHARS)

        self.assertEqual(success, True)
        self.assertEqual(message, "")

    def test_large(self):
        # large test case
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
        self.assertEqual(derivatives, ["-1.00", "0.00", "-2.00", "1.00", "-2.00", "1.00", "1.00", "-1.00", "-2.00",
                                       "-2.00", "-0.50", "-0.00", "-0.50", "-0.00", "2.00", "1.50", "-0.00", "-1.50",
                                       "-3.00", "-1.00", "2.00", "-2.00", "2.00", "3.00", "2.00", "1.00", "-1.00",
                                       "-0.11", "-3.00", "0.00", "-3.00", "-1.50", "0.00", "0.50", "0.00", "0.00",
                                       "4.00", "-1.00", "-2.00", "0.00", "-0.50", "-0.50", "0.50", "0.00", "1.00",
                                       "1.00", "0.00", "1.00", "1.00", "2.00", "0.50", "-1.00", "4.00", "0.00",
                                       "-3.00", "0.00", "-2.00", "-0.50", "1.00", "1.00", "-0.50", "-2.00", "1.00",
                                       "1.50", "2.00", "-1.00", "-1.00", "-1.00", "-2.00", "-0.50", "1.00", "-1.00",
                                       "-0.00", "1.00", "1.00", "1.50", "2.00", "2.00", "2.00", "2.00", "-2.00",
                                       "-1.50", "-1.00", "0.11"])
        self.assertEqual(evals, [(["1", "2", "3"], "3.00"), (["0.1", "0.2", "0.3"], "2.93")])
        self.assertEqual(image, "")
        self.assertEqual(success, True)
        self.assertEqual(message, "")

    def test_error_2argument(self):
        # test if construction of a two argument function produces the expected errors
        try:
            dexi.create_2argument_function(-1, 5, None)
        except ValueError, message:
            self.failUnlessEqual(message.args[0], "Multiplicity of the first attribute must be more than 0.")
        else:
            self.fail("ValueError not raised")

        try:
            dexi.create_2argument_function(2, -1, None)
        except ValueError, message:
            self.failUnlessEqual(message.args[0], "Multiplicity of the second attribute must be more than 0.")
        else:
            self.fail("ValueError not raised")

        self.assertRaises(TypeError, dexi.create_2argument_function, 1, 5, None)

        self.assertRaises(TypeError, dexi.create_2argument_function, 1, 5, lambda x: x)

        self.assertRaises(TypeError, dexi.create_2argument_function, 1, 5, lambda x,y,z: x + y + z)

    def test_2argument(self):
        # test that we get the expected functions back
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
