import unittest
from unittest.mock import patch, MagicMock
import pytest
from src.tool.search_engine import SearchEngine

class TestDuckDuckGoTool(unittest.TestCase):
    def setUp(self):
        self.tool = SearchEngine()
    
    def test_init(self):
        """Test that the tool initializes correctly."""
        self.assertEqual(self.tool.name, "duckduckgo")
        self.assertEqual(self.tool.base_url, "https://html.duckduckgo.com/html/")
        self.assertIn("User-Agent", self.tool.headers)
    
    def test_run_no_query(self):
        """Test that the tool handles missing query correctly."""
        result = self.tool.run({})
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "No search query provided")
        self.assertEqual(result["results"], [])
        
        result = self.tool.run({"query": ""})
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "No search query provided")
        self.assertEqual(result["results"], [])
    
    @patch('requests.post')
    def test_run_http_error(self, mock_post):
        """Test that the tool handles HTTP errors correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response
        
        result = self.tool.run({"query": "test query"})
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "DuckDuckGo returned status code 404")
        self.assertEqual(result["results"], [])
    
    @patch('requests.post')
    def test_run_exception(self, mock_post):
        """Test that the tool handles exceptions correctly."""
        mock_post.side_effect = Exception("Test exception")
        
        result = self.tool.run({"query": "test query"})
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Error during search: Test exception")
        self.assertEqual(result["results"], [])
    
    @patch('requests.post')
    def test_run_success(self, mock_post):
        """Test that the tool processes search results correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="result">
                    <a class="result__a" href="https://example.com">Example Title</a>
                    <a class="result__url">https://example.com</a>
                    <div class="result__snippet">Example snippet text</div>
                </div>
                <div class="result">
                    <a class="result__a" href="https://example2.com">Example Title 2</a>
                    <a class="result__url">https://example2.com</a>
                    <div class="result__snippet">Example snippet text 2</div>
                </div>
            </body>
        </html>
        """
        mock_post.return_value = mock_response
        
        result = self.tool.run({"query": "test query", "num_results": 2})
        self.assertTrue(result["success"])
        self.assertEqual(len(result["results"]), 2)
        
        # Check first result
        self.assertEqual(result["results"][0]["title"], "Example Title")
        self.assertEqual(result["results"][0]["url"], "https://example.com")
        self.assertEqual(result["results"][0]["snippet"], "Example snippet text")
        
        # Check second result
        self.assertEqual(result["results"][1]["title"], "Example Title 2")
        self.assertEqual(result["results"][1]["url"], "https://example2.com")
        self.assertEqual(result["results"][1]["snippet"], "Example snippet text 2")
    
    @patch('requests.post')
    def test_run_with_redirect_url(self, mock_post):
        """Test that the tool handles redirect URLs correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="result">
                    <a class="result__a" href="/redirect?uddg=https%3A%2F%2Fexample.com">Example Title</a>
                    <div class="result__snippet">Example snippet text</div>
                </div>
            </body>
        </html>
        """
        mock_post.return_value = mock_response
        
        result = self.tool.run({"query": "test query"})
        self.assertTrue(result["success"])
        self.assertEqual(len(result["results"]), 1)
        
        # Check that URL extraction from redirect works
        self.assertEqual(result["results"][0]["title"], "Example Title")
        self.assertEqual(result["results"][0]["url"], "https://example.com")
        self.assertEqual(result["results"][0]["snippet"], "Example snippet text")
    
    @patch('requests.post')
    def test_run_missing_elements(self, mock_post):
        """Test that the tool handles missing HTML elements correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="result">
                    <!-- Missing title and URL elements -->
                    <div class="result__snippet">Example snippet text</div>
                </div>
            </body>
        </html>
        """
        mock_post.return_value = mock_response
        
        result = self.tool.run({"query": "test query"})
        self.assertTrue(result["success"])
        self.assertEqual(len(result["results"]), 1)
        
        # Check default values for missing elements
        self.assertEqual(result["results"][0]["title"], "No title")
        self.assertEqual(result["results"][0]["url"], "No URL")
        self.assertEqual(result["results"][0]["snippet"], "Example snippet text")

if __name__ == "__main__":
    unittest.main() 