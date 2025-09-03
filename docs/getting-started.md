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
- Neo4j Desktop or Docker
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
LANGSMITH_API_KEY=lsv2_pt_your_key_here  # Optional
```

### 3. Start Database

**Neo4j Desktop** (recommended):
1. Install Neo4j Desktop
2. Create project → Add local DBMS  
3. Set password (same as .env)
4. Start database

**Docker alternative**:
```bash
docker run --name neo4j-learning -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password neo4j:latest
```

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
- **500 genes** (TP53, BRCA1, KRAS, etc.)
- **661 proteins** with molecular properties
- **191 diseases** across 15 medical categories  
- **350 drugs** (small molecules, biologics)
- **3,200+ relationships**

**Key relationships**: Gene→Protein, Protein→Disease, Drug→Disease, Drug→Protein

## Learning Path

**Foundation**: Read concepts → Complete setup → Try web interface → Basic exercises  
**Intermediate**: Work through tutorial notebook → Complete exercises Level 2-3 → Study architecture  
**Advanced**: Master Level 4 exercises → Review technical guide → Build custom applications

## Development Commands

```bash
pdm run test            # Run all tests (27 tests)
pdm run format          # Format code
pdm run lint            # Check code quality
pdm run quickstart      # System diagnostics
```

## Troubleshooting

**Neo4j Connection Failed**:
- Verify Neo4j is running
- Check password in .env matches database  
- Run `pdm run quickstart` for diagnostics

**No Results Found**:
- Ensure data loaded: `pdm run load-data`
- Use real entity names: TP53, BRCA1, Hypertension, Lisinopril
- Start with simpler queries

**API Key Issues**:
- Check ANTHROPIC_API_KEY in .env starts with sk-ant-
- Get free credits at console.anthropic.com

**Import Errors**:
- Run from project root
- Reinstall: `pdm install`  
- Check Python version (needs 3.10+)

## Next Steps

Once running: Explore the web interface → Ask questions → Study generated queries → Master all features

*The best way to learn is by doing - experiment with the interactive tools!*

---

*For help: [Foundations Guide](foundations-and-background.md) | [Reference](reference.md) | [Technical Guide](technical-guide.md)*