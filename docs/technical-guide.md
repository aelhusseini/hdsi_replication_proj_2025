# Technical Guide

Complete technical documentation for developers working with Helix Navigator.

**Prerequisites**: This guide assumes familiarity with concepts covered in [Foundations Guide](foundations-and-background.md).

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

#### 2. LangGraph Studio Integration (`langgraph-studio/langgraph_studio.py`)
- Visual workflow debugging with real-time graph visualization
- Factory function for Studio compatibility: `create_graph()`
- Configuration via `langgraph-studio/langgraph.json` for dependencies and graph paths
- **Features**: Interactive visualization, state inspection, step-by-step execution, direct testing, performance monitoring

**Studio Architecture Pattern**:
```python
def create_graph():
    """Create and return the workflow graph for LangGraph Studio."""
    # Load environment variables
    load_dotenv()
    
    # Get environment variables
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Create graph interface
    graph_interface = GraphInterface(
        uri=neo4j_uri, user=neo4j_user, password=neo4j_password
    )
    
    # Create workflow agent
    agent = WorkflowAgent(
        graph_interface=graph_interface, anthropic_api_key=anthropic_api_key
    )
    
    # Return compiled LangGraph for Studio
    return agent.workflow

# Create the graph instance for Studio
graph = create_graph()
```

#### 3. Agent Types (`src/agents/`)

**WorkflowAgent** - Educational LangGraph implementation (used in web app):
```python
class WorkflowAgent:
    """LangGraph workflow agent for biomedical knowledge graphs."""
    
    # Class constants
    MODEL_NAME = "claude-sonnet-4-20250514"
    DEFAULT_MAX_TOKENS = 200
    
    def __init__(self, graph_interface: GraphInterface, anthropic_api_key: str):
        self.graph_db = graph_interface
        self.anthropic = Anthropic(api_key=anthropic_api_key)
        self.schema = self.graph_db.get_schema_info()
        self.property_values = self._get_key_property_values()
        self.workflow = self._create_workflow()
    
    def _get_key_property_values(self) -> Dict[str, List[str]]:
        """Get property values dynamically from all nodes and relationships.
        
        This method discovers all available properties in the database schema and
        collects sample values for each property. This enables the LLM to generate
        more accurate queries by knowing what property values actually exist.
        
        Returns:
            Dict mapping property names to lists of sample values from the database
        """
    
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
    """Thread-safe Neo4j database wrapper with security and error handling."""
    
    def execute_query(self, cypher_query: str, parameters: Optional[Dict[str, Any]] = None):
        """Execute parameterized Cypher query and return results as dictionaries."""
        # Executes Cypher queries safely with parameterization
        # Handles connection management and error logging
        # Returns structured results as list of dictionaries
    
    def get_schema_info(self) -> Dict[str, Any]:
        """Get database schema: node labels, relationship types, and properties."""
        # Returns comprehensive schema information
        # Includes node labels, relationship types, and property mappings
        # Used for dynamic query generation and validation
    
    def get_property_values(self, node_label: str, property_name: str, limit: int = 20):
        """Get sample property values for a given node type and property."""
        # Discovers actual property values in the database
        # Supports both node and relationship property discovery
        # Enables context-aware query generation
```

## Data Model

### Node Types
```cypher
// Genes with properties
(:Gene {gene_name: "TP53", gene_id: "G001", chromosome: "2", function: "metabolism", expression_level: "medium"})

// Proteins with molecular details
(:Protein {protein_name: "PROT_001", protein_id: "P001", molecular_weight: 45.2, function: "enzyme", localization: "cytoplasm"})

// Diseases with classifications  
(:Disease {disease_name: "Hypertension", disease_id: "D001", category: "cardiovascular", prevalence: "uncommon", severity: "life_threatening"})

// Drugs with mechanisms
(:Drug {drug_name: "AlphaCure", drug_id: "DR001", type: "small_molecule", mechanism: "inhibitor", approval_status: "approved"})
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
from typing import TypedDict, List, Optional, Dict, Any

class WorkflowState(TypedDict):
    """State that flows through the workflow steps."""
    user_question: str
    question_type: Optional[str]
    entities: Optional[List[str]]
    cypher_query: Optional[str]
    results: Optional[List[Dict]]
    final_answer: Optional[str]
    error: Optional[str]
```

