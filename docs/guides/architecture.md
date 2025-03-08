# Architecture Overview

This document provides an overview of the Hands-On Deep Research project architecture, explaining the key components and how they interact.

## System Architecture

The Hands-On Deep Research project follows a modular architecture with clear separation of concerns. The main components are:

```
                    ┌───────────────┐
                    │     CLI       │
                    └───────┬───────┘
                            │
                            ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Settings     │◄───┤   Pipeline    │───►│   Data Utils   │
└───────────────┘    └───────┬───────┘    └───────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
    ┌───────────────┐         ┌───────────────┐
    │Research Agent │         │Evaluator Agent│
    └───────────────┘         └───────────────┘
```

## Key Components

### Agents

The agents are responsible for specific tasks in the research process:

- **BaseAgent**: Abstract base class that defines the common interface for all agents.
- **ResearchAgent**: Responsible for generating search queries, processing search results, and compiling findings into a report.
- **EvaluatorAgent**: Responsible for evaluating the quality of research findings and reports.

### Pipelines

The pipelines orchestrate the research process:

- **BasePipeline**: Abstract base class that defines the common interface for all pipelines.
- **ResearchPipeline**: Coordinates the research process, delegating tasks to the appropriate agents and managing the overall flow.

### Data Utilities

The data utilities provide functionality for processing and handling data:

- **Text Processing**: Functions for cleaning and extracting information from text.
- **Web Utilities**: Functions for fetching and parsing web content.

### Configuration

The configuration components manage application settings:

- **Settings**: Dataclass that holds application settings loaded from environment variables.
- **Settings Loading**: Functions for loading and validating settings.

### CLI

The command-line interface provides a way to interact with the system:

- **Main CLI**: Entry point for the CLI with argument parsing and command handling.
- **Commands**: Implementation of various commands (research, batch, settings).

## Flow of Execution

1. **Setup**: The application loads settings from environment variables and initializes the appropriate components.
2. **Query Processing**: The research pipeline receives a query and delegates it to the research agent.
3. **Search**: The research agent generates search queries and performs searches.
4. **Information Extraction**: The research agent processes search results to extract relevant information.
5. **Report Generation**: The research agent compiles findings into a comprehensive report.
6. **Evaluation**: The evaluator agent assesses the quality of the research findings and report.
7. **Results**: The pipeline returns the research results and evaluation to the caller.

## Asynchronous Design

The project uses asynchronous programming (async/await) to handle I/O-bound operations efficiently:

- **Concurrent Searches**: Multiple search queries can be executed concurrently.
- **Concurrent Processing**: Multiple search results can be processed concurrently.
- **Synchronous Wrappers**: Synchronous wrappers are provided for convenience when async is not needed.

## Extensibility

The architecture is designed to be extensible:

- **Custom Agents**: New types of agents can be added by inheriting from BaseAgent.
- **Custom Pipelines**: New types of pipelines can be added by inheriting from BasePipeline.
- **Custom Data Processing**: Additional data processing utilities can be added as needed.

## Best Practices

The project follows several best practices:

- **Type Annotations**: All functions and classes use type annotations for better code understanding and static type checking.
- **Documentation**: Comprehensive docstrings and documentation provide clear explanations of functionality.
- **Error Handling**: Robust error handling ensures graceful failure and helpful error messages.
- **Configuration**: Flexible configuration through environment variables for easy deployment in different environments.
- **Testing**: Unit tests ensure the reliability of key components. 