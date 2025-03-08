import unittest
from unittest.mock import patch, MagicMock
import subprocess
from src.agent.code_agent import CodeAgent
from src.base_class.base_tool import BaseTool

class TestCodeAgent(unittest.TestCase):
    def setUp(self):
        # Create a mock tool
        self.mock_tool = MagicMock(spec=BaseTool)
        self.mock_tool.run.return_value = {"result": "mock_result"}
        
        # Initialize the agent with the mock tool
        self.agent = CodeAgent(tools=[self.mock_tool])
    
    def test_init(self):
        """Test the initialization of the CodeAgent class."""
        self.assertEqual(len(self.agent.tools), 1)
        self.assertIsNotNone(self.agent.prompt_template)
        self.assertIn("{query}", self.agent.prompt_template)
    
    def test_init_with_custom_prompt(self):
        """Test initialization with a custom prompt template."""
        custom_prompt = "Custom prompt with {query}"
        agent = CodeAgent(tools=[self.mock_tool], prompt_template=custom_prompt)
        self.assertEqual(agent.prompt_template, custom_prompt)
    
    @patch('src.agent.code_agent.llm_call')
    @patch('src.agent.code_agent.extract_xml')
    @patch('subprocess.run')
    def test_run(self, mock_subprocess_run, mock_extract_xml, mock_llm_call):
        """Test the run method of the CodeAgent class."""
        # Setup mocks
        mock_llm_call.return_value = "<code>ls -la</code>"
        mock_extract_xml.return_value = "ls -la"
        
        mock_process = MagicMock()
        mock_process.stdout = "file1\nfile2"
        mock_process.stderr = ""
        mock_process.returncode = 0
        mock_subprocess_run.return_value = mock_process
        
        # Call the method
        result = self.agent.run("List files in the current directory")
        
        # Assertions
        mock_llm_call.assert_called_once()
        mock_extract_xml.assert_called_once_with("<code>ls -la</code>", "code")
        mock_subprocess_run.assert_called_once_with("ls -la", shell=True, capture_output=True, text=True)
        
        self.assertEqual(result["stdout"], "file1\nfile2")
        self.assertEqual(result["stderr"], "")
        self.assertEqual(result["returncode"], 0)
    
    @patch('src.agent.code_agent.llm_call')
    @patch('src.agent.code_agent.extract_xml')
    def test_run_with_empty_command(self, mock_extract_xml, mock_llm_call):
        """Test the run method when the LLM returns an empty command."""
        # Setup mocks
        mock_llm_call.return_value = "<code></code>"
        mock_extract_xml.return_value = ""
        
        # Call the method and check if it handles empty commands
        result = self.agent.run("Generate an empty command")
        
        # Empty command should still be executed but return an error
        self.assertNotEqual(result["returncode"], 0)
    
    def test_get_prompt(self):
        """Test the _get_prompt method of the CodeAgent class."""
        query = "List files in the current directory"
        prompt = self.agent._get_prompt(query)
        
        self.assertIn(query, prompt)
    
    def test_get_prompt_with_empty_query(self):
        """Test the _get_prompt method with an empty query."""
        query = ""
        prompt = self.agent._get_prompt(query)
        
        # Even with empty query, the prompt should be formatted correctly
        self.assertIn(query, prompt)
    
    @patch('src.agent.code_agent.llm_call')
    def test_query_llm(self, mock_llm_call):
        """Test the query_llm method of the CodeAgent class."""
        # Setup mock
        mock_llm_call.return_value = "<code>ls -la</code>"
        
        # Call the method
        with patch('src.agent.code_agent.extract_xml', return_value="ls -la"):
            result = self.agent.query_llm("Test prompt")
        
        # Assertions
        mock_llm_call.assert_called_once_with(prompt="Test prompt", model="gpt-3.5-turbo")
        self.assertEqual(result, "ls -la")
    
    @patch('src.agent.code_agent.llm_call')
    def test_query_llm_no_code_tag(self, mock_llm_call):
        """Test the query_llm method when the response doesn't contain a code tag."""
        # Setup mock to return a response without a code tag
        mock_llm_call.return_value = "This is a response without a code tag"
        
        # Call the method
        result = self.agent.query_llm("Test prompt")
        
        # Should return an empty string if no code tag is found
        self.assertEqual(result, "")
    
    def test_execute_linux_command_success(self):
        """Test the _execute_linux_command method with a successful command."""
        # Use a simple command that should work on most systems
        result = self.agent._execute_linux_command("echo 'test'")
        
        self.assertIn("test", result["stdout"])
        self.assertEqual(result["stderr"], "")
        self.assertEqual(result["returncode"], 0)
    
    def test_execute_linux_command_failure(self):
        """Test the _execute_linux_command method with a failing command."""
        # Use a command that should fail on most systems
        result = self.agent._execute_linux_command("command_that_does_not_exist")
        
        self.assertNotEqual(result["returncode"], 0)
        self.assertNotEqual(result["stderr"], "")
    
    def test_execute_linux_command_with_empty_command(self):
        """Test the _execute_linux_command method with an empty command."""
        # Empty command should still be executed but return an error
        result = self.agent._execute_linux_command("")
        
        self.assertNotEqual(result["returncode"], 0)
    
    @patch('subprocess.run')
    def test_execute_linux_command_exception(self, mock_subprocess_run):
        """Test the _execute_linux_command method when an exception occurs."""
        # Setup mock to raise an exception
        mock_subprocess_run.side_effect = Exception("Test exception")
        
        # This should handle the exception gracefully
        with self.assertRaises(Exception):
            self.agent._execute_linux_command("echo 'test'")

if __name__ == '__main__':
    unittest.main() 