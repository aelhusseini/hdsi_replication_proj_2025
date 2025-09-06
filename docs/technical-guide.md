# Technical Guide

Complete technical documentation for developers working with Helix Navigator.

**Prerequisites**: This guide assumes familiarity with concepts covered in [foundations-and-background.md](foundations-and-background.md).

## System Architecture

### Overview
The project uses a modular architecture combining Neo4j graph database, LangGraph workflow engine, Streamlit interface for interactive learning, and LangGraph Studio for visual debugging.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      User Interfaces                                   │
│                                                                         │
│ ┌─────────────────────────────────┐ ┌─────────────────────────────────┐ │
│ │     Streamlit Web Interface     │ │     LangGraph Studio            │ │
│ │ ┌─────────┐ ┌─────────┐         │ │ ┌─────────┐ ┌─────────┐         │ │
│ │ │Concepts │ │Try Agent│ ...     │ │ │Visual   │ │Debug    │ ...     │ │
│ │ └─────────┘ └─────────┘         │ │ │Workflow │ │State    │         │ │
│ └─────────────────────────────────┘ └─────────────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                         Agent Layer                                     │
│                     ┌─────────────────┐                               │
│                     │ WorkflowAgent   │                               │
│                     │ (Educational)   │                               │
│                     └─────────────────┘                               │
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

#### 2. LangGraph Studio Integration (`langgraph_studio.py`)
- Visual workflow debugging with real-time graph visualization
- Factory function for Studio compatibility: `create_graph()`
- Configuration via `langgraph.json` for dependencies and graph paths
- **Features**: Interactive visualization, state inspection, step-by-step execution, direct testing, performance monitoring

**Studio Architecture Pattern**:
```python
def create_graph():
    # Environment setup with dotenv
    load_dotenv()
    
    # Create database interface
    graph_interface = GraphInterface(...)
    
    # Create educational workflow agent
    agent = WorkflowAgent(graph_interface, api_key)
    
    # Return compiled LangGraph for Studio
    return agent.workflow
```

#### 3. Agent Types (`src/agents/`)

**WorkflowAgent** - Educational LangGraph implementation (used in web app):
```python
class WorkflowAgent:
    def __init__(self, graph_interface, anthropic_key):
        self.graph_db = graph_interface
        self.anthropic = Anthropic(api_key=anthropic_key)
        self.schema = self.graph_db.get_schema_info()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self):
        # LangGraph state machine with 5 nodes:
        # classify → extract → generate → execute → format
        workflow = StateGraph(WorkflowState)
        workflow.add_node("classify", self.classify_question)
        workflow.add_node("extract", self.extract_entities)
        workflow.add_node("generate", self.generate_query)
        workflow.add_node("execute", self.execute_query)
        workflow.add_node("format", self.format_answer)
        return workflow.compile()
```

#### 4. Graph Interface (`src/agents/graph_interface.py`)
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

## Data Model

### Node Types
```cypher
// Genes with properties
(:Gene {gene_name: "TP53", gene_id: "G001", chromosome: "2"})

// Proteins with molecular details
(:Protein {protein_name: "PROT_ALPHA", protein_id: "P001", molecular_weight: 45.2})

// Diseases with classifications
(:Disease {disease_name: "Hypertension", disease_id: "D001", category: "cardiovascular"})

// Drugs with mechanisms
(:Drug {drug_name: "Lisinopril", drug_id: "DR001", type: "small_molecule"})
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

// Find treatments for hypertension
MATCH (dr:Drug)-[:TREATS]->(d:Disease)
WHERE toLower(d.disease_name) CONTAINS 'hypertension'
RETURN dr.drug_name, d.disease_name

// Complex pathway: Gene → Protein → Disease ← Drug
MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)<-[:TREATS]-(dr:Drug)
RETURN g.gene_name, p.protein_name, d.disease_name, dr.drug_name
LIMIT 3
```

## LangGraph Workflow Implementation

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
        model="claude-3-5-sonnet-20241022",
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
    
    # Implementation extracts relevant entities
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
    # Additional query types handled similarly
    
    state["cypher_query"] = query
    return state
```

## Testing Strategy

### Test Coverage
```bash
tests/
├── test_app.py                    # 7 tests - Web interface & NetworkX
├── test_graph_interface.py        # 4 tests - Database operations  
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

## Development Patterns

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

## Deployment Considerations

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