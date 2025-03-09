from src.base_class.base_tool import BaseTool
import sys
import io

class PythonRunner(BaseTool):
    def __init__(self):
        super().__init__()
        self.name = "python_runner"
        self.description = "Run a python script"
        self.parameters = {
            'code': {
                'type': 'string',
                'description': 'The python code to run'
            }
        }
        self.logger.debug(f"PythonRunner initialized with parameters: {self.parameters}")
    
    def run(self, input: dict) -> dict:
        """
        Run Python code and return the output.
        
        Args:
            input: A dictionary containing the code to run.
            
        Returns:
            A dictionary containing the output of the code execution.
        """
        code = input.get("code")
        if not code:
            self.logger.error("No code provided to PythonRunner")
            raise ValueError("No code provided")
        
        predefined_code = """
def final_answer(answer):
    print(f"Final answer: {answer}")
        """
        code_to_run = predefined_code + "\n" + code
        
        self.logger.info("Running Python code")
        self.logger.debug(f"Code to run: {code_to_run[:100]}...")
        
        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            self.logger.debug("Executing code")
            # Execute the code and capture any print statements
            exec(code_to_run, {}, {})
            # Get the captured output
            output = new_stdout.getvalue()
            self.logger.debug(f"Code execution completed, output: {output[:100]}...")
            return {"output": output, "success": True}
        except Exception as e:
            error_msg = f"Error running code: {e}"
            self.logger.error(error_msg, exc_info=True)
            return {"output": error_msg, "success": False}
        finally:
            # Restore stdout
            sys.stdout = old_stdout
            self.logger.debug("Restored stdout after code execution")
    
    def forward(self, input: dict) -> dict:
        """
        Forward method to maintain compatibility with other frameworks.
        
        Args:
            input: A dictionary containing the code to run.
            
        Returns:
            The result of the run method.
        """
        return self.run(input)

    