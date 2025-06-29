# Life Sciences Knowledge Graph Agent

## 🎓 Learning Project: LangGraph and Knowledge Graphs

An interactive learning project designed for beginner to advanced users to learn **LangGraph workflows** and **knowledge graph concepts** through practical biomedical AI applications.

## 📚 What You'll Learn

- **Knowledge Graphs**: How to represent domain knowledge as nodes and relationships
- **LangGraph**: Multi-step AI workflows with state management  
- **Cypher Queries**: Graph database query language for complex data retrieval
- **AI Integration**: Combining language models with structured knowledge
- **Biomedical Applications**: Real-world use cases in drug discovery and personalized medicine

## 🚀 Quick Start for Users

1. **Start with the Tutorial**: Open `tutorial_langgraph_knowledge_graphs.ipynb`
2. **Try the Application**: Run the Streamlit app for interactive learning
3. **Follow the Learning Guide**: See `LEARNING_GUIDE.md` for structured curriculum
4. **Practice with Exercises**: Work through progressive challenges in `learning_exercises.py`

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
   cd biomedical_kg_project
   ```

3. **Install dependencies**:
   ```bash
   pdm install
   ```

#### Option 2: Using pip

1. **Clone the repository**:
   ```bash
   cd biomedical_kg_project
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
biomedical_kg_project/
├── src/                      # Source code
│   ├── agents/                  # AI agent implementations
│   │   ├── advanced_ai_agent.py     # 🎓 ACTIVE: Learning-focused LangGraph agent (used in web app)
│   │   ├── workflow_agent.py        # 📚 EXAMPLE: Full-featured LangGraph agent (learning reference)
│   │   ├── template_query_agent.py  # 📚 EXAMPLE: Template-based agent (learning reference)
│   │   └── graph_interface.py     # Neo4j database interface
│   └── web/                     # Streamlit web interface
│       └── app.py                 # Main learning interface
├── docs/                     # Documentation and learning materials
│   ├── exercises/               # Learning exercises
│   │   └── learning_exercises.py  # Progressive challenges
│   ├── tutorials/               # Interactive tutorials
│   │   └── tutorial_langgraph_knowledge_graphs.ipynb
│   └── guides/                  # Learning guides
│       └── LEARNING_GUIDE.md      # 6-week curriculum
├── data/                     # Biomedical CSV datasets
├── docs/                     # Technical documentation
│   ├── ARCHITECTURE.md           # System architecture overview
│   ├── USER_GUIDE.md             # User learning guide
│   ├── DEMO_SCRIPT.md            # Demonstration script
│   ├── SETUP_GUIDE.md            # Setup instructions
│   └── PROJECT_SUMMARY.md        # Project overview
├── scripts/                  # Utility scripts
│   ├── load_data.py              # Full data loader
│   ├── simple_load_data.py       # Simplified data loader
│   └── quickstart.py             # Setup verification
├── tests/                    # Test suite (17 tests)
├── config/                   # Configuration files
│   └── CLAUDE.md                 # Claude Code configuration
├── pyproject.toml            # PDM configuration and dependencies
├── pdm.lock                  # PDM lock file
└── pytest.ini               # Test configuration
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