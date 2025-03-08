from src.base_class.base_agent import BaseAgent
from src.base_class.base_tool import BaseTool
from typing import List
import subprocess
from src.llm_call import llm_call, extract_xml

class CodeAgent(BaseAgent):
    def __init__(self, tools: List[BaseTool], prompt_template: str=None) -> None:
        super().__init__(tools, prompt_template)
        self.prompt_template = """
        You are a coding and linux command experts. You are given a task to write linux command to solve the problem.
        {query}
        You response should be in the following format:
        <code>your linux command</code>
        """
    
    def run(self, query: str) -> dict:
        prompt = self._get_prompt(query)
        linux_cmd = self.query_llm(prompt)
        run_result = self._execute_linux_command(linux_cmd)
        return run_result
    
    def query_llm(self, prompt: str) -> str:
        model_id = "gpt-4o-mini"
        response = llm_call(prompt=prompt, model=model_id)
        return extract_xml(response, "code")
    
    def _execute_linux_command(self, command: str) -> dict:
        """
        Execute a Linux command and return the output and error if any.
        
        Args:
            command: The Linux command to execute
            
        Returns:
            A dictionary containing stdout, stderr, and return code
        """
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }        
        