#!/usr/bin/env python
"""
Simple Research Example.

This script demonstrates the basic usage of the research pipeline.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.evaluator import EvaluatorAgent
from src.agents.research import ResearchAgent
from src.config.settings import load_settings
from src.pipelines.research import ResearchPipeline
from src.utils.logging import setup_logging


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Simple Research Example")
    parser.add_argument(
        "query", 
        nargs="?", 
        default="What are the latest advancements in AI research?",
        help="The research query to process (default: What are the latest advancements in AI research?)"
    )
    parser.add_argument(
        "--model", 
        default="gpt-4",
        help="The language model to use (default: gpt-4)"
    )
    parser.add_argument(
        "--max-iterations", 
        type=int, 
        default=3,
        help="Maximum number of research iterations (default: 3)"
    )
    parser.add_argument(
        "--save-results", 
        action="store_true",
        help="Save results to disk"
    )
    parser.add_argument(
        "--output-file", 
        default=None,
        help="Output file to save results (default: auto-generated)"
    )
    return parser.parse_args()


async def run_research(
    query: str, 
    model: str = "gpt-4", 
    max_iterations: int = 3,
    save_results: bool = True,
    output_file: str = None
) -> Dict[str, Any]:
    """Run a research task.

    Args:
        query: The research query to process.
        model: The language model to use.
        max_iterations: Maximum number of research iterations.
        save_results: Whether to save results to disk.
        output_file: Output file to save results to.

    Returns:
        A dictionary containing the research results.
    """
    # Create agents
    research_agent = ResearchAgent(
        model=model,
        max_iterations=max_iterations,
    )
    
    evaluator_agent = EvaluatorAgent(model=model)
    
    # Create and run pipeline
    pipeline = ResearchPipeline(
        agent=research_agent,
        evaluator=evaluator_agent,
        save_results=save_results,
    )
    
    # Run the pipeline asynchronously
    results = await pipeline.run_async(query)
    
    # Save results to specified file if requested
    if save_results and output_file:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {output_file}")
    
    return results


def main() -> None:
    """Main entry point for the example script."""
    # Set up logging
    setup_logging(log_level="INFO")
    
    # Parse arguments
    args = parse_arguments()
    
    # Load settings
    settings = load_settings()
    
    # Print configuration
    print("Running research with the following configuration:")
    print(f"  Query: {args.query}")
    print(f"  Model: {args.model}")
    print(f"  Max iterations: {args.max_iterations}")
    print(f"  Save results: {args.save_results}")
    if args.output_file:
        print(f"  Output file: {args.output_file}")
    print("\nStarting research...\n")
    
    # Run the research
    results = asyncio.run(run_research(
        query=args.query,
        model=args.model,
        max_iterations=args.max_iterations,
        save_results=args.save_results,
        output_file=args.output_file,
    ))
    
    # Print the report
    print("\nResearch Report:")
    print("=" * 80)
    print(results["research"]["report"])
    print("=" * 80)
    
    # Print evaluation summary if available
    if results.get("evaluation"):
        print("\nEvaluation Summary:")
        print(f"Overall Score: {results['evaluation']['overall_assessment']['overall_score']}/10")
        print(f"Verdict: {results['evaluation']['overall_assessment']['verdict']}")
    
    print(f"\nResearch completed in {results['metadata']['duration_seconds']:.2f} seconds")


if __name__ == "__main__":
    main() 