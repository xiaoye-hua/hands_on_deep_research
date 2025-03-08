# Hands-On Deep Research

A Python-based deep research project inspired by Hugging Face's open-deep-research approach. This project provides a framework for conducting deep research tasks, enabling the creation of multi-agent research systems that understand their knowledge boundaries and can learn iteratively.

## 🚀 Features

- **Modular Architecture**: Organized as a structured Python package with clear separation of concerns
- **Multi-Agent System**: Framework for creating and coordinating different research agents
- **Knowledge Awareness**: Agents designed to understand what they know and don't know
- **Iterative Research**: Ability to refine search queries and knowledge collection process
- **Reproducible Research**: Tools for documenting research findings and processes
- **Web Search Integration**: DuckDuckGo search implementation that doesn't require API keys
- **Content Processing**: Fetch and analyze web content to extract relevant information

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
- `OPENAI_API_KEY`: Your OpenAI API key for accessing models like GPT-4.

Optional API keys:
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key (for future extensions).
- `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`: For Google Custom Search (alternative to DuckDuckGo).

Note: The current implementation uses DuckDuckGo for web searches, which doesn't require API keys.

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
poetry run python -m src.cli research --model gpt-4 --max-iterations 5 --output-format json --output-file "results/ai_research.json" "What are the latest advances in transformer architecture for NLP?"
```

### Using Example Scripts

```bash
# Run the simple research example
poetry run python examples/simple_research.py "Your research question here" --max-iterations 3
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- User Guides: `docs/guides/`
- API Documentation: `docs/api/`

## 🧪 Testing

Run tests using pytest:

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=src
```

## 🚀 Next Steps

This project is under active development. Here are some planned improvements:

1. **Improve DuckDuckGo Integration**:
   - Handle HTTP 202 responses and other edge cases
   - Implement rate limiting and retry mechanisms
   - Add support for different search regions and languages

2. **Enhance Web Content Processing**:
   - Improve HTML parsing for better content extraction
   - Add support for PDFs, images, and other media
   - Implement content summarization techniques

3. **Expand Search Sources**:
   - Add support for academic databases (e.g., Semantic Scholar, ArXiv)
   - Implement specialized search for news, social media, etc.
   - Create adaptable search strategies based on query type

4. **Improve Evaluation**:
   - Enhance evaluation metrics for research quality
   - Implement fact-checking mechanisms
   - Add source credibility assessment

5. **User Interface Improvements**:
   - Create a web interface using Streamlit or Gradio
   - Implement interactive visualization of research findings
   - Add real-time progress tracking

6. **Performance Optimization**:
   - Implement caching for search results and model calls
   - Optimize parallel processing for large-scale research
   - Add distributed processing capabilities

Contributions to any of these areas are welcome!

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
