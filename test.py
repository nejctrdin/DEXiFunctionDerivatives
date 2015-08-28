import unittest
import dexi
import os
import string
import content
import server
import re

class TestDexi(unittest.TestCase):

    _EMPTY_FUNCTION = ""
    _INCORRECT_EVAL_ARGS = "012\nf\n3\n1,2"
    _INCORRECT_EVAL_ARGS_TYPE = "012\nf\n3\na"
    _INCORRECT_FUN_OUTPUT = "a12\nf\n3"
    _INCORRECT_MULTIPLICITIES = "012012123\nf,s\n4,3,3"
    _INCORRECT_MULTIPLICITIES_TYPE = "012012123\nf,s\n4,3a"
    _INCORRECT_N_INPUT_OUTPUT = "012012123\nf,s\n4,3"
    _SMALL_TEST = "0,1,2\nf\n3\n1\n2\n3"
    _MEDIUM_TEST = "012123234\nf,s\n3,3\n1,1\n2,2\n3,3.5"
    _LARGE_TEST = "423120124321201212013024421\nf,s,t\n3,3,3\n1,2,3\n0.1,0.2,0.3"
    _LARGE_TEST_NEWLINE = "423120124321201212013024421\n\n\nf,s,t\n\n3,3,3\n\n1,2,3\n\n0.1,0.2,0.3"
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

        derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations, arguments, False)
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

        derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations, arguments, False)
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

        derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations, arguments)
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

    def test_large_newlines(self):
        # large test case with newlines
        function, arguments, evaluations, success, message = dexi.parse_function(self._LARGE_TEST_NEWLINE)
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

        derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations, arguments)
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
        self.assertRaisesRegexp(ValueError, "Multiplicity of the first attribute must be more than 0.",
                                dexi.create_2argument_function, -1, 5, None)

        self.assertRaisesRegexp(ValueError, "Multiplicity of the second attribute must be more than 0.",
                                dexi.create_2argument_function, 2, -1, None)

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

    def test_formatting(self):
        formatted = dexi._format_number(1.5)
        self.assertEqual(formatted, "1.50")

        formatted = dexi._format_number(2)
        self.assertEqual(formatted, "2.00")

        formatted = dexi._format_number(1.55555)
        self.assertEqual(formatted, "1.56")

        self.assertRaises(ValueError, dexi._format_number, "foo")

    def test_content_examples(self):
        for description, example in content._EXAMPLES:
            inp_line = example.replace(" ", "\n")
            self.assertNotEqual(description, "")

            function, arguments, evaluations, success, message = dexi.parse_function(inp_line)

            self.assertNotEqual(function, [])
            for point, output in function:
                for arg in point:
                    self.assertTrue(type(arg) is int)
                self.assertTrue(type(output) is float)

            self.assertNotEqual(arguments, [])
            for arg in arguments:
                self.assertNotEqual(arg, "")

            if evaluations:
                for evaluation in evaluations:
                    for point in evaluation:
                        self.assertTrue(type(point) is str)
                        self.assertTrue(type(float(point)) is float)
            self.assertEqual(success, True)
            self.assertEqual(message, "")

            derivatives, evals, image, success, message = dexi.get_derivatives(function, evaluations, arguments, False)

            self.assertEqual(len(derivatives), (len(function) + 1)*len(arguments))

            for derivative in derivatives:
                self.assertTrue(type(derivative) is str)
                self.assertTrue(type(float(derivative)) is float)

            if evaluations:
                self.assertNotEqual(evals, [])
                for point, evaluation in evals:
                    self.assertEqual(len(point), len(arguments))
                    for p in point:
                        self.assertTrue(type(p) is str)
                        self.assertTrue(type(float(p)) is float)
                    self.assertTrue(type(evaluation) is str)
                    self.assertTrue(type(float(evaluation)) is float)

            if len(arguments) < 3:
                self.assertRegexpMatches(image, "[a-zA-Z0-9]{10}\.png")
            else:
                self.assertEqual(image, "")

            self.assertEqual(success, True)
            self.assertEqual(message, "")


