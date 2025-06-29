# 🚀 Getting Started

Complete guide to setting up and using the Life Sciences Knowledge Graph Agent platform.

**🆕 New to AI, knowledge graphs, or biomedical concepts?** Start with our [Foundations and Background Guide](foundations-and-background.md) - a comprehensive resource designed for complete beginners to understand the technologies and concepts used in this project.

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
cd hdsi_replication_proj_2025

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

### 4. Generate and Load Sample Data
```bash
# Generate expanded biomedical dataset (500 genes, 191 diseases, 350 drugs)
pdm run generate-data

# Load biomedical dataset into Neo4j
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

Our comprehensive synthetic dataset includes:
- **500 Genes**: Real gene families (TP53, BRCA1/2, KRAS, PIK3, EGFR, etc.) + synthetic genes
- **661 Proteins**: Encoded proteins with realistic molecular weights and structures  
- **191 Diseases**: Across 15 medical categories (cardiovascular, oncology, neurological, psychiatric, metabolic, autoimmune, respiratory, infectious, genetic, pediatric, geriatric, etc.)
- **350 Drugs**: Multiple drug classes (small molecules, biologics, gene therapies) with real drug names
- **3,200+ Relationships**: Complex biomedical networks and pathways

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
1. **Read background materials**: Review [foundations-and-background.md](foundations-and-background.md) if new to these concepts
2. Complete setup and data loading
3. Explore **Concepts** tab thoroughly
4. Try example questions in **Try the Agent**
5. Practice basic queries in **Explore Queries**

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
1. Ensure data is loaded: `pdm run generate-data && pdm run load-data`
2. Use entity names from expanded dataset: `TP53`, `BRCA1`, `Type2_Diabetes`, `Atorvastatin`
3. Start with simpler queries in the Explore Queries tab

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
4. **Master the platform** - Understand all features and capabilities thoroughly

The platform is designed for hands-on learning - the best way to understand knowledge graphs and LangGraph is to use them!

---

*Need help? Check [foundations-and-background.md](foundations-and-background.md) for complete background, [reference.md](reference.md) for quick syntax help, or [technical-guide.md](technical-guide.md) for implementation details.*