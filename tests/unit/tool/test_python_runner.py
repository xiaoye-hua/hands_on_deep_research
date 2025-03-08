import unittest
from unittest.mock import patch
import sys
import io
from src.tool.python_runner import PythonRunner

class TestPythonRunner(unittest.TestCase):
    
    def setUp(self):
        self.python_runner = PythonRunner()
    
    def test_initialization(self):
        """Test the initialization of PythonRunner"""
        self.assertEqual(self.python_runner.name, "python_runner")
        self.assertEqual(self.python_runner.description, "Run a python script")
        # Check if parameters is correctly defined
        self.assertTrue(hasattr(self.python_runner, "parameters"))
        self.assertIn("code", self.python_runner.parameters)
    
    def test_run_without_code(self):
        """Test run method with no code provided"""
        with self.assertRaises(ValueError) as context:
            self.python_runner.run({})
        self.assertEqual(str(context.exception), "No code provided")
    
    def test_successful_execution(self):
        """Test successful execution of code"""
        code = 'print("Hello, World!")'
        result = self.python_runner.run({"code": code})
        # Check that the function returns a dictionary
        self.assertIsInstance(result, dict)
        self.assertIn("output", result)
        self.assertEqual(result["output"], "Hello, World!\n")
    
    def test_execution_error(self):
        """Test error handling during execution"""
        code = 'x = 1/0'  # Division by zero error
        with self.assertRaises(ValueError) as context:
            self.python_runner.run({"code": code})
        self.assertIn("Error running code: division by zero", str(context.exception))
    
    def test_execution_with_variables(self):
        """Test execution with variables and more complex code"""
        code = """
a = 10
b = 20
c = a + b
print(f"The sum of {a} and {b} is {c}")
"""
        result = self.python_runner.run({"code": code})
        self.assertIn("output", result)
        self.assertEqual(result["output"], "The sum of 10 and 20 is 30\n")
    
    def test_execution_with_multiple_prints(self):
        """Test execution with multiple print statements"""
        code = """
print("Line 1")
print("Line 2")
print("Line 3")
"""
        result = self.python_runner.run({"code": code})
        self.assertIn("output", result)
        expected_output = "Line 1\nLine 2\nLine 3\n"
        self.assertEqual(result["output"], expected_output)
    
    def test_execution_with_import(self):
        """Test execution with import statement"""
        code = """
import math
print(f"The value of pi is approximately {math.pi:.2f}")
"""
        result = self.python_runner.run({"code": code})
        self.assertIn("output", result)
        self.assertEqual(result["output"], "The value of pi is approximately 3.14\n")
    
    def test_syntax_error(self):
        """Test handling of syntax errors"""
        code = """
print("This line is fine")
print("This line has a syntax error"
"""
        with self.assertRaises(ValueError) as context:
            self.python_runner.run({"code": code})
        self.assertIn("Error running code: ", str(context.exception))
        # Check that it contains part of the error message, as the exact message might vary by Python version
        self.assertIn("was never closed", str(context.exception))
    
    def test_execution_isolation(self):
        """Test that executions are isolated from each other"""
        # First execution: define a variable
        code1 = """
x = 42
print(f"x = {x}")
"""
        result1 = self.python_runner.run({"code": code1})
        self.assertEqual(result1["output"], "x = 42\n")
        
        # Second execution: the variable should not be available
        code2 = """
try:
    print(f"x = {x}")
except NameError:
    print("x is not defined")
"""
        result2 = self.python_runner.run({"code": code2})
        self.assertEqual(result2["output"], "x is not defined\n")

if __name__ == '__main__':
    unittest.main() 