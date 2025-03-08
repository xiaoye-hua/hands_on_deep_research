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
        code = input.get("code")
        if not code:
            self.logger.error("No code provided to PythonRunner")
            raise ValueError("No code provided")
        
        self.logger.info("Running Python code")
        self.logger.debug(f"Code to run: {code[:100]}...")
        
        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            self.logger.debug("Executing code")
            exec(code)
            output = new_stdout.getvalue()
            self.logger.debug(f"Code execution completed, output: {output[:100]}...")
            return {"output": output}
        except Exception as e:
            error_msg = f"Error running code: {e}"
            self.logger.error(error_msg, exc_info=True)
            raise ValueError(error_msg)
        finally:
            # Restore stdout
            sys.stdout = old_stdout
            self.logger.debug("Restored stdout after code execution")
    