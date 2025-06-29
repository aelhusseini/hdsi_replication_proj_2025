# 🔧 Technical Guide

Complete technical documentation for developers working with the Life Sciences Knowledge Graph Agent platform.

**📖 Prerequisites**: This guide assumes familiarity with the concepts covered in [foundations-and-background.md](foundations-and-background.md). If you're new to AI, knowledge graphs, or the biomedical domain, please read that guide first for essential background knowledge.

## 🏗️ System Architecture

### Overview
The platform uses a modular architecture combining Neo4j graph database, LangGraph workflow engine, and Streamlit interface for interactive learning.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Streamlit Web Interface                            │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │ Concepts    │  │ Try Agent    │  │ Queries     │  │ Exercises   │  │
│  └─────────────┘  └──────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                         Agent Layer                                     │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────────┐ │
│ │ WorkflowAgent   │ │AdvancedAIAgent  │ │ TemplateQueryAgent         │ │
│ │ (Production)    │ │ (Learning)      │ │ (Templates)                │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                    Graph Interface Layer                                │
│                   ┌─────────────────────┐                              │
│                   │   GraphInterface    │                              │
│                   │  - Execute Queries  │                              │
│                   │  - Validate Cypher  │                              │
│                   │  - Schema Info      │                              │
│                   └─────────────────────┘                              │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                        Neo4j Database                                   │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │
│   │  Gene   │  │Protein  │  │Disease  │  │  Drug   │                  │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘                  │
│                    Connected by Relationships                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Web Interface (`src/web/app.py`)
- **Streamlit application** with 4 learning tabs
- **Interactive visualizations** using Plotly and NetworkX
- **Real-time query execution** and results display
- **Learning feedback** and step-by-step explanations

#### 2. Agent Types (`src/agents/`)

**AdvancedAIAgent** - Educational LangGraph implementation (learning reference):
```python
class AdvancedAIAgent:
    def __init__(self, graph_interface, anthropic_key):
        self.graph = graph_interface
        self.client = Anthropic(api_key=anthropic_key)
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        # LangGraph state machine with 5 nodes:
        # classify → extract → generate → execute → format
        workflow = StateGraph(AgentState)
        workflow.add_node("classify", self.classify_question)
        workflow.add_node("extract", self.extract_entities)
        workflow.add_node("generate", self.generate_cypher_query)
        workflow.add_node("execute", self.execute_query)
        workflow.add_node("format", self.format_response)
        return workflow.compile()
```

**WorkflowAgent** - Production LangGraph implementation (used in web app):
```python
class WorkflowAgent:
    # Full-featured LangGraph implementation
    # Used in the main Streamlit web application
    # Production-ready with proper error handling
```

**TemplateQueryAgent** - Template-based for beginners:
```python
class TemplateQueryAgent:
    # Pre-built query templates
    # Good for understanding Cypher patterns
    # No AI generation, just parameterized queries
```

#### 3. Graph Interface (`src/agents/graph_interface.py`)
```python
class GraphInterface:
    def execute_query(self, query: str, parameters: dict = None):
        # Executes Cypher queries safely
        # Handles connection management
        # Validates query syntax
    
    def get_schema_info(self):
        # Returns node labels and relationship types
        # Used for query generation and validation
```

## 🧬 Data Model

### Node Types
```cypher
// Genes with properties
(:Gene {gene_name: "GENE_ALPHA", gene_id: "GA001", chromosome: "1"})

// Proteins with molecular details
(:Protein {protein_name: "PROT_ALPHA", protein_id: "PA001", molecular_weight: 45.2})

// Diseases with classifications
(:Disease {disease_name: "diabetes", disease_id: "D001", category: "metabolic"})

// Drugs with mechanisms
(:Drug {drug_name: "AlphaCure", drug_id: "DR001", drug_type: "small_molecule"})
```

### Relationship Types
```cypher
// Central dogma: Gene encodes Protein
(g:Gene)-[:ENCODES]->(p:Protein)

// Genetic associations
(g:Gene)-[:LINKED_TO]->(d:Disease)

// Protein functions
(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)

// Drug mechanisms
(dr:Drug)-[:TREATS]->(d:Disease)
(dr:Drug)-[:TARGETS]->(p:Protein)
```

### Sample Queries
```cypher
// Find pathway: Gene → Protein → Disease
MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)
RETURN g.gene_name, p.protein_name, d.disease_name
LIMIT 5

// Find treatments for diabetes
MATCH (dr:Drug)-[:TREATS]->(d:Disease)
WHERE toLower(d.disease_name) CONTAINS 'diabetes'
RETURN dr.drug_name, d.disease_name

// Complex pathway: Gene → Protein → Disease ← Drug
MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)<-[:TREATS]-(dr:Drug)
RETURN g.gene_name, p.protein_name, d.disease_name, dr.drug_name
LIMIT 3
```

## 🤖 LangGraph Workflow Implementation

### State Definition
```python
from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    question: str
    question_type: str
    entities: List[str]
    cypher_query: Optional[str]
    query_results: List[dict]
    answer: str
    error: Optional[str]
```

### Workflow Nodes

#### 1. Classification Node
```python
def classify_question(state: AgentState) -> AgentState:
    """Classify the type of biomedical question."""
    question = state["question"]
    
    prompt = f"""
    Classify this biomedical question into one of these types:
    - gene_disease: Questions about genes and diseases
    - drug_treatment: Questions about drugs and treatments
    - gene_protein: Questions about genes and proteins
    - pathway: Questions about biological pathways
    
    Question: {question}
    """
    
    response = self.client.messages.create(
        model="claude-3-haiku-20240307",
        messages=[{"role": "user", "content": prompt}]
    )
    
    state["question_type"] = response.content[0].text.strip()
    return state
```

