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
    
    def run(self, input: dict) -> dict:
        code = input.get("code")
        if not code:
            raise ValueError("No code provided")
        
        # Capture stdout
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            exec(code)
            output = new_stdout.getvalue()
            return {"output": output}
        except Exception as e:
            raise ValueError(f"Error running code: {e}")
        finally:
            # Restore stdout
            sys.stdout = old_stdout
    