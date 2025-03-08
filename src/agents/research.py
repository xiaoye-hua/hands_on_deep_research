"""
Research Agent Implementation.

This module provides the implementation of the research agent,
which is responsible for performing research tasks.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Set, Union

import aiohttp
import openai
from dotenv import load_dotenv

from src.agents.base import BaseAgent
from src.utils.api import get_api_key

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class ResearchAgent(BaseAgent):
    """Research agent that performs information gathering and processing.

    This agent is responsible for:
    1. Generating search queries based on the research question
    2. Processing search results to extract relevant information
    3. Determining if further research is needed
    4. Compiling findings into a comprehensive report
    """

    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        max_iterations: int = 5,
        max_concurrent_requests: int = 5,
        timeout: int = 300,
        **kwargs: Any,
    ) -> None:
        """Initialize the research agent.

        Args:
            model: The language model to use for the agent.
            temperature: Sampling temperature for the model.
            max_tokens: Maximum number of tokens for model responses.
            max_iterations: Maximum number of research iterations.
            max_concurrent_requests: Maximum number of concurrent API requests.
            timeout: Timeout in seconds for API requests.
            **kwargs: Additional keyword arguments for the agent.
        """
        super().__init__(model, temperature, max_tokens, **kwargs)
        self.max_iterations = max_iterations
        self.max_concurrent_requests = max_concurrent_requests
        self.timeout = timeout
        self.visited_urls: Set[str] = set()
        self.openai_api_key = get_api_key("OPENAI_API_KEY")
        self.system_prompt = (
            "You are a research assistant AI. Your goal is to gather and analyze "
            "information to answer the user's query comprehensively and accurately. "
            "You should be thorough, clear, and provide properly sourced information. "
            "You should be aware of what you know and don't know, and be transparent "
            "about any uncertainties in your research."
        )
        self.clear_context()

    def add_to_context(self, role: str, content: str) -> None:
        """Add a message to the agent's context.

        Args:
            role: The role of the message sender (e.g., 'system', 'user', 'assistant').
            content: The content of the message.
        """
        self.context.append({"role": role, "content": content})

    def clear_context(self) -> None:
        """Clear the agent's context."""
        self.context = [{"role": "system", "content": self.system_prompt}]

    async def call_model(self, prompt: Union[str, List[Dict[str, str]]]) -> str:
        """Call the language model with a prompt.

        Args:
            prompt: The prompt to send to the model, either as a string or a list of messages.

        Returns:
            The model's response as a string.
        """
        try:
            if isinstance(prompt, str):
                messages = [{"role": "user", "content": prompt}]
            else:
                messages = prompt

            client = openai.OpenAI(api_key=self.openai_api_key)
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling model: {e}")
            return f"Error: {e}"

    async def generate_search_queries(self, query: str) -> List[str]:
        """Generate search queries based on the research question.

        Args:
            query: The research question.

        Returns:
            A list of search queries.
        """
        prompt = (
            f"Based on the research question: '{query}', generate up to 4 distinct search "
            f"queries that would be useful for gathering comprehensive information. "
            f"Format your response as a JSON array of strings, containing only the search queries."
        )
        self.add_to_context("user", prompt)
        response = await self.call_model(self.context)
        self.add_to_context("assistant", response)

        try:
            # Extract JSON array from response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            queries = json.loads(json_str)
            if isinstance(queries, list):
                return queries
            return [str(queries)]
        except (json.JSONDecodeError, IndexError) as e:
            logger.error(f"Error parsing queries response: {e}")
            # Fallback: return a single search query based on the original query
            return [query]

    async def process_web_content(self, url: str, content: str) -> Dict[str, Any]:
        """Process web content to extract relevant information.

        Args:
            url: The URL of the web page.
            content: The content of the web page.

        Returns:
            A dictionary containing the extracted information.
        """
        prompt = (
            f"Analyze the following content from {url} and extract information relevant "
            f"to our research. Determine if this source is useful and reliable. If it is, "
            f"provide a detailed summary of the key points and insights.\n\n"
            f"Content: {content[:5000]}..."  # Limit content to avoid token limits
        )
        self.add_to_context("user", prompt)
        response = await self.call_model(self.context)
        self.add_to_context("assistant", response)

        return {
            "url": url,
            "is_useful": "not useful" not in response.lower(),
            "summary": response,
        }

    async def is_research_complete(self, current_findings: List[Dict[str, Any]]) -> bool:
        """Determine if the research is complete.

        Args:
            current_findings: The current research findings.

        Returns:
            True if the research is complete, False otherwise.
        """
        if not current_findings:
            return False

        findings_summary = "\n\n".join(
            [f"Source: {finding['url']}\nSummary: {finding['summary']}" for finding in current_findings]
        )
        prompt = (
            f"Based on the research findings so far, determine if we have enough information "
            f"to answer the original query comprehensively, or if further research is needed. "
            f"If further research is needed, specify what specific information is still missing.\n\n"
            f"Research findings:\n{findings_summary}\n\n"
            f"Is the research complete? Answer with 'COMPLETE' if yes, or 'INCOMPLETE: [missing info]' if no."
        )
        self.add_to_context("user", prompt)
        response = await self.call_model(self.context)
        self.add_to_context("assistant", response)

        return response.upper().startswith("COMPLETE")

    async def compile_report(self, query: str, findings: List[Dict[str, Any]]) -> str:
        """Compile a comprehensive report based on the research findings.

        Args:
            query: The original research question.
            findings: The research findings.

        Returns:
            A comprehensive report.
        """
        findings_summary = "\n\n".join(
            [f"Source: {finding['url']}\nSummary: {finding['summary']}" for finding in findings]
        )
        prompt = (
            f"Based on our research, create a comprehensive report that answers the original "
            f"question: '{query}'. Organize the information logically, cite sources where "
            f"appropriate, and provide a balanced and thorough analysis. Be clear about any "
            f"limitations or uncertainties in the research.\n\n"
            f"Research findings:\n{findings_summary}"
        )
        self.add_to_context("user", prompt)
        response = await self.call_model(self.context)
        self.add_to_context("assistant", response)

        return response

    async def search_web(self, query: str) -> List[Dict[str, str]]:
        """Search the web for information.

        Args:
            query: The search query.

        Returns:
            A list of search results, each containing a URL and snippet.
        """
        # This is a placeholder for actual search implementation
        # In a real implementation, this would call a search API like Google or Bing
        logger.info(f"Searching web for: {query}")
        return [
            {
                "url": f"https://example.com/result-{i}",
                "snippet": f"Example search result {i} for query: {query}",
            }
            for i in range(3)
        ]

    async def process(self, query: str) -> Dict[str, Any]:
        """Process a research query and return the results.

        Args:
            query: The research query to process.

        Returns:
            A dictionary containing the research results.
        """
        self.clear_context()
        self.add_to_context("user", f"Research query: {query}")
        
        findings: List[Dict[str, Any]] = []
        iteration = 0
        
        while iteration < self.max_iterations:
            logger.info(f"Research iteration {iteration + 1}/{self.max_iterations}")
            
            # Generate search queries
            search_queries = await self.generate_search_queries(query)
            
            # Search the web for each query
            for search_query in search_queries:
                search_results = await self.search_web(search_query)
                
                # Process each search result
                for result in search_results:
                    url = result["url"]
                    
                    # Skip already visited URLs
                    if url in self.visited_urls:
                        continue
                    
                    self.visited_urls.add(url)
                    
                    # In a real implementation, fetch and process the web page content
                    # For this example, we'll use the snippet as content
                    processed_result = await self.process_web_content(url, result["snippet"])
                    
                    if processed_result["is_useful"]:
                        findings.append(processed_result)
            
            # Check if research is complete
            if await self.is_research_complete(findings) or iteration == self.max_iterations - 1:
                break
                
            iteration += 1
        
        # Compile the final report
        report = await self.compile_report(query, findings)
        
        return {
            "query": query,
            "iterations": iteration + 1,
            "findings": findings,
            "report": report,
        } 