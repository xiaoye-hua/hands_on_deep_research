from src.base_class.base_agent import BaseAgent
from src.base_class.base_tool import BaseTool
from typing import List
import subprocess
from src.llm_call import llm_call, extract_xml
from src.prompts.code_agent_prompt import prompt_template
from src.tool.python_runner import PythonRunner
import re
import ast

class CodeAgent(BaseAgent):
    def __init__(self, tools: List[BaseTool], max_steps: int=1) -> None:
        super().__init__(tools, prompt_template)
        # Only set the default prompt template if none was provided
        # if prompt_template is None:
        self.prompt_template = prompt_template        
        self.python_runner = PythonRunner()
        self.max_steps = max_steps
    
    def run(self, task: str) -> dict:
        self.logger.info(f"Running CodeAgent with task: {task[:50]}...")
        final_answer = None
        prompt = self.prompt_template + "\n" + f"Task: {task}" + '\n'
        step = 0
        while step < self.max_steps and final_answer is None:
            self.logger.debug(f"Generated prompt: {prompt[:100]}...")
            self.logger.info(f"LLM prompt: {prompt}")
            response = self.query_llm(prompt)
            self.logger.info(f"Received response from LLM:")
            self.logger.info(f"Response: {response}")
            codes = self.extract_codes(response)
            # Run the code and capture the output
            observation = self.python_runner.run(codes)
            final_answer = self.extract_final_answer(observation)
            # self.logger.debug(f"Code execution output: {observation}")
            prompt = prompt + response + "\n" + f"Observation: {observation}" + '\n'
        self.logger.info(f"Final answer: {final_answer}")
        # code = self.query_llm(prompt)
        # self.logger.info(f"Received code from LLM: {code}")
    
    def extract_final_answer(self, observation: str) -> str:
        if "Final answer" in observation:
            return observation.split("final answer:")[1].strip().replace("```", "").replace("\n", "")
        return None
    
    def extract_codes(self, code_blob: str) -> List[str]:
        """Parses the LLM's output to get any code blob inside. Will return the code directly if it's code."""
        pattern = r"```(?:py|python)?\n(.*?)\n```"
        matches = re.findall(pattern, code_blob, re.DOTALL)
        if len(matches) == 0:
            try:  # Maybe the LLM outputted a code blob directly
                ast.parse(code_blob)
                return code_blob
            except SyntaxError:
                pass

            if "final" in code_blob and "answer" in code_blob:
                raise ValueError(
                    f"""
    Your code snippet is invalid, because the regex pattern {pattern} was not found in it.
    Here is your code snippet:
    {code_blob}
    It seems like you're trying to return the final answer, you can do it as follows:
    Code:
    ```py
    final_answer("YOUR FINAL ANSWER HERE")
    ```<end_code>""".strip()
                )
            raise ValueError(
                f"""
    Your code snippet is invalid, because the regex pattern {pattern} was not found in it.
    Here is your code snippet:
    {code_blob}
    Make sure to include code with the correct pattern, for instance:
    Thoughts: Your thoughts
    Code:
    ```py
    # Your python code here
    ```<end_code>""".strip()
            )
        return "\n\n".join(match.strip() for match in matches)
    
    def get_observation(self, codes: List[str]) -> str:
        return codes

    
        
    
    def query_llm(self, prompt: str) -> str:
        # model_id = "gpt-3.5-turbo"
        model_id = 'qwen2.5:1.5b'
        self.logger.info(f"Querying LLM with model: {model_id}")
        # self.logger.debug(f"LLM prompt: {prompt[:100]}...")
        
        response = llm_call(prompt=prompt, model=model_id)
        self.logger.debug(f"Raw LLM response: {response[:100]}...")
        return response
    
    def _execute_linux_command(self, command: str) -> dict:
        """
        Execute a Linux command and return the output and error if any.
        
        Args:
            command: The Linux command to execute
            
        Returns:
            A dictionary containing stdout, stderr, and return code
        """
        # Handle empty commands
        if not command or command.strip() == "":
            self.logger.warning("Attempted to execute empty command")
            return {
                "stdout": "",
                "stderr": "Error: Empty command",
                "returncode": 1
            }
            
        try:
            self.logger.debug(f"Running subprocess: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.logger.debug(f"Subprocess completed with return code: {result.returncode}")
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            self.logger.error(f"Exception in subprocess: {str(e)}", exc_info=True)
            # Re-raise the exception to be handled by the caller
            raise e 
    

if __name__ == "__main__":
    agent = CodeAgent(tools=[])
    result = agent.run("what's 5677*325343-4343*4/223?")
    print(result)