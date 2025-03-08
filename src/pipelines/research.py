"""
Research Pipeline Implementation.

This module provides the implementation of the research pipeline,
which orchestrates the research process across multiple agents.
"""

import asyncio
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Union

from src.agents.evaluator import EvaluatorAgent
from src.agents.research import ResearchAgent
from src.pipelines.base import BasePipeline
from src.utils.logging import get_logger

logger = get_logger(__name__)


class ResearchPipeline(BasePipeline):
    """Research pipeline that orchestrates the research process.

    This pipeline coordinates between research and evaluation agents to:
    1. Process research queries
    2. Conduct research to gather information
    3. Evaluate the quality of findings
    4. Generate comprehensive reports
    """

    def __init__(
        self,
        agent: Optional[ResearchAgent] = None,
        evaluator: Optional[EvaluatorAgent] = None,
        output_dir: Optional[str] = None,
        save_results: bool = True,
        evaluate_results: bool = True,
        max_iterations: int = 5,
        **kwargs: Any,
    ) -> None:
        """Initialize the research pipeline.

        Args:
            agent: The research agent to use. If not provided, a new one will be created.
            evaluator: The evaluator agent to use. If not provided, a new one will be created.
            output_dir: Optional directory to save results to.
            save_results: Whether to save results to disk.
            evaluate_results: Whether to evaluate results using the evaluator agent.
            max_iterations: Maximum number of research iterations.
            **kwargs: Additional keyword arguments passed to the base class.
        """
        # Create default agents if not provided
        if agent is None:
            logger.info("No research agent provided, creating default ResearchAgent")
            agent = ResearchAgent()
            
        super().__init__(agent, output_dir, save_results, **kwargs)
        
        self.research_agent = agent
        
        if evaluator is None and evaluate_results:
            logger.info("No evaluator agent provided, creating default EvaluatorAgent")
            evaluator = EvaluatorAgent()
        
        self.evaluator = evaluator
        self.evaluate_results = evaluate_results
        self.max_iterations = max_iterations

    async def run_async(self, query: str) -> Dict[str, Any]:
        """Run the research pipeline asynchronously.

        Args:
            query: The research query to process.

        Returns:
            A dictionary containing the research results and evaluations.
        """
        start_time = time.time()
        logger.info(f"Starting research for query: {query}")
        
        # Phase 1: Conduct research
        research_results = await self.research_agent.process(query)
        
        # Phase 2: Evaluate research (if enabled)
        evaluation_results = None
        if self.evaluate_results and self.evaluator is not None:
            logger.info("Evaluating research results")
            evaluation_results = await self.evaluator.process(
                query=query,
                report=research_results["report"],
                findings=research_results["findings"]
            )
        
        # Compile final results
        final_results = {
            "query": query,
            "research": research_results,
            "evaluation": evaluation_results,
            "metadata": {
                "duration_seconds": time.time() - start_time,
                "timestamp": time.time(),
                "max_iterations": self.max_iterations,
                "iterations_used": research_results.get("iterations", 0),
            }
        }
        
        # Save results if enabled
        if self.save_results:
            # Create a filename based on a sanitized version of the query
            sanitized_query = "".join(c if c.isalnum() else "_" for c in query[:30])
            filename = f"research_{sanitized_query}_{int(time.time())}.json"
            filepath = self.save_result_to_disk(final_results, filename)
            logger.info(f"Research results saved to: {filepath}")
        
        logger.info(f"Research completed in {final_results['metadata']['duration_seconds']:.2f} seconds")
        return final_results
    
    async def run_batch_async(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Run multiple research queries in batch.

        Args:
            queries: List of research queries to process.

        Returns:
            A list of dictionaries containing the research results for each query.
        """
        tasks = [self.run_async(query) for query in queries]
        return await asyncio.gather(*tasks)
    
    def run_batch(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Run multiple research queries in batch synchronously.

        Args:
            queries: List of research queries to process.

        Returns:
            A list of dictionaries containing the research results for each query.
        """
        return asyncio.run(self.run_batch_async(queries)) 