# Quick Reference

Essential commands, queries, and troubleshooting for Helix Navigator.

## Common Commands

### Setup & Development
```bash
# Setup
pdm install                 # Install dependencies
pdm run load-data          # Load data into Neo4j
pdm run quickstart         # Verify setup

# Launch
pdm run app                 # Streamlit interface
pdm run langgraph dev       # LangGraph Studio

# Development
pdm run test               # Run tests (27 tests)
pdm run format             # Format code
pdm run lint               # Check quality

# Data Loading
python scripts/load_data.py           # Load complete dataset
```

### Database & Studio
```bash
# Neo4j Docker
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest

# LangGraph Studio
pdm run langgraph dev    # Opens at smith.langchain.com/studio
```

**Test questions for Studio**:
- "What drugs treat diabetes?"
- "What protein does TP53 encode?"
- "Find genes linked to cancer"

## Sample Cypher Queries

### Basic Queries
```cypher
-- Find genes
MATCH (g:Gene) RETURN g.gene_name LIMIT 5

-- Find diseases by category
MATCH (d:Disease) RETURN d.disease_name, d.category LIMIT 5

-- Find drugs by type
MATCH (dr:Drug) RETURN dr.drug_name, dr.type LIMIT 5
```

### Relationships
```cypher
-- Gene encodes protein
MATCH (g:Gene)-[:ENCODES]->(p:Protein)
RETURN g.gene_name, p.protein_name LIMIT 5

-- Drugs treat diseases
MATCH (dr:Drug)-[:TREATS]->(d:Disease)
RETURN dr.drug_name, d.disease_name LIMIT 5

-- Proteins linked to diseases
MATCH (p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)
RETURN p.protein_name, d.disease_name LIMIT 5
```

### Complex Pathways
```cypher
-- Gene → Protein → Disease
MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)
RETURN g.gene_name, p.protein_name, d.disease_name LIMIT 5

-- Complete pathway: Gene → Protein → Disease ← Drug
MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)<-[:TREATS]-(dr:Drug)
RETURN g.gene_name, dr.drug_name, d.disease_name LIMIT 3
```

### Filtering
```cypher
-- Genes linked to diabetes
MATCH (g:Gene)-[:LINKED_TO]->(d:Disease)
WHERE toLower(d.disease_name) CONTAINS 'diabetes'
RETURN g.gene_name, d.disease_name

-- High molecular weight proteins
MATCH (p:Protein)
WHERE p.molecular_weight > 50
RETURN p.protein_name, p.molecular_weight
ORDER BY p.molecular_weight DESC LIMIT 5
```

## Sample Questions

**Beginner**:
- "What drugs treat hypertension?"
- "What protein does TP53 encode?"
- "What diseases is BRCA1 associated with?"

**Intermediate**:
- "Show pathway from BRCA2 to diseases"
- "Find proteins linked to cardiovascular diseases"
- "What are the targets of Lisinopril?"

**Advanced**:
- "Find complete pathways from TP53 to treatments"
- "Show drugs targeting proteins encoded by BRCA1"
- "Find genes encoding proteins targeted by multiple drugs"

## Demo Script (15 minutes)

### Opening (2 min)
"Demonstrating knowledge graphs + AI agents for biomedical questions. Problem: scattered data. Solution: graph databases + AI workflows."

### Application Demo (8 min)

**Overview** (1 min): Show http://localhost:8501 interface

**Concepts Tab** (2 min): Knowledge graph fundamentals, node/relationship types

**Try the Agent** (3 min): 
- Ask: "What drugs treat Hypertension?"
- Show 5-step workflow: classify → extract → generate → execute → format
- Highlight LangGraph state management

**Explore Queries** (2 min): Run Cypher queries, show visualizations

### Architecture (3 min)
```
Streamlit → LangGraph → Neo4j → Anthropic Claude
```

Three agent types: Educational, Production patterns, Template-based

### Learning Value (2 min)
- Knowledge graphs + LangGraph + Cypher + Biomedical AI
- Progressive: Foundation → Intermediate → Advanced

**Next steps**: Tutorial notebook, exercises, custom development

## Troubleshooting

**Connection Issues**:
```bash
pdm run quickstart    # Check status
# Restart Neo4j in Desktop or Docker
```

**Data Issues**:
```bash
pdm run load-data     # Reload data
# Check in Neo4j Browser: MATCH (n) RETURN count(n)
```

**API Issues**:
```bash
cat .env | grep ANTHROPIC_API_KEY    # Verify key
```

**Import Errors**:
```bash
pdm install --no-cache              # Reinstall
python --version                    # Check 3.10+
```

## Links

- Neo4j Browser: http://localhost:7474
- Web Interface: http://localhost:8501
- Anthropic Console: https://console.anthropic.com/
- LangGraph Docs: https://python.langchain.com/docs/langgraph

---

*For detailed implementation, see [technical-guide.md](technical-guide.md)*