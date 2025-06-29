# 📖 Quick Reference

Essential commands, queries, and demo script for the Life Sciences Knowledge Graph Agent platform.

## 🚀 Common Commands

### Setup & Development
```bash
# Project setup
pdm install                 # Install dependencies
pdm run load-data          # Load sample biomedical data
pdm run quickstart         # Verify system setup

# Launch platform
pdm run app                 # Start Streamlit interface (localhost:8501)

# Development
pdm run test               # Run all tests (should see 27 passed)
pdm run format             # Format code with Black + isort
pdm run lint               # Check code quality with Flake8 + MyPy

# Data management
python scripts/simple_load_data.py    # Quick data reload
python scripts/load_data.py           # Full dataset (advanced)
```

### Neo4j Database
```bash
# Docker (if not using Neo4j Desktop)
docker run -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest

# Access Neo4j Browser: http://localhost:7474
# Connection: bolt://localhost:7687
```

## 🧬 Sample Cypher Queries

### Basic Queries
```cypher
-- Find all genes
MATCH (g:Gene) 
RETURN g.gene_name 
LIMIT 5

-- Find all diseases
MATCH (d:Disease) 
RETURN d.disease_name, d.category 
LIMIT 5

-- Find all drugs and their types
MATCH (dr:Drug) 
RETURN dr.drug_name, dr.drug_type 
LIMIT 5
```

### Relationship Queries
```cypher
-- Gene encodes protein
MATCH (g:Gene)-[:ENCODES]->(p:Protein)
RETURN g.gene_name, p.protein_name
LIMIT 5

-- Drugs that treat diseases
MATCH (dr:Drug)-[:TREATS]->(d:Disease)
RETURN dr.drug_name, d.disease_name
LIMIT 5

-- Proteins associated with diseases
MATCH (p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)
RETURN p.protein_name, d.disease_name
LIMIT 5
```

### Complex Pathways
```cypher
-- Gene → Protein → Disease pathway
MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)
RETURN g.gene_name, p.protein_name, d.disease_name
LIMIT 5

-- Complete treatment pathway: Gene → Protein → Disease ← Drug
MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)<-[:TREATS]-(dr:Drug)
RETURN g.gene_name, p.protein_name, d.disease_name, dr.drug_name
LIMIT 3

-- Drug targets and diseases
MATCH (dr:Drug)-[:TARGETS]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)
RETURN dr.drug_name, p.protein_name, d.disease_name
LIMIT 5
```

### Filtered Queries
```cypher
-- Find genes linked to diabetes
MATCH (g:Gene)-[:LINKED_TO]->(d:Disease)
WHERE toLower(d.disease_name) CONTAINS 'diabetes'
RETURN g.gene_name, d.disease_name

-- Find drugs treating hypertension
MATCH (dr:Drug)-[:TREATS]->(d:Disease)
WHERE toLower(d.disease_name) CONTAINS 'hypertension'
RETURN dr.drug_name, d.disease_name

-- Find proteins with high molecular weight
MATCH (p:Protein)
WHERE p.molecular_weight > 50
RETURN p.protein_name, p.molecular_weight
ORDER BY p.molecular_weight DESC
LIMIT 5
```

## 🎓 Sample Questions for the Platform

### Beginner Questions
- "What genes are associated with diabetes?"
- "What drugs treat hypertension?"
- "What protein does GENE_ALPHA encode?"
- "What diseases is PROT_BETA associated with?"

### Intermediate Questions
- "Show me the pathway from GENE_GAMMA to diseases"
- "What are the targets of AlphaCure?"
- "Find proteins linked to metabolic diseases"
- "Which drugs target proteins associated with cancer?"

### Advanced Questions
- "Find complete pathways from genes to treatments for diabetes"
- "Show drugs that target proteins encoded by GENE_ALPHA"
- "What is the shortest path between GENE_BETA and BetaTherapy?"
- "Find genes that encode proteins targeted by multiple drugs"

## 🎯 Demo Script (12-15 minutes)