#### 2. Entity Extraction Node
```python
def extract_entities(state: AgentState) -> AgentState:
    """Extract biomedical entities from the question."""
    question = state["question"]
    
    prompt = f"""
    Extract biomedical entities from this question.
    Look for: gene names, protein names, disease names, drug names
    
    Question: {question}
    
    Return as comma-separated list:
    """
    
    # ... implementation
    state["entities"] = entities
    return state
```

#### 3. Query Generation Node
```python
def generate_cypher_query(state: AgentState) -> AgentState:
    """Generate Cypher query based on classification and entities."""
    question_type = state["question_type"]
    entities = state["entities"]
    
    # Template-based generation with validation
    if question_type == "gene_disease":
        query = """
        MATCH (g:Gene)-[:LINKED_TO]->(d:Disease)
        WHERE toLower(g.gene_name) CONTAINS toLower($entity)
           OR toLower(d.disease_name) CONTAINS toLower($entity)
        RETURN g.gene_name, d.disease_name
        LIMIT 10
        """
    # ... other query types
    
    state["cypher_query"] = query
    return state
```

## 📊 Testing Strategy

### Test Coverage
```bash
tests/
├── test_advanced_ai_agent.py      # 7 tests - Full LangGraph workflow
├── test_app.py                    # 7 tests - Web interface & NetworkX
├── test_graph_interface.py        # 4 tests - Database operations
├── test_template_query_agent.py   # 6 tests - Template queries
└── test_workflow_agent.py         # 3 tests - Learning workflow
```

### Key Test Patterns
```python
# Mock external dependencies
@patch('anthropic.Anthropic')
def test_classify_question(self, mock_anthropic):
    # Test AI classification without API calls
    
# Validate database operations
def test_execute_query(self):
    # Test Cypher execution with mock results
    
# Test web visualization
@patch("networkx.spring_layout")
def test_create_network_visualization(self, mock_spring_layout):
    # Test NetworkX graph creation
```

## 🛠️ Development Patterns

### Code Quality
```bash
# Line length: 88 characters (Black standard)
# Formatting: Black + isort
pdm run format

# Linting: Flake8 + MyPy
pdm run lint

# Testing: Pytest with coverage
pdm run test
```

### Security Best Practices
```python
# Always use parameterized queries
def execute_query(self, query: str, parameters: dict = None):
    with self.driver.session() as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]

# Validate all inputs
def validate_query(self, query: str) -> bool:
    # Check for dangerous operations
    dangerous_keywords = ['DELETE', 'DETACH', 'CREATE', 'MERGE']
    return not any(keyword in query.upper() for keyword in dangerous_keywords)
```

### Error Handling
```python
def execute_query(self, query: str, parameters: dict = None):
    try:
        # Execute query
        return results
    except ServiceUnavailable:
        raise ConnectionError("Neo4j database not available")
    except CypherSyntaxError as e:
        raise ValueError(f"Invalid Cypher syntax: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Query execution failed: {str(e)}")
```

## 🚀 Deployment Considerations

### Environment Variables
```bash
# Required for production
ANTHROPIC_API_KEY=sk-ant-your-production-key
NEO4J_URI=bolt://production-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=secure-production-password

# Optional for configuration
APP_ENV=production
LOG_LEVEL=INFO
MAX_QUERY_RESULTS=100
```

### Performance Optimization
```python
# Connection pooling
driver = GraphDatabase.driver(
    uri, 
    auth=(user, password),
    max_connection_lifetime=30 * 60,  # 30 minutes
    max_connection_pool_size=50
)

# Query optimization
CREATE INDEX ON :Gene(gene_name)
CREATE INDEX ON :Disease(disease_name)
CREATE INDEX ON :Drug(drug_name)
CREATE INDEX ON :Protein(protein_name)
```

### Monitoring
```python
# Add timing to queries
import time
def execute_query(self, query: str, parameters: dict = None):
    start_time = time.time()
    try:
        result = session.run(query, parameters or {})
        execution_time = time.time() - start_time
        logger.info(f"Query executed in {execution_time:.2f}s")
        return result
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise
```

## 📚 Extension Points

### Adding New Agent Types
```python
class CustomAgent:
    def __init__(self, graph_interface, custom_config):
        self.graph = graph_interface
        self.config = custom_config
    
    def answer_question(self, question: str):
        # Implement your custom logic
        pass
```

### Custom Visualizations
```python
def create_custom_visualization(results, viz_type):
    if viz_type == "heatmap":
        # Create correlation heatmap
        pass
    elif viz_type == "sankey":
        # Create pathway flow diagram  
        pass
```

### Domain-Specific Extensions
```python
# Finance knowledge graphs
class FinanceAgent(AdvancedAIAgent):
    def get_finance_schema(self):
        return {
            "nodes": ["Company", "Person", "Transaction"],
            "relationships": ["OWNS", "TRANSACTS", "MANAGES"]
        }

# Social network analysis  
class SocialAgent(AdvancedAIAgent):
    def get_social_schema(self):
        return {
            "nodes": ["Person", "Group", "Event"],
            "relationships": ["FRIENDS", "MEMBER_OF", "ATTENDED"]
        }
```

This technical guide provides the foundation for understanding, extending, and deploying the platform in various contexts while maintaining the learning focus that makes knowledge graphs and LangGraph accessible to users.