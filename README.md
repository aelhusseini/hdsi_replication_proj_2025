# Helix Navigator

**Learn LangGraph and Knowledge Graphs through Biomedical AI**

An interactive educational project that teaches modern AI development through hands-on biomedical applications. Build AI agents that answer complex questions about genes, proteins, diseases, and drugs using graph databases and multi-step AI workflows.


## What You'll Learn

- **Knowledge Graphs**: Represent domain knowledge as nodes and relationships
- **LangGraph**: Build multi-step AI workflows with state management  
- **Cypher Queries**: Query graph databases effectively
- **AI Integration**: Combine language models with structured knowledge
- **Biomedical Applications**: Apply AI to drug discovery and personalized medicine

## Quick Start

1. **New to these concepts?** Read the [Foundations Guide](docs/foundations-and-background.md)
2. **Setup**: Follow [Getting Started](docs/getting-started.md) for installation
3. **Learn**: Try the interactive tutorial: `docs/tutorials/langgraph-tutorial.ipynb`
4. **Practice**: Work through exercises in `docs/exercises/practice-exercises.py`

## Technology Stack

- **LangGraph**: AI workflow orchestration
- **Neo4j**: Graph database
- **Anthropic Claude**: Language model
- **Streamlit**: Interactive web interface
- **LangGraph Studio**: Visual debugging

## Installation

**Quick Setup**: Python 3.10+, Neo4j, PDM

```bash
# Install dependencies
pdm install

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Load data and start
pdm run load-data
pdm run app
```

**Detailed instructions**: See [Getting Started](docs/getting-started.md)

## Project Structure

```
├── src/agents/              # AI agent implementations
├── src/web/app.py          # Interactive Streamlit interface
├── docs/                   # Documentation and tutorials
├── data/                   # Biomedical datasets
├── scripts/                # Data loading utilities
└── tests/                  # Test suite
```

**Key Files**:
- `src/agents/workflow_agent.py` - Main educational LangGraph agent
- `docs/tutorials/langgraph-tutorial.ipynb` - Interactive tutorial
- `docs/exercises/practice-exercises.py` - Progressive challenges

## Running the Application

### Basic Usage
```bash
pdm run load-data         # Load biomedical data
pdm run app              # Start web interface
```

### Visual Debugging
```bash
pdm run langgraph    # Start LangGraph Studio
```

### Development
```bash
pdm run test            # Run tests (27 tests)
pdm run format          # Format code
pdm run lint            # Check quality
```

**Full commands**: See [Reference Guide](docs/reference.md)

## AI Agent

**WorkflowAgent** - LangGraph implementation with transparent processing for learning core LangGraph concepts through biomedical applications

## Example Questions

- **"What protein does TP53 encode?"** 
- **"What diseases is BRCA1 linked to?"** 
- **"What drugs treat hypertension?"** 
- **"What drugs treat Alzheimer_Disease?"** 
- **"What genes are associated with diabetes?"** 
- **"What genes are linked to both diabetes and hypertension?"** 
- **"Which genes are linked to neurological disorders?"** 
- **"What proteins are associated with cancer?"** 

