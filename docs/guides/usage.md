# Usage Guide

This guide explains how to use the Hands-On Deep Research project for conducting research.

## Installation

Before using the project, you need to install it and set up the environment:

```bash
# Clone the repository
git clone https://github.com/xiaoye_hua/hands-on-deep-research.git
cd hands-on-deep-research

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## Configuration

The project uses environment variables for configuration. Create a `.env` file in the root directory:

```bash
# Copy the example configuration
cp .env.example .env

# Edit with your credentials
nano .env
```

Required API keys:
- `OPENAI_API_KEY`: Your OpenAI API key for accessing models like GPT-4.
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key (optional).
- `GOOGLE_API_KEY`: Your Google API key (optional, for web search).
- `GOOGLE_CSE_ID`: Your Google Custom Search Engine ID (optional, for web search).

## Using the Command-Line Interface

The project provides a command-line interface (CLI) for running research tasks.

### Running a Research Task

To run a single research task:

```bash
# Basic usage
poetry run python -m src.cli research "What are the latest advancements in AI research?"

# With custom options
poetry run python -m src.cli research \
  --model "gpt-4" \
  --max-iterations 5 \
  --output-format json \
  --output-file "results/ai_research.json" \
  "What are the latest advancements in AI research?"
```

### Running Multiple Research Tasks

To run multiple research tasks in batch mode:

```bash
# Create a JSON file with queries
echo '["What are the environmental impacts of AI?", "How is AI used in healthcare?"]' > queries.json

# Run batch mode
poetry run python -m src.cli batch \
  --model "gpt-4" \
  --max-iterations 3 \
  --output-dir "results/batch" \
  queries.json
```

### Viewing Settings

To view the current settings:

```bash
# View settings in text format
poetry run python -m src.cli settings

# View settings in JSON format
poetry run python -m src.cli settings --json
```

## Using the Python API

You can also use the project as a Python library in your own code or notebooks.

### Basic Usage

```python
from src.agents.research import ResearchAgent
from src.agents.evaluator import EvaluatorAgent
from src.pipelines.research import ResearchPipeline

# Create agents
research_agent = ResearchAgent(model="gpt-4", max_iterations=3)
evaluator_agent = EvaluatorAgent(model="gpt-4")

# Create pipeline
pipeline = ResearchPipeline(
    agent=research_agent,
    evaluator=evaluator_agent,
    evaluate_results=True,
    save_results=True
)

# Run research
query = "What are the latest advancements in transformer architecture for NLP?"
results = pipeline.run(query)

# Process results
print(f"Research completed in {results['metadata']['duration_seconds']:.2f} seconds")
print(f"Report:\n{results['research']['report']}")
if results.get('evaluation'):
    print(f"Evaluation Score: {results['evaluation']['overall_assessment']['overall_score']}/10")
    print(f"Verdict: {results['evaluation']['overall_assessment']['verdict']}")
```

### Asynchronous Usage

For asynchronous usage in an async context:

```python
import asyncio

async def run_research():
    # Create pipeline as in the previous example
    pipeline = ResearchPipeline(...)
    
    # Run research asynchronously
    results = await pipeline.run_async(query)
    
    return results

# Run the async function
results = asyncio.run(run_research())
```

### Batch Processing

For processing multiple queries:

```python
# Define queries
queries = [
    "What are the environmental impacts of large language models?",
    "How is AI being used in healthcare?"
]

# Run batch processing
results = pipeline.run_batch(queries)

# Process each result
for i, result in enumerate(results):
    print(f"Query {i+1}: {result['query']}")
    print(f"Report: {result['research']['report'][:100]}...")  # Show first 100 chars
```

## Using in Jupyter Notebooks

To use the project in Jupyter notebooks:

```python
import asyncio
import nest_asyncio
import sys
import os

# Add project to path if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

# Apply nest_asyncio to allow running asyncio in Jupyter
nest_asyncio.apply()

# Import and use as in the Python API examples
from src.agents.research import ResearchAgent
# ...rest of the code as above
```

## Advanced Usage

### Customizing Agents

You can customize the behavior of agents by passing different parameters:

```python
# Customize research agent
research_agent = ResearchAgent(
    model="gpt-4",
    temperature=0.7,
    max_tokens=4000,
    max_iterations=5,
    max_concurrent_requests=3,
    timeout=300,
)

# Customize evaluator agent
evaluator_agent = EvaluatorAgent(
    model="gpt-4",
    temperature=0.2,  # Lower temperature for more consistent evaluations
    max_tokens=4000,
)
```

### Extending the Project

To extend the project with custom functionality:

1. **Create Custom Agents**: Inherit from `BaseAgent` and implement the required methods.
2. **Create Custom Pipelines**: Inherit from `BasePipeline` and implement the required methods.
3. **Add New Data Processing Utilities**: Add new functions to the data module.

Example of a custom agent:

```python
from src.agents.base import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, model="gpt-4", **kwargs):
        super().__init__(model, **kwargs)
        # Custom initialization
    
    async def process(self, query):
        # Custom processing logic
        pass
    
    def add_to_context(self, role, content):
        # Custom context management
        pass
    
    def clear_context(self):
        # Custom context clearing
        pass
    
    async def call_model(self, prompt):
        # Custom model calling
        pass
```

## Troubleshooting

### API Key Issues

If you encounter API key errors:

1. Verify that your `.env` file contains the correct API keys.
2. Check that the environment variables are being loaded correctly.
3. Try setting the API keys directly in your code for testing.

### Performance Issues

If you encounter performance issues:

1. Reduce the number of concurrent requests.
2. Reduce the maximum number of iterations.
3. Use a smaller model or lower max_tokens value.
4. Check for network or API rate limiting issues.

### Other Issues

For other issues:

1. Check the logs for error messages.
2. Increase the log level to DEBUG for more detailed information.
3. Check for common issues in the project documentation or issues page.
4. Report an issue on the project's repository. 