class ServerTest(unittest.TestCase):
    
    _QUERY_SMALL = "123\nf\n3"

    def setUp(self):
        self.app = server.app.test_client()
        server.app.config["TESTING"] = True
        server.app.config["DEBUG"] = True
        content._DEFAULT_IMAGE_PATH = ""

    def test_content(self):
        self.assertIn("DEVELOPMENT", content._TITLE)
        self.assertIn("DEX", content._TITLE)
        self.assertIn("General Public License", content._GPL)
        self.assertNotEqual(content._ABOUT, "")
        self.assertNotEqual(content._SUBTITLE, "")

    def test_root(self):
        result = self.app.get("/")
        self.assertEqual(result.status, "200 OK")
        data = result.data

        for line in content._TITLE.split("\n"):
            self.assertIn(line, data)

        for line in content._SUBTITLE.split("\n"):
            self.assertIn(line, data)

        for line in content._GPL.split("\n"):
            self.assertIn(line, data)

        for line in content._ABOUT.split("\n"):
            self.assertIn(line, data)

        for description, example in content._EXAMPLES:
            self.assertIn(description, data)
            for line in example.split(" "):
                self.assertIn(line, data)

    def test_nonexistent(self):
        result = self.app.get("/foo")
        self.assertEqual(result.status, "404 NOT FOUND")
        
        result = self.app.get("/bar")
        self.assertEqual(result.status, "404 NOT FOUND")
        
        result = self.app.get("/123")
        self.assertEqual(result.status, "404 NOT FOUND")

    def test_not_allowed(self):
        result = self.app.get("/get_derivatives")
        self.assertEqual(result.status, "405 METHOD NOT ALLOWED")

        result = self.app.get("/get_animation")
        self.assertEqual(result.status, "405 METHOD NOT ALLOWED")

    def test_incorrect_input(self):
        result = self.app.post("/get_derivatives")
        self.assertIn("Could not parse input! Unsupported operation!", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "123"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! Function should be represented in at least 3 lines!", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "123\n\n"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! Function should be represented in at least 3 lines!", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "123\n1,2,3\n"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! Function should be represented in at least 3 lines!", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "123\nf,s\n2"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! Number of function arguments (2) and number of multiplicities (1) should be equal!", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "123\nf,s\n2,3"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! The input space size (6) does not match output space size (3)!", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "1234567\nf,s\n2,3"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! The input space size (6) does not match output space size (7)!", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "12345,60\nf,s\n2,3"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! The input space size (6) does not match output space size (2)!", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "123456\nf,s\n2,3\n1,2,3"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! Number of function arguments (2) does not match number of supplied evaluation arguments (3)", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "123456\nf,s\n2,3\n1"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! Number of function arguments (2) does not match number of supplied evaluation arguments (1)", result.data)
        self.assertEqual(result.status, "200 OK")

        query = {"function": "123456\nf,s\n2,3.5"}
        result = self.app.post("/get_derivatives", data=query)
        self.assertIn("Could not parse input! Multiplicities should be integers! Muliplicity 2 is not!", result.data)
        self.assertEqual(result.status, "200 OK")

    def test_derivatives_small_custom(self):
        query = {"function": self._QUERY_SMALL}
        
        result = self.app.post("/get_derivatives", data=query)
        data = result.data

        self.assertEqual(result.status, "200 OK")

        for line in content._TITLE.split("\n"):
            self.assertIn(line, data)

        for line in content._SUBTITLE.split("\n"):
            self.assertIn(line, data)

        for line in content._GPL.split("\n"):
            self.assertIn(line, data)

        for line in content._ABOUT.split("\n"):
            self.assertIn(line, data)

        self.assertIn("<h1>Tabelaric Function and Derivatives</h1>", data)
        self.assertIn("<h1>Function Image</h1>", data)
        self.assertNotIn("<h1>Function Animation</h1>", data)
        self.assertIn("<th>Average</th>", data)

        m = re.search("[A-Za-z0-9]{10}\.png", data)
        png_file = m.group(0)
        self.assertTrue(os.path.isfile(png_file))
        os.remove(png_file)

    def test_derivatives_small_dynamic(self):
        query = {"names": "f,s",
                 "multiplicity": "2,2",
                 "v0": 0,
                 "v1": 1,
                 "v2": 2,
                 "v3": 3}
        
        result = self.app.post("/get_derivatives", data=query)
        data = result.data

        self.assertEqual(result.status, "200 OK")

        for line in content._TITLE.split("\n"):
            self.assertIn(line, data)

        for line in content._SUBTITLE.split("\n"):
            self.assertIn(line, data)

        for line in content._GPL.split("\n"):
            self.assertIn(line, data)

        for line in content._ABOUT.split("\n"):
            self.assertIn(line, data)

        self.assertIn("<h1>Tabelaric Function and Derivatives</h1>", data)
        self.assertIn("<h1>Function Image</h1>", data)
        self.assertIn("<h1>Function Animation</h1>", data)
        self.assertIn("<th>Average</th>", data)

        m = re.search("[A-Za-z0-9]{10}\.png", data)
        png_file = m.group(0)
        self.assertTrue(os.path.isfile(png_file))
        os.remove(png_file)

    def test_animation(self):
        query = {"names": "f,s",
                 "multiplicity": "2,2",
                 "v0": 0,
                 "v1": 1,
                 "v2": 2,
                 "v3": 3}
        
        result = self.app.post("/get_animation", data=query)
        data = result.data

        self.assertEqual(result.status, "200 OK")
        self.assertRegexpMatches(data, "[A-Za-z0-9]{10}\.gif")
        self.assertTrue(os.path.isfile(data))
        os.remove(data)

    def test_animation_error(self):
        query = {}
        result = self.app.post("/get_animation", data=query)
        self.assertEqual(result.status, "200 OK")
        data = result.data
        self.assertEqual(data, "Cannot create function animation. Missing arguments in request.")

        query = {"names": "f,s",
                 "multiplicity": "2,2",
                 "v0": 0,
                 "v1": 1,
                 "v2": 2}
        result = self.app.post("/get_animation", data=query)
        self.assertEqual(result.status, "200 OK")
        data = result.data
        self.assertEqual(data, "Could not parse function! The input space size (4) does not match output space size (3)!")

    def test_derivatives_content_examples(self):
        for _, example in content._EXAMPLES:
            function = example.replace(" ", "\n")
            query = {"function": function}

            result = self.app.post("/get_derivatives", data=query)
            data = result.data
            self.assertEqual(result.status, "200 OK")

            for line in content._TITLE.split("\n"):
                self.assertIn(line, data)

            for line in content._SUBTITLE.split("\n"):
                self.assertIn(line, data)

            for line in content._GPL.split("\n"):
                self.assertIn(line, data)

            for line in content._ABOUT.split("\n"):
                self.assertIn(line, data)

            self.assertIn("<h1>Tabelaric Function and Derivatives</h1>", data)
            if len(function.split("\n")[1].split(",")) < 3:
                self.assertIn("<h1>Function Image</h1>", data)
                m = re.search("[A-Za-z0-9]{10}\.png", data)
                png_file = m.group(0)
                self.assertTrue(os.path.isfile(png_file))
                os.remove(png_file)

                if len(function.split("\n")[1].split(",")) == 2:
                    self.assertIn("<h1>Function Animation</h1>", data)
                else:
                    self.assertNotIn("<h1>Function Animation</h1>", data)
            else:
                self.assertNotIn("<h1>Function Image</h1>", data)
                self.assertNotIn("<h1>Function Animation</h1>", data)

            self.assertIn("<th>Average</th>", data)

            if len(function.split("\n")) > 3:
                self.assertIn("<h1>Function Evaluations</h1>", data)


if __name__ == "__main__":
    unittest.main()
