"""
Evaluator Agent Implementation.

This module provides the implementation of the evaluator agent,
which is responsible for assessing the quality of research outputs.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union

import openai
from dotenv import load_dotenv

from src.agents.base import BaseAgent
from src.utils.api import get_api_key

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class EvaluatorAgent(BaseAgent):
    """Evaluator agent that assesses the quality of research outputs.

    This agent is responsible for:
    1. Evaluating the completeness of research findings
    2. Checking for factual accuracy and logical consistency
    3. Identifying gaps or biases in the research
    4. Providing quality metrics and overall assessment
    """

    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.2,  # Lower temperature for more consistent evaluations
        max_tokens: int = 4000,
        **kwargs: Any,
    ) -> None:
        """Initialize the evaluator agent.

        Args:
            model: The language model to use for the agent.
            temperature: Sampling temperature for the model.
            max_tokens: Maximum number of tokens for model responses.
            **kwargs: Additional keyword arguments for the agent.
        """
        super().__init__(model, temperature, max_tokens, **kwargs)
        self.openai_api_key = get_api_key("OPENAI_API_KEY")
        self.system_prompt = (
            "You are an evaluator AI responsible for assessing the quality of research reports. "
            "Your job is to critically analyze research findings and reports, checking for "
            "completeness, factual accuracy, logical consistency, and potential biases or gaps. "
            "You should provide a fair and balanced assessment, identifying both strengths and "
            "weaknesses of the research."
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

    async def evaluate_completeness(self, query: str, report: str) -> Dict[str, Any]:
        """Evaluate the completeness of the research report.

        Args:
            query: The original research query.
            report: The research report to evaluate.

        Returns:
            A dictionary containing the completeness evaluation.
        """
        prompt = (
            f"Evaluate the completeness of the following research report in addressing "
            f"the original query: '{query}'. Identify any significant gaps or missing "
            f"information that would be important for a comprehensive answer.\n\n"
            f"Research report:\n{report}\n\n"
            f"Score the completeness on a scale of 1-10, where 10 is perfectly complete. "
            f"Provide a detailed explanation of your rating."
        )
        self.add_to_context("user", prompt)
        response = await self.call_model(self.context)
        self.add_to_context("assistant", response)

        # Extract score using simple heuristic (find first number 1-10 in the response)
        score = None
        for word in response.split():
            if word.strip(",.()[]{}:;").isdigit():
                num = int(word.strip(",.()[]{}:;"))
                if 1 <= num <= 10:
                    score = num
                    break

        if score is None:
            score = 5  # Default middle score if we couldn't extract one

        return {
            "aspect": "completeness",
            "score": score,
            "explanation": response,
        }

    async def evaluate_accuracy(self, report: str, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate the factual accuracy of the research report.

        Args:
            report: The research report to evaluate.
            findings: The research findings used to create the report.

        Returns:
            A dictionary containing the accuracy evaluation.
        """
        findings_summary = "\n\n".join(
            [f"Source: {finding['url']}\nSummary: {finding['summary']}" for finding in findings]
        )
        prompt = (
            f"Evaluate the factual accuracy of the following research report by comparing it "
            f"to the original findings. Identify any factual errors, misrepresentations, or "
            f"unsupported claims.\n\n"
            f"Research findings:\n{findings_summary}\n\n"
            f"Research report:\n{report}\n\n"
            f"Score the factual accuracy on a scale of 1-10, where 10 is perfectly accurate. "
            f"Provide a detailed explanation of your rating."
        )
        self.add_to_context("user", prompt)
        response = await self.call_model(self.context)
        self.add_to_context("assistant", response)

        # Extract score using simple heuristic
        score = None
        for word in response.split():
            if word.strip(",.()[]{}:;").isdigit():
                num = int(word.strip(",.()[]{}:;"))
                if 1 <= num <= 10:
                    score = num
                    break

        if score is None:
            score = 5  # Default middle score if we couldn't extract one

        return {
            "aspect": "factual_accuracy",
            "score": score,
            "explanation": response,
        }

    async def evaluate_bias(self, report: str) -> Dict[str, Any]:
        """Evaluate the report for potential biases.

        Args:
            report: The research report to evaluate.

        Returns:
            A dictionary containing the bias evaluation.
        """
        prompt = (
            f"Evaluate the following research report for potential biases, one-sided "
            f"perspectives, or lack of balanced consideration of different viewpoints. "
            f"Identify any instances where the report may present a skewed or incomplete "
            f"picture of the topic.\n\n"
            f"Research report:\n{report}\n\n"
            f"Score the neutrality on a scale of 1-10, where 10 is perfectly neutral and "
            f"balanced. Provide a detailed explanation of your rating."
        )
        self.add_to_context("user", prompt)
        response = await self.call_model(self.context)
        self.add_to_context("assistant", response)

        # Extract score using simple heuristic
        score = None
        for word in response.split():
            if word.strip(",.()[]{}:;").isdigit():
                num = int(word.strip(",.()[]{}:;"))
                if 1 <= num <= 10:
                    score = num
                    break

        if score is None:
            score = 5  # Default middle score if we couldn't extract one

        return {
            "aspect": "neutrality",
            "score": score,
            "explanation": response,
        }

    async def generate_overall_assessment(self, evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate an overall assessment based on all evaluations.

        Args:
            evaluations: The list of aspect evaluations.

        Returns:
            A dictionary containing the overall assessment.
        """
        evaluations_summary = "\n\n".join(
            [
                f"Aspect: {eval['aspect']}\nScore: {eval['score']}/10\nExplanation: {eval['explanation']}"
                for eval in evaluations
            ]
        )
        prompt = (
            f"Based on the following detailed evaluations of different aspects of a research "
            f"report, provide an overall assessment of the report's quality. Consider the "
            f"relative importance of each aspect and provide a final score and verdict.\n\n"
            f"Evaluations:\n{evaluations_summary}\n\n"
            f"Provide your overall assessment, including:\n"
            f"1. A final score on a scale of 1-10\n"
            f"2. A verdict (Excellent, Good, Satisfactory, Needs Improvement, or Inadequate)\n"
            f"3. A summary of key strengths and weaknesses\n"
            f"4. Suggestions for improvement"
        )
        self.add_to_context("user", prompt)
        response = await self.call_model(self.context)
        self.add_to_context("assistant", response)

        # Extract overall score using simple heuristic
        score = None
        for word in response.split():
            if word.strip(",.()[]{}:;").isdigit():
                num = int(word.strip(",.()[]{}:;"))
                if 1 <= num <= 10:
                    score = num
                    break

        if score is None:
            # Calculate average of aspect scores if we couldn't extract one
            aspect_scores = [eval["score"] for eval in evaluations]
            score = sum(aspect_scores) / len(aspect_scores) if aspect_scores else 5

        # Extract verdict using simple keyword matching
        verdict = "Satisfactory"  # Default
        if "excellent" in response.lower():
            verdict = "Excellent"
        elif "good" in response.lower():
            verdict = "Good"
        elif "needs improvement" in response.lower():
            verdict = "Needs Improvement"
        elif "inadequate" in response.lower():
            verdict = "Inadequate"

        return {
            "overall_score": score,
            "verdict": verdict,
            "assessment": response,
        }

    async def process(self, query: str, report: str, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process an evaluation request and return the results.

        Args:
            query: The original research query.
            report: The research report to evaluate.
            findings: The research findings used to create the report.

        Returns:
            A dictionary containing the evaluation results.
        """
        self.clear_context()
        
        # Evaluate different aspects of the report
        completeness_eval = await self.evaluate_completeness(query, report)
        accuracy_eval = await self.evaluate_accuracy(report, findings)
        bias_eval = await self.evaluate_bias(report)
        
        evaluations = [completeness_eval, accuracy_eval, bias_eval]
        
        # Generate overall assessment
        overall_assessment = await self.generate_overall_assessment(evaluations)
        
        return {
            "query": query,
            "evaluations": {
                "completeness": completeness_eval,
                "factual_accuracy": accuracy_eval,
                "neutrality": bias_eval,
            },
            "overall_assessment": overall_assessment,
        } 