### Workflow Nodes

#### 1. Classification Node
```python
def classify_question(state: WorkflowState) -> WorkflowState:
    """Classify the type of biomedical question."""
    question = state["user_question"]
    
    prompt = f"""
    Classify this biomedical question into one of these types:
    - gene_disease: Questions about genes and diseases
    - drug_treatment: Questions about drugs and treatments
    - gene_protein: Questions about genes and proteins
    - pathway: Questions about biological pathways
    
    Question: {question}
    """
    
    response = self.anthropic.messages.create(
        model="claude-sonnet-4-20250514",
        messages=[{"role": "user", "content": prompt}]
    )
    
    state["question_type"] = response.content[0].text.strip()
    return state
```

#### 2. Entity Extraction Node
```python
def extract_entities(state: WorkflowState) -> WorkflowState:
    """Extract biomedical entities from the question."""
    question = state["user_question"]
    
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
def generate_cypher_query(state: WorkflowState) -> WorkflowState:
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
@patch('src.agents.workflow_agent.Anthropic')
def test_classify_question(self, mock_anthropic):
    """Test question classification."""
    state = WorkflowState(
        user_question="What genes are associated with diabetes?",
        question_type=None,
        # ... other fields
    )
    
# Validate database operations
def test_execute_query(self):
    """Test Cypher execution with mock results."""
    # Test parameterized queries with mock graph interface
    
# Test web visualization
@patch("networkx.spring_layout")
def test_create_network_visualization(self, mock_spring_layout):
    """Test NetworkX graph creation and Plotly visualization."""
    # Test graph layout and interactive visualization
```

## Development Patterns

### Code Quality Standards
```bash
# Project uses PDM for dependency management
pdm install                    # Install dependencies

# Code formatting (88 character line length)
pdm run format                # Black + isort formatting

# Code quality checks
pdm run lint                  # Flake8 + MyPy static analysis

# Testing with comprehensive coverage
pdm run test                  # Pytest with 14 total tests

# Application commands
pdm run app                   # Launch Streamlit interface
pdm run langgraph            # Launch LangGraph Studio
pdm run load-data            # Load biomedical data into Neo4j
pdm run quickstart           # Verify system setup
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

### Environment Configuration
```bash
# Required environment variables (create .env file)
ANTHROPIC_API_KEY=sk-ant-your-production-key
NEO4J_URI=bolt://localhost:7687              # Local development
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-neo4j-password

# Optional configuration
APP_ENV=development
LOG_LEVEL=INFO
MAX_QUERY_RESULTS=100
QUERY_TIMEOUT=30

# LangGraph Studio integration
LANGSMITH_API_KEY=lsv2_pt_your-key-here     # For Studio debugging
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

### Educational Architecture

The technical architecture is designed specifically for learning:

```python
# Dynamic Schema Discovery
class WorkflowAgent:
    def _get_key_property_values(self) -> Dict[str, List[str]]:
        """Dynamically discover database properties for accurate query generation."""
        # Replaces hardcoded schema with runtime discovery
        # Enables more intelligent query generation
        # Supports both node and relationship properties
    
    def _get_llm_response(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Centralized LLM interaction using Claude Sonnet 4."""
        # Uses claude-sonnet-4-20250514 model
        # Configurable token limits for different query types
        # Consistent error handling across all LLM calls
```

### Monitoring and Debugging
```python
# Built-in logging for development
import logging
logger = logging.getLogger(__name__)

def execute_query(self, cypher_query: str, parameters: Optional[Dict[str, Any]] = None):
    """Execute queries with comprehensive error handling."""
    try:
        # Execute with session management
        with self.driver.session() as session:
            result = session.run(cast(Query, cypher_query), parameters or {})
            return [record.data() for record in result]
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise
```

---

*Navigate: [← README](../README.md) | [Getting Started](getting-started.md) | [Foundations Guide](foundations-and-background.md) | [Reference](reference.md)*