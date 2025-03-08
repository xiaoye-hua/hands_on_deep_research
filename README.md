# Hands-On Deep Research

A Python-based deep research project inspired by Hugging Face's open-deep-research approach. This project provides a framework for conducting deep research tasks, enabling the creation of multi-agent research systems that understand their knowledge boundaries and can learn iteratively.

## 🚀 Features

- **Modular Architecture**: Organized as a structured Python package with clear separation of concerns
- **Multi-Agent System**: Framework for creating and coordinating different research agents
- **Knowledge Awareness**: Agents designed to understand what they know and don't know
- **Iterative Research**: Ability to refine search queries and knowledge collection process
- **Reproducible Research**: Tools for documenting research findings and processes

## 📋 Project Structure

```
hands-on-deep-research/
├── data/                    # Data storage
│   ├── raw/                 # Raw, immutable data
│   ├── processed/           # Processed data ready for analysis
│   └── external/            # Data from external sources
├── docs/                    # Documentation
│   ├── guides/              # User guides and tutorials
│   └── api/                 # API documentation
├── models/                  # Trained models
├── results/                 # Experiment results and outputs
├── src/                     # Source code
│   ├── agents/              # Agent implementations
│   ├── config/              # Configuration files
│   ├── data/                # Data processing scripts
│   ├── models/              # Model implementations
│   ├── notebooks/           # Jupyter notebooks
│   ├── pipelines/           # Research pipelines
│   ├── utils/               # Utility functions
│   └── visualization/       # Visualization tools
├── tests/                   # Test code
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── examples/                # Example scripts and notebooks
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore file
├── pyproject.toml           # Project configuration and dependencies
└── README.md                # This file
```

## 🔧 Installation

This project uses Poetry for dependency management. To install:

```bash
# Clone the repository
git clone https://github.com/xiaoye_hua/hands-on-deep-research.git
cd hands-on-deep-research

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## 🔑 Configuration

Create a `.env` file in the root directory with your API keys:

```bash
# Copy the example configuration
cp .env.example .env

# Edit with your credentials
nano .env
```

Required API keys:
- OpenAI API key
- Hugging Face API key
- Google Custom Search API key (optional)

## 💻 Usage

### Basic Example

```python
from src.agents import ResearchAgent
from src.pipelines import ResearchPipeline

# Initialize a research agent
agent = ResearchAgent(model="gpt-4")

# Create a research pipeline
pipeline = ResearchPipeline(agent=agent)

# Run a research task
results = pipeline.run("What are the latest advances in transformer architecture for NLP?")
```

### Running from Command Line

```bash
# Run a basic research task
poetry run python -m src.cli research "What are the latest advances in transformer architecture for NLP?"

# Run with advanced options
poetry run python -m src.cli research --model gpt-4 --max-iterations 5 --output-format json "What are the latest advances in transformer architecture for NLP?"
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- User Guides: `docs/guides/`
- API Documentation: `docs/api/`
- Logging System: `docs/logging.md`

## 🧪 Testing

Run tests using pytest:

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=src
```

## 🛠️ Development

This project includes a Makefile to simplify common development tasks:

```bash
# Show available commands
make help

# Run all tests
make test

# Run tests for specific components
make test-tools
make test-python-runner

# Run linting checks
make lint

# Format code
make format

# Generate coverage report
make coverage

# Clean build artifacts
make clean

# Run pre-commit hooks
make pre-commit
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Inspired by Hugging Face's open-deep-research
- Built with Poetry, PyTorch, and Transformers
