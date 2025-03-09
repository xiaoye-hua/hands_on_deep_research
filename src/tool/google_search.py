from src.base_class.base_tool import BaseTool
from googlesearch import search
from typing import Dict, Any, List, Optional
import time
import random

class GoogleSearch(BaseTool):
    name = "google_search"
    description = "A tool for searching the web using Google."
    inputs = ["query", "num_results", "lang", "safe"]
    outputs = ["success", "results", "error"]

    def run(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """
        Perform a search using Google and return the results.
        
        Args:
            input: A dictionary containing:
                - query (str): The search query
                - num_results (int, optional): Number of results to return (default: 5)
                - lang (str, optional): Language for search results (default: 'en')
                - safe (bool, optional): Whether to use safe search (default: True)
        
        Returns:
            dict: A dictionary containing:
                - success (bool): Whether the search was successful
                - results (list): List of search results, each containing:
                    - title (str): Title of the result
                    - url (str): URL of the result
                    - snippet (str): Snippet/description of the result (if available)
                - error (str, optional): Error message if the search failed
        """        
        if not query:
            return {
                "success": False,
                "error": "No search query provided",
                "results": []
            }
        
        try:
            # Add a small random delay to avoid rate limiting
            time.sleep(random.uniform(0.5, 1.5))
            
            # Use the googlesearch package to perform the search
            search_results = search(
                query,
                num_results=num_results,
            )
            
            # Process the results
            results = []
            for url in search_results:
                # The googlesearch package only returns URLs, not titles or snippets
                results.append({
                    "title": self._extract_title_from_url(url),
                    "url": url,
                    "snippet": "No description available"  # The package doesn't provide snippets
                })
            
            # If no results were found
            return results
            
        except Exception as e:
            self.logger.error(f"Error during Google search: {str(e)}")
            result = [f"Error during search: {str(e)}"]
            return result
    
    def _extract_title_from_url(self, url: str) -> str:
        """
        Extract a title from a URL.
        This is a simple implementation since the googlesearch package doesn't provide titles.
        
        Args:
            url: The URL to extract a title from
            
        Returns:
            A title extracted from the URL
        """
        # Remove protocol
        if "://" in url:
            url = url.split("://")[1]
        
        # Remove www. if present
        if url.startswith("www."):
            url = url[4:]
        
        # Remove path and query parameters
        if "/" in url:
            url = url.split("/")[0]
        
        # Return the domain as the title
        return url

# Run the example if this file is executed directly
if __name__ == "__main__":
    # search_engine = GoogleSearch()
    result = GoogleSearch()(**{"query": "What is the capital of France?", "num_results": 5})
    print("\nSearch Results:")
    print("=" * 50)
    for i, item in enumerate(result, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   URL: {item['url']}")
        print(f"   {item['snippet']}")