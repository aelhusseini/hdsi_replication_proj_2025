# 🚀 Getting Started

Complete guide to setting up and using the Life Sciences Knowledge Graph Agent platform.

## 🎯 What You'll Learn

Build real AI systems that combine:
- **Knowledge Graphs** with biomedical data (genes, proteins, diseases, drugs)
- **LangGraph Workflows** for AI agent state management
- **Cypher Queries** for graph database interactions
- **Biomedical AI Applications** for healthcare and research

## 📋 Prerequisites

### Required Software
- **Python 3.10+** ([Download](https://python.org))
- **Neo4j Desktop** ([Download](https://neo4j.com/download/)) OR Docker
- **Git** for cloning the repository

### Required Accounts
- **Anthropic API Key** ([Get free credits](https://console.anthropic.com/))

## ⚙️ Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd biomedical_kg_project

# Install dependencies
pdm install

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment
Edit `.env` file:
```bash
# Anthropic API (get free credits at console.anthropic.com)
ANTHROPIC_API_KEY=sk-ant-your_api_key_here

# Neo4j Database (local)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
```

### 3. Start Neo4j Database

**Option A: Neo4j Desktop (Recommended)**
1. Install Neo4j Desktop
2. Create new project → Add local DBMS
3. Set password (use same as `.env` file)
4. Start the database

**Option B: Docker**
```bash
docker run \
    --name neo4j-learning \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/your_password \
    neo4j:latest
```

### 4. Load Sample Data
```bash
# Load sample biomedical dataset
pdm run load-data

# Verify setup
pdm run quickstart
```

### 5. Launch Platform
```bash
# Start web interface
pdm run app

# Open browser to http://localhost:8501
```

## 🎓 Platform Interface

### Main Learning Tabs

**📚 Concepts** - Learn fundamentals:
- Knowledge graph basics
- LangGraph workflow steps
- Cypher query syntax
- Biomedical applications

**🧪 Try the Agent** - Interactive demos:
- Ask questions and see step-by-step processing
- View generated Cypher queries
- Understand LangGraph state management
- See real biomedical AI in action

**🔍 Explore Queries** - Practice Cypher:
- Pre-built query examples
- Write custom queries
- Immediate results and feedback
- Network visualizations

**🏋️ Exercises** - Progressive challenges:
- Level 1: Basic node and relationship queries
- Level 2: Pattern matching and filtering
- Level 3: Complex multi-hop relationships
- Level 4: Advanced pathway analysis

## 🧬 Sample Data Overview

Our sample dataset includes:
- **Genes**: GENE_ALPHA, GENE_BETA, GENE_GAMMA...
- **Proteins**: PROT_ALPHA, PROT_BETA, PROT_GAMMA...
- **Diseases**: diabetes, hypertension, cancer...
- **Drugs**: AlphaCure, BetaTherapy, GammaRx...

**Relationships**:
```
Gene --[ENCODES]--> Protein
Gene --[LINKED_TO]--> Disease
Protein --[ASSOCIATED_WITH]--> Disease
Drug --[TREATS]--> Disease
Drug --[TARGETS]--> Protein
```

## 🎯 Learning Path

### Week 1-2: Fundamentals
1. Complete setup and data loading
2. Explore **Concepts** tab thoroughly
3. Try example questions in **Try the Agent**
4. Practice basic queries in **Explore Queries**

### Week 3-4: Building Skills
1. Work through **Exercises** Level 1-2
2. Study the generated Cypher queries
3. Open [langgraph-tutorial.ipynb](tutorials/langgraph-tutorial.ipynb)
4. Practice with [practice-exercises.py](exercises/practice-exercises.py)

### Week 5-6: Advanced Applications
1. Complete **Exercises** Level 3-4
2. Study [technical-guide.md](technical-guide.md)
3. Build custom agents using the patterns
4. Present using the demo script in [reference.md](reference.md)

## 🔧 Development Commands

```bash
# Run all tests (should see 27 passed)
pdm run test

# Code formatting and linting
pdm run format && pdm run lint

# Load larger dataset (advanced)
python scripts/load_data.py

# Quick system check
pdm run quickstart
```

## 🆘 Troubleshooting

### "Neo4j Connection Failed"
1. Verify Neo4j is running (check Neo4j Desktop)
2. Check password in `.env` matches database
3. Try: `pdm run quickstart` for diagnostics

### "No Results Found"
1. Ensure data is loaded: `pdm run load-data`
2. Use sample entity names: `GENE_ALPHA`, `diabetes`, `AlphaCure`
3. Start with simpler queries

### "API Key Not Working"
1. Check `.env` has correct `ANTHROPIC_API_KEY`
2. Ensure key starts with `sk-ant-`
3. Visit [console.anthropic.com](https://console.anthropic.com/) for credits

### "Import Errors"
1. Run from project root directory
2. Reinstall: `pdm install`
3. Check Python version: `python --version` (needs 3.10+)

## 🎉 What's Next?

Once you have the platform running:
1. **Explore freely** - Click around and experiment
2. **Ask questions** - Try your own biomedical queries
3. **Study patterns** - Look at the generated Cypher queries
4. **Build projects** - Use the platform as foundation for your own ideas

The platform is designed for hands-on learning - the best way to understand knowledge graphs and LangGraph is to use them!

---

*Need help? Check [reference.md](reference.md) for quick syntax help or [technical-guide.md](technical-guide.md) for implementation details.*