"""
Agents module for the Hands-On Deep Research project.

This module contains implementations of various research agents
that can be used for collecting and processing information.
"""

from src.agents.base import BaseAgent
from src.agents.research import ResearchAgent
from src.agents.evaluator import EvaluatorAgent

__all__ = ["BaseAgent", "ResearchAgent", "EvaluatorAgent"] 