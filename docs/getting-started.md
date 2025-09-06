# Getting Started

Complete setup guide for Helix Navigator.

**New to these concepts?** Start with the [Foundations Guide](foundations-and-background.md) for essential background.

## What You'll Build

AI systems that combine:
- Knowledge graphs with biomedical data
- LangGraph workflows for AI agent state management
- Cypher queries for graph database interactions
- Biomedical AI applications for healthcare research

## Prerequisites

**Software**:
- Python 3.10+
- Neo4j Desktop
- Git

**API Keys**:
- Anthropic API key (get free credits at console.anthropic.com)
- LangSmith API key (optional, for LangGraph Studio debugging)

## Installation

### 1. Setup Project
```bash
git clone <repository-url>
cd hdsi_replication_proj_2025
pdm install
cp .env.example .env
```

### 2. Configure Environment
Edit `.env` with your API keys:
```bash
ANTHROPIC_API_KEY=sk-ant-your_key_here
NEO4J_PASSWORD=your_password
LANGSMITH_API_KEY=lsv2_pt_your_key_here  
```

### 3. Start Database

**Neo4j Desktop** (Recommended):
1. Download and install Neo4j Desktop from [neo4j.com/download](https://neo4j.com/download/)
2. Create a new project → Add local DBMS
3. Set database name (e.g., "helix-navigator") 
4. Set password (must match NEO4J_PASSWORD in your .env file)
5. Start the database (green play button)
6. Verify connection: Neo4j Browser opens at http://localhost:7474

**Alternative - Neo4j Aura (Cloud)**:
1. Create free account at [neo4j.com/aura](https://neo4j.com/aura/)
2. Create database instance
3. Update .env with provided connection details

### 4. Load Data
```bash
pdm run load-data        # Load existing CSV data into Neo4j
pdm run quickstart       # Verify setup
```

### 5. Start Application

**Web Interface** (learning):
```bash
pdm run app              # http://localhost:8501
```

**LangGraph Studio** (debugging):
```bash
pdm run langgraph dev    # Visual workflow debugging
```

## Web Interface

Four learning tabs:

**Concepts** - Knowledge graph and LangGraph fundamentals  
**Try the Agent** - Interactive AI demos with step-by-step processing  
**Explore Queries** - Practice Cypher with examples and visualizations  
**Exercises** - Progressive challenges from basic to advanced  

## Sample Data

Synthetic biomedical dataset:
- **500 genes** (TP53, BRCA1, TP73, etc.)
- **661 proteins** with molecular properties
- **191 diseases** across cardiovascular, neurological, oncological, and other categories
- **350 drugs** (small molecules and biologics)
- **3,039 relationships**

**Key relationships**:
- **Gene→Protein (ENCODES)**: 500 relationships (central dogma)
- **Protein→Disease (ASSOCIATED_WITH)**: 1,347 relationships
- **Drug→Disease (TREATS)**: 618 therapeutic relationships
- **Drug→Protein (TARGETS)**: 574 molecular target relationships

## Development Commands

```bash
pdm run test            # Run all tests (14 tests)
pdm run format          # Format code
pdm run lint            # Check code quality
pdm run quickstart      # System diagnostics
```

---

*Navigate: [← README](../README.md) | [Foundations Guide](foundations-and-background.md) | [Reference](reference.md) | [Technical Guide](technical-guide.md)*