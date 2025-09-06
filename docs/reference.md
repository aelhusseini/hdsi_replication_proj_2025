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
pdm run langgraph           # LangGraph Studio

# Development
pdm run test               # Run tests (14 tests)
pdm run format             # Format code
pdm run lint               # Check quality

# Data Loading
python scripts/load_data.py           # Load complete dataset
```

### Database & Studio
```bash
# Neo4j Desktop (start database first)
Access at http://localhost:7474

# LangGraph Studio
pdm run langgraph    # Opens at smith.langchain.com/studio
```

**Test questions for Studio**:
- "What drugs treat Type2_Diabetes?"
- "What protein does TP53 encode?"
- "Find genes linked to Breast_Cancer"

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
WHERE d.disease_name CONTAINS 'Diabetes'
RETURN g.gene_name, d.disease_name

-- High molecular weight proteins
MATCH (p:Protein)
WHERE p.molecular_weight > 50
RETURN p.protein_name, p.molecular_weight
ORDER BY p.molecular_weight DESC LIMIT 5
```

## Sample Questions

**Beginner**:
- "What drugs treat Hypertension?"
- "What protein does TP53 encode?"
- "What diseases is BRCA1 associated with?"

**Intermediate**:
- "Show pathway from BRCA2 to diseases"
- "Find proteins linked to cardiovascular diseases"
- "What are the targets of Quetiapine?"

**Advanced**:
- "Find complete pathways from TP53 to treatments"
- "Show drugs targeting proteins encoded by BRCA1"
- "Find genes encoding proteins targeted by multiple drugs"


## Links

- Neo4j Browser: http://localhost:7474
- Web Interface: http://localhost:8501
- Anthropic Console: https://console.anthropic.com/
- LangGraph Docs: https://python.langchain.com/docs/langgraph

---

*Navigate: [← README](../README.md) | [Getting Started](getting-started.md) | [Foundations Guide](foundations-and-background.md) | [Technical Guide](technical-guide.md)*