### Opening (2 minutes)
*"Today I'll demonstrate how **knowledge graphs** and **AI agents** solve complex biomedical questions. This platform shows how graph databases and LangGraph workflows analyze relationships between genes, proteins, diseases, and drugs."*

**Key Points:**
- **Problem**: Biomedical data is interconnected but stored in silos
- **Solution**: Graph databases + AI workflows for intelligent exploration
- **Value**: Fast, accurate answers to complex research questions

### Platform Walkthrough (8 minutes)

#### 1. Overview (1 minute)
Navigate to `http://localhost:8501`

Show: Clean interface, four learning tabs, real-time connectivity

#### 2. Concepts Tab (2 minutes)
**Demonstrate**:
- Knowledge graph fundamentals
- Node types: Genes, Proteins, Diseases, Drugs
- Relationship types: ENCODES, TREATS, TARGETS, etc.
- Interactive schema exploration

#### 3. Try the Agent (3 minutes)
**Live Demo**:
- Ask: *"What drugs treat diabetes?"*
- Show step-by-step workflow:
  - Question classification
  - Entity extraction
  - Cypher generation
  - Query execution
  - Response formatting
- Highlight LangGraph state management

#### 4. Explore Queries (2 minutes)
**Interactive Demonstration**:
- Run pre-built query: Gene → Protein relationships
- Show network visualization
- Try custom query: *"Find drugs targeting PROT_ALPHA"*
- Explain Cypher syntax patterns

### Technical Deep Dive (3 minutes)

#### Architecture Overview
- **Frontend**: Streamlit for interactive learning
- **Backend**: Three agent types (Simple, Learning, Advanced)
- **Database**: Neo4j with biomedical schema
- **AI**: LangGraph + Anthropic Claude for natural language processing

#### Key Technologies
```
Streamlit → User Interface
LangGraph → AI Workflow Engine  
Neo4j → Graph Database
Anthropic Claude → Natural Language Processing
NetworkX → Graph Visualizations
```

### Learning Value (2 minutes)

**Learning Outcomes**:
- **Knowledge Graphs**: Understand relationships and graph thinking
- **LangGraph**: Build AI agents with state management
- **Cypher**: Query graph databases effectively
- **Biomedical AI**: Apply AI to healthcare and research

**Progression**:
- **Week 1-2**: Basic concepts and simple queries
- **Week 3-4**: LangGraph workflows and complex patterns
- **Week 5-6**: Advanced applications and custom development

### Closing & Q&A (2 minutes)

**Summary Points**:
- Platform demonstrates **real-world AI applications**
- **Progressive learning** from basic to advanced concepts
- **Industry-standard tools** and practices
- **Biomedical focus** with practical applications

**Next Steps**:
- Hands-on exercises with sample data
- Jupyter notebook tutorial
- Custom agent development
- Integration with real research workflows

## 🆘 Troubleshooting Quick Fixes

### Connection Issues
```bash
# Check Neo4j status
pdm run quickstart

# Restart Neo4j
# In Neo4j Desktop: Stop → Start database
# In Docker: docker restart neo4j-container
```

### Data Issues
```bash
# Reload sample data
pdm run load-data

# Check data exists
# In Neo4j Browser: MATCH (n) RETURN count(n)
```

### API Issues
```bash
# Verify API key in .env
cat .env | grep ANTHROPIC_API_KEY

# Test API connection
python -c "from anthropic import Anthropic; print('API OK')"
```

### Import Errors
```bash
# Reinstall dependencies
pdm install --no-cache

# Check Python version
python --version  # Should be 3.10+

# Verify working directory
pwd  # Should end with biomedical_kg_project
```

## 🔗 Useful Links

- **Neo4j Browser**: http://localhost:7474
- **Platform Interface**: http://localhost:8501
- **Anthropic Console**: https://console.anthropic.com/
- **Neo4j Desktop**: https://neo4j.com/download/
- **LangGraph Docs**: https://python.langchain.com/docs/langgraph

---

*This reference covers the most common use cases. For detailed implementation, see [technical-guide.md](technical-guide.md).*