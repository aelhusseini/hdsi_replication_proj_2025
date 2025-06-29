# Life Sciences Knowledge Graph Agent

## 🎓 Learning Project: LangGraph and Knowledge Graphs

An interactive learning project designed for beginner to advanced users to learn **LangGraph workflows** and **knowledge graph concepts** through practical biomedical AI applications.

**New to AI, knowledge graphs, or biomedical concepts?** Start with our comprehensive [Foundations and Background Guide](docs/foundations-and-background.md) - designed for users with zero prior knowledge to understand and appreciate every aspect of this project.

## 📚 What You'll Learn

- **Knowledge Graphs**: How to represent domain knowledge as nodes and relationships
- **LangGraph**: Multi-step AI workflows with state management  
- **Cypher Queries**: Graph database query language for complex data retrieval
- **AI Integration**: Combining language models with structured knowledge
- **Biomedical Applications**: Real-world use cases in drug discovery and personalized medicine

## 🚀 Quick Start for Users

1. **Complete Beginner?** Read the [Foundations and Background Guide](docs/foundations-and-background.md) first
2. **Start with Setup**: Follow `docs/getting-started.md` for complete setup instructions
3. **Try the Application**: Run the Streamlit app for interactive learning
4. **Follow the Tutorial**: Open `docs/tutorials/langgraph-tutorial.ipynb`
5. **Practice with Exercises**: Work through progressive challenges in `docs/exercises/practice-exercises.py`

## Technology Stack

- **Frontend**: Streamlit
- **Agent Framework**: LangGraph
- **LLM**: Anthropic Claude
- **Database**: Neo4j
- **Package Manager**: PDM

## Setup Instructions

### Prerequisites

- Python 3.10+
- Neo4j Community Edition
- PDM (Python Dependency Manager)

### Installation

#### Option 1: Using PDM (Recommended)

1. **Install PDM** (if not already installed):
   ```bash
   curl -sSL https://pdm.fming.dev/install-pdm.py | python3 -
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hdsi_replication_proj_2025
   ```

3. **Install dependencies**:
   ```bash
   pdm install
   ```

#### Option 2: Using pip

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hdsi_replication_proj_2025
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pdm install
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Anthropic API key and Neo4j credentials
   ```

5. **Install and start Neo4j**:
   - Download Neo4j Community Edition from https://neo4j.com/download/
   - Start the Neo4j server
   - Set your password (update it in .env)

## Project Structure

```
hdsi_replication_proj_2025/
├── src/                      # Source code
│   ├── agents/                  # AI agent implementations
│   │   ├── workflow_agent.py        # 🎓 ACTIVE: Full-featured LangGraph agent (used in web app)
│   │   ├── advanced_ai_agent.py     # 📚 EXAMPLE: Simplified LangGraph agent (learning reference)
│   │   ├── template_query_agent.py  # 📚 EXAMPLE: Template-based agent (learning reference)
│   │   └── graph_interface.py       # Neo4j database interface
│   └── web/                     # Streamlit web interface
│       └── app.py                   # Main learning interface
├── docs/                     # Documentation and learning materials
│   ├── foundations-and-background.md # Complete beginner's guide (start here!)
│   ├── getting-started.md          # Complete setup guide
│   ├── reference.md               # Commands and demo script
│   ├── technical-guide.md         # Architecture and development
│   ├── exercises/                 # Learning exercises
│   │   └── practice-exercises.py    # Progressive challenges
│   └── tutorials/                 # Interactive tutorials
│       └── langgraph-tutorial.ipynb # Hands-on LangGraph tutorial
├── data/                     # Biomedical CSV datasets
├── scripts/                  # Utility scripts
│   ├── load_data.py              # Full data loader
│   ├── simple_load_data.py       # Simplified data loader
│   └── quickstart.py             # Setup verification
├── tests/                    # Test suite (27 tests)
├── CLAUDE.md                 # Claude Code configuration
├── pyproject.toml            # PDM configuration and dependencies
└── .env.example              # Environment variables template
```

## 🏃‍♂️ Running the Application

### For Users (Recommended)
1. **Load sample data**:
   ```bash
   pdm run load-data
   ```

2. **Start learning with the tutorial**:
   ```bash
   jupyter notebook docs/tutorials/langgraph-tutorial.ipynb
   ```

3. **Try the interactive app**:
   ```bash
   pdm run app
   ```
   Then explore the interactive learning interface.

4. **Verify everything works**:
   ```bash
   pdm run quickstart
   ```

### For Developers
- Format code: `pdm run format`
- Run linting: `pdm run lint`
- Run tests: `pdm run test`

## 🎯 Learning Objectives

This project teaches you to:

1. **Design Knowledge Graphs**
   - Model domain relationships as nodes and edges
   - Understand graph vs. relational database trade-offs

2. **Master Cypher Queries**
   - Write simple to complex graph traversal queries
   - Optimize for performance and readability

3. **Build LangGraph Workflows**
   - Create multi-step AI reasoning processes
   - Manage state flow between processing nodes

4. **Apply to Biomedical AI**
   - Understand real-world applications in drug discovery
   - Build domain-specific AI assistants

## 📖 Learning Resources

- **📖 Foundations Guide**: Complete background for beginners ([foundations-and-background.md](docs/foundations-and-background.md))
- **📔 Tutorial Notebook**: Step-by-step interactive learning
- **🎓 Learning Mode**: Streamlit interface with exercises
- **📚 Learning Guide**: Structured 6-week curriculum
- **🏋️ Progressive Exercises**: From beginner to expert level
- **🔧 Example Code**: Three different agent implementations

## 💡 Example Learning Questions

Start your exploration with these questions:

**Knowledge Graph Basics:**
- How do biological entities naturally form graph relationships?
- What makes graph databases better for biomedical data?

**Cypher Query Practice:**
- "Find genes on chromosome 1 that encode proteins"
- "Discover complete pathways from genes to treatments"

**LangGraph Workflow Building:**
- How does state flow through multi-step AI reasoning?
- When should you use templates vs. AI-generated queries?

**Real-World Applications:**
- How might this approach help drug discovery?
- What are the ethical considerations for biomedical AI?

## License

MIT License