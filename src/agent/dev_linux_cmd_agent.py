from src.base_class.base_agent import BaseAgent
from src.base_class.base_tool import BaseTool
from typing import List
import subprocess
from src.llm_call import llm_call, extract_xml

class CodeAgent(BaseAgent):
    def __init__(self, tools: List[BaseTool], prompt_template: str=None) -> None:
        super().__init__(tools, prompt_template)
        # Only set the default prompt template if none was provided
        if prompt_template is None:
            self.prompt_template = """
            You are a coding and linux command experts. You are given a task to write linux command to solve the problem.
            {query}
            You response should be in the following format:
            <code>your linux command</code>
            """
            self.logger.debug("Using default prompt template for CodeAgent")
    
    def run(self, query: str) -> dict:
        self.logger.info(f"Running CodeAgent with query: {query[:50]}...")
        prompt = self._get_prompt(query)
        self.logger.debug(f"Generated prompt: {prompt[:100]}...")
        
        linux_cmd = self.query_llm(prompt)
        self.logger.info(f"Received command from LLM: {linux_cmd}")
        
        # Handle empty commands
        if not linux_cmd or linux_cmd.strip() == "":
            self.logger.warning("Empty command received from LLM")
            return {
                "stdout": "",
                "stderr": "Error: Empty command received from LLM",
                "returncode": 1,
                'linux_cmd': linux_cmd
            }
        try:
            self.logger.info(f"Executing command: {linux_cmd}")
            run_result = self._execute_linux_command(linux_cmd)
            self.logger.info(f"Command execution completed with return code: {run_result['returncode']}")
            self.logger.debug(f"Command stdout: {run_result['stdout'][:100]}...")
            
            if run_result["returncode"] != 0:
                self.logger.warning(f"Command failed with stderr: {run_result['stderr']}")
                
            return {
                "success": True,
                "result": run_result,
                "stdout": run_result["stdout"],
                "stderr": run_result["stderr"],
                "returncode": run_result["returncode"],
                'linux_cmd': linux_cmd
            }
        except Exception as e:
            self.logger.error(f"Error executing command: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": str(e),
                "returncode": 1,
                'linux_cmd': linux_cmd
            }
    
    def query_llm(self, prompt: str) -> str:
        model_id = "gpt-3.5-turbo"
        self.logger.info(f"Querying LLM with model: {model_id}")
        self.logger.debug(f"LLM prompt: {prompt[:100]}...")
        
        response = llm_call(prompt=prompt, model=model_id)
        self.logger.debug(f"Raw LLM response: {response[:100]}...")
        
        extracted = extract_xml(response, "code")
        self.logger.debug(f"Extracted command: {extracted}")
        return extracted
    
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