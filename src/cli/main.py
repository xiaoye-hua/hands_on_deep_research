"""
Main CLI module for the Hands-On Deep Research project.

This module provides the command-line interface for running research tasks.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional

from src.agents.evaluator import EvaluatorAgent
from src.agents.research import ResearchAgent
from src.config.settings import load_settings
from src.pipelines.research import ResearchPipeline
from src.utils.logging import get_logger, setup_logging

logger = get_logger(__name__)


def setup_argparse() -> argparse.ArgumentParser:
    """Set up the argument parser for the CLI.

    Returns:
        The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Hands-On Deep Research CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Research command
    research_parser = subparsers.add_parser("research", help="Run a research task")
    research_parser.add_argument("query", help="The research query")
    research_parser.add_argument(
        "--model",
        default=None,
        help="The language model to use (overrides env settings)",
    )
    research_parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of research iterations",
    )
    research_parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    research_parser.add_argument(
        "--output-file",
        default=None,
        help="Output file to save results (in addition to stdout)",
    )
    research_parser.add_argument(
        "--no-evaluation",
        action="store_true",
        help="Skip evaluation of research results",
    )

    # Batch research command
    batch_parser = subparsers.add_parser("batch", help="Run multiple research tasks")
    batch_parser.add_argument(
        "input_file",
        help="JSON file containing a list of queries",
    )
    batch_parser.add_argument(
        "--model",
        default=None,
        help="The language model to use (overrides env settings)",
    )
    batch_parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of research iterations",
    )
    batch_parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory to save results",
    )
    batch_parser.add_argument(
        "--no-evaluation",
        action="store_true",
        help="Skip evaluation of research results",
    )

    # Settings command
    settings_parser = subparsers.add_parser("settings", help="Show settings")
    settings_parser.add_argument(
        "--json",
        action="store_true",
        help="Output settings as JSON",
    )

    # Common arguments for all commands
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=None,
        help="Logging level",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help="Log file",
    )

    return parser


def format_research_results(results: Dict[str, Any], format_type: str) -> str:
    """Format research results based on the specified format type.

    Args:
        results: The research results to format.
        format_type: The format type ('text' or 'json').

    Returns:
        The formatted results.
    """
    if format_type == "json":
        return json.dumps(results, indent=2)

    # Default to text format
    output = []
    output.append(f"Research Query: {results['query']}")
    output.append(f"Iterations: {results['metadata']['iterations_used']}")
    output.append(f"Duration: {results['metadata']['duration_seconds']:.2f} seconds")
    output.append("\nResearch Report:")
    output.append("=" * 80)
    output.append(results['research']['report'])
    output.append("=" * 80)

    if results['evaluation']:
        output.append("\nEvaluation:")
        output.append(f"Overall Score: {results['evaluation']['overall_assessment']['overall_score']}/10")
        output.append(f"Verdict: {results['evaluation']['overall_assessment']['verdict']}")
        output.append("\nDetailed Assessment:")
        output.append(results['evaluation']['overall_assessment']['assessment'])

    return "\n".join(output)


def handle_research_command(args: argparse.Namespace, settings: Dict[str, Any]) -> None:
    """Handle the 'research' command.

    Args:
        args: Command-line arguments.
        settings: Application settings.
    """
    # Create agents with settings from args (if provided) or environment
    model = args.model or settings.default_model
    max_iterations = args.max_iterations or settings.max_search_iterations
    evaluate_results = not args.no_evaluation

    logger.info(f"Running research query: {args.query}")
    logger.info(f"Using model: {model}")
    logger.info(f"Max iterations: {max_iterations}")
    logger.info(f"Evaluation enabled: {evaluate_results}")

    research_agent = ResearchAgent(
        model=model,
        max_iterations=max_iterations,
    )

    evaluator_agent = EvaluatorAgent(model=model) if evaluate_results else None

    # Create and run pipeline
    pipeline = ResearchPipeline(
        agent=research_agent,
        evaluator=evaluator_agent,
        evaluate_results=evaluate_results,
        max_iterations=max_iterations,
    )

    # Run the pipeline
    results = pipeline.run(args.query)

    # Format and display results
    formatted_results = format_research_results(results, args.output_format)
    print(formatted_results)

    # Save to file if specified
    if args.output_file:
        output_dir = os.path.dirname(args.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(args.output_file, "w") as f:
            if args.output_format == "json":
                f.write(formatted_results)
            else:
                f.write(formatted_results)

        logger.info(f"Results saved to: {args.output_file}")


def handle_batch_command(args: argparse.Namespace, settings: Dict[str, Any]) -> None:
    """Handle the 'batch' command.

    Args:
        args: Command-line arguments.
        settings: Application settings.
    """
    # Load queries from input file
    try:
        with open(args.input_file, "r") as f:
            queries = json.load(f)
    except Exception as e:
        logger.error(f"Error loading queries from {args.input_file}: {e}")
        sys.exit(1)

    if not isinstance(queries, list):
        logger.error(f"Input file must contain a JSON array of queries")
        sys.exit(1)

    # Create agents with settings from args (if provided) or environment
    model = args.model or settings.default_model
    max_iterations = args.max_iterations or settings.max_search_iterations
    evaluate_results = not args.no_evaluation
    output_dir = args.output_dir or settings.output_dir

    logger.info(f"Running batch research with {len(queries)} queries")
    logger.info(f"Using model: {model}")
    logger.info(f"Max iterations: {max_iterations}")
    logger.info(f"Evaluation enabled: {evaluate_results}")
    logger.info(f"Output directory: {output_dir}")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    research_agent = ResearchAgent(
        model=model,
        max_iterations=max_iterations,
    )

    evaluator_agent = EvaluatorAgent(model=model) if evaluate_results else None

    # Create and run pipeline
    pipeline = ResearchPipeline(
        agent=research_agent,
        evaluator=evaluator_agent,
        evaluate_results=evaluate_results,
        max_iterations=max_iterations,
        output_dir=output_dir,
    )

    # Run the pipeline for each query
    for i, query in enumerate(queries):
        logger.info(f"Processing query {i+1}/{len(queries)}: {query}")
        
        try:
            results = pipeline.run(query)
            
            # Save results to output directory
            sanitized_query = "".join(c if c.isalnum() else "_" for c in query[:30])
            output_file = os.path.join(output_dir, f"result_{sanitized_query}_{int(time.time())}.json")
            
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
                
            logger.info(f"Results saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")


def handle_settings_command(args: argparse.Namespace, settings: Dict[str, Any]) -> None:
    """Handle the 'settings' command.

    Args:
        args: Command-line arguments.
        settings: Application settings.
    """
    if args.json:
        print(json.dumps(settings.to_dict(), indent=2))
    else:
        print("Current Settings:")
        for key, value in settings.to_dict().items():
            print(f"{key}: {value}")


def main() -> None:
    """Main entry point for the CLI."""
    # Set up argument parser
    parser = setup_argparse()
    args = parser.parse_args()

    # Set up logging
    log_level = args.log_level if args.log_level else os.getenv("LOG_LEVEL", "INFO")
    log_file = args.log_file if args.log_file else os.getenv("LOG_FILE", None)
    setup_logging(log_level=log_level, log_file=log_file)

    # Load settings
    settings = load_settings()

    # Handle commands
    if args.command == "research":
        handle_research_command(args, settings)
    elif args.command == "batch":
        handle_batch_command(args, settings)
    elif args.command == "settings":
        handle_settings_command(args, settings)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main() 