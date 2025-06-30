# 🧬 Helix Navigator

## 🎓 Learning Project: LangGraph and Knowledge Graphs

An interactive educational project for learning **LangGraph workflows** and **knowledge graph concepts** through hands-on biomedical AI applications. Navigate the complex world of life sciences data with AI-powered discovery. Progress from beginner to advanced with real-world examples.

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

## 🛠️ Technology Stack

- **Frontend**: Streamlit (interactive web interface)
- **AI Framework**: LangGraph (workflow orchestration)
- **Language Model**: Anthropic Claude (natural language processing)
- **Database**: Neo4j (graph database)
- **Package Manager**: PDM (modern Python dependency management)

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
   pip install -e .
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
│   │   ├── advanced_workflow_agent.py # 📚 EXAMPLE: Production LangGraph patterns (learning reference)
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

## 🎯 Progressive Learning Architecture

The project provides **three different agent implementations** to demonstrate various approaches:

### 🎓 **WorkflowAgent** (Primary - Used in Web App)
- **Educational LangGraph implementation** optimized for learning
- **5-step workflow**: Classify → Extract → Generate → Execute → Format
- **Transparent processing** with detailed comments and print statements
- **Perfect for understanding** core LangGraph concepts and biomedical AI

### 📚 **AdvancedWorkflowAgent** (Reference - Production Patterns)
- **Production-ready LangGraph** with advanced error handling and monitoring
- **Same core workflow** as WorkflowAgent but with enterprise features
- **Demonstrates evolution** from educational prototype to production system
- **Learn advanced patterns**: conditional routing, query validation, comprehensive logging

### 📚 **TemplateQueryAgent** (Reference - High Performance)
- **Template-based approach** using pre-written Cypher queries
- **Lightning fast**: ~200ms vs ~3-5 seconds for AI agents
- **100% deterministic** results with no AI inference overhead
- **Perfect for learning** direct graph database query construction

### 🎯 **Learning Progression**
1. **Start with WorkflowAgent** to understand LangGraph fundamentals
2. **Study AdvancedWorkflowAgent** to see production engineering patterns  
3. **Compare with TemplateQueryAgent** to understand performance trade-offs
4. **Build your own** agents combining the best of all approaches

## 📖 Learning Resources

- **📖 Foundations Guide**: Complete background for beginners ([foundations-and-background.md](docs/foundations-and-background.md))
- **📔 Tutorial Notebook**: Step-by-step interactive learning
- **🎓 Learning Mode**: Streamlit interface with exercises
- **📚 Learning Guide**: Progressive skill development
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

