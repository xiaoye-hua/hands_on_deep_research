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
            
            try:
                codes = self.extract_codes(response)
                if codes:
                    # Run the code and capture the output
                    observation = self.get_observation(codes)
                    final_answer = self.extract_final_answer(observation)
                    self.logger.debug(f"Code execution output: {observation}")
                else:
                    observation = "No valid code found in the response."
                    self.logger.warning("No valid code found in the response")
            except Exception as e:
                observation = f"Error: {str(e)}"
                self.logger.error(f"Error processing response: {str(e)}", exc_info=True)
            
            prompt = prompt + response + "\n" + f"Observation: {observation}" + '\n'
            step += 1
            
        result = {
            "final_answer": final_answer,
            "steps": step,
            "success": final_answer is not None
        }
        self.logger.info(f"Final result: {result}")
        return result
    
    def extract_final_answer(self, observation: str) -> str:
        """
        Extracts the final answer from the observation.
        
        Args:
            observation: The observation string containing the final answer.
            
        Returns:
            The extracted final answer, or None if no final answer is found.
        """
        self.logger.debug(f"Extracting final answer from: {observation[:100]}...")
        
        # Try to match "Final answer: <answer>" pattern
        final_answer_pattern = r"Final answer: (.*?)(?:\n|$)"
        match = re.search(final_answer_pattern, observation, re.IGNORECASE)
        
        if match:
            final_answer = match.group(1).strip()
            self.logger.info(f"Extracted final answer: {final_answer}")
            return final_answer
            
        # If no final answer found, check if the observation itself is a simple value
        if observation and len(observation.strip().split('\n')) == 1:
            self.logger.info(f"Using observation as final answer: {observation.strip()}")
            return observation.strip()
            
        self.logger.warning("No final answer found in observation")
        return None
    
    def extract_codes(self, code_blob: str) -> str:
        """
        Parses the LLM's output to get any code blob inside.
        
        Args:
            code_blob: The LLM's response containing code.
            
        Returns:
            The extracted code.
        """
        self.logger.debug(f"Extracting code from: {code_blob[:100]}...")
        
        # Try to extract code between ```py and ``` or ```python and ```
        pattern = r"```(?:py|python)?\n(.*?)\n```"
        matches = re.findall(pattern, code_blob, re.DOTALL)
        
        if matches:
            extracted_code = "\n\n".join(match.strip() for match in matches)
            self.logger.debug(f"Extracted code: {extracted_code[:100]}...")
            return extracted_code
        
        # If no code blocks found, try to extract code after "Code:" or "code:"
        code_pattern = r"(?:Code:|code:)\s*\n(.*?)(?:\n\s*(?:Observation:|<end_code>|$))"
        code_matches = re.findall(code_pattern, code_blob, re.DOTALL)
        
        if code_matches:
            extracted_code = "\n\n".join(match.strip() for match in code_matches)
            self.logger.debug(f"Extracted code after 'Code:': {extracted_code[:100]}...")
            return extracted_code
            
        # If still no code found, try to parse the entire response as code
        try:
            ast.parse(code_blob)
            self.logger.debug("Entire response parsed as code")
            return code_blob
        except SyntaxError:
            self.logger.warning("No valid code found in response")
            
        # If we get here, no valid code was found
        self.logger.warning(f"No code found in response: {code_blob}")
        return None
    
    def get_observation(self, codes: str) -> str:
        """
        Gets the observation from running the code.
        
        Args:
            codes: The code to run.
            
        Returns:
            The observation from running the code.
        """
        if not codes:
            return "No valid code found in the response."
            
        try:
            result = self.python_runner.run({"code": codes})
            return result.get("output", "No output from code execution.")
        except Exception as e:
            error_msg = f"Error running code: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return error_msg
    
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