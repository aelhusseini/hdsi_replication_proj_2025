# System Architecture

## 🎓 Overview

The Life Sciences Knowledge Graph Agent is designed as a learning platform for undergraduate students to learn **LangGraph workflows** and **knowledge graph concepts** through hands-on biomedical AI applications.

## 🏗️ Architecture Components

### 1. **Learning-Focused Components**
- **Educational Agent**: Simplified LangGraph implementation with clear learning comments
- **Interactive Tutorial**: Jupyter notebook with step-by-step progression
- **Progressive Exercises**: Four difficulty levels from beginner to expert
- **Multiple Agent Types**: Template-based, educational, and full-featured variants

### 2. **Traditional Components** 
- **Neo4j Knowledge Graph**: Biomedical entities and relationships
- **Streamlit Web Interface**: Interactive learning environment
- **Python Backend**: Orchestrates educational workflows

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Interactive Streamlit Interface                    │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │📚 Concepts  │  │🧪 Try Agent  │  │🔍 Queries  │  │🏋️ Exercises │  │
│  │ Learning    │  │ Interactive  │  │ Practice    │  │ Progressive │  │
│  │ Materials   │  │ Workflow     │  │ Cypher      │  │ Challenges  │  │
│  └─────────────┘  └──────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────┐
│                    Three Educational Approaches                         │
│                                                                         │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────────┐ │
│ │ Simple Agent    │ │Educational Agent│ │ LangGraph Agent            │ │
│ │ (Templates)     │ │ (Learning)      │ │ (Full-Featured)            │ │
│ │                 │ │                 │ │                            │ │
│ │ • Fast          │ │ • Simplified    │ │ • Complete                 │ │
│ │ • Predictable   │ │ • Well-commented│ │ • Error handling           │ │
│ │ • Reliable      │ │ • Educational   │ │ • Advanced features        │ │
│ │                 │ │                 │ │                            │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Biomedical Knowledge Graph                           │
│                                                                         │
│  ┌────────┐     ┌─────────┐     ┌─────────┐     ┌────────┐             │
│  │ Genes  │────►│ Proteins│────►│ Diseases│◄────│ Drugs  │             │
│  │ (🧬)   │     │ (🧪)    │     │ (🏥)    │     │ (💊)   │             │
│  └────────┘     └─────────┘     └─────────┘     └────────┘             │
│                                                                         │
│  Educational Features:                                                  │
│  • Clear entity relationships for learning                            │
│  • Sample data that demonstrates key concepts                         │
│  • Schema designed for educational exploration                        │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Educational Data Flow

### 1. Learning-Focused Query Processing

```
Student Question → 🎓 Educational Agent Workflow → Learning-Rich Response

Detailed Flow:
User Input → [📊 Classify] → [🧬 Extract] → [🔧 Generate] → [▶️ Execute] → [💬 Format] → Output
              ↓             ↓             ↓              ↓             ↓
           Print logs    Print entities  Print query   Print results  Print completion
```

### 2. Educational LangGraph State Management

```python
class LearningState(TypedDict):
    """Educational state with clear field explanations"""
    user_question: str              # Original question from student
    question_type: Optional[str]     # What kind of biomedical question?
    entities: Optional[List[str]]    # Important terms we found
    cypher_query: Optional[str]      # The database query we generated
    results: Optional[List[Dict]]    # What we found in the database
    final_answer: Optional[str]      # Human-readable response
    error: Optional[str]             # If something went wrong
```

### 3. Progressive Learning Workflow

**Beginner Level (Weeks 1-2):**
1. **Understand Graphs**: Nodes, relationships, basic concepts
2. **Practice Queries**: Simple Cypher patterns
3. **Explore Data**: Use template-based SimpleAgent

**Intermediate Level (Weeks 3-4):**
1. **Learn LangGraph**: State management and workflows
2. **Build Workflows**: Modify educational agent
3. **Complex Queries**: Multi-hop relationship traversal

**Advanced Level (Weeks 5-6):**
1. **Custom Agents**: Design specialized workflows
2. **Real Applications**: Drug discovery, personalized medicine
3. **Performance**: Optimization and scaling

## 🗄️ Educational Database Schema

### Node Types (Educational Focus)
- **Gene (🧬)**: Genetic sequences that students can explore
  - Clear naming: `GENE_ALPHA`, `GENE_BETA` for easy recognition
  - Properties: chromosome location, biological function
  
- **Protein (🧪)**: Products of gene expression
  - Connected to genes via ENCODES relationship
  - Properties: molecular weight, structure type
  
- **Disease (🏥)**: Medical conditions for practical relevance
  - Categories: neurological, metabolic, etc. for classification practice
  - Properties: prevalence, severity for realistic data
  
- **Drug (💊)**: Treatments that complete the biological story
  - Types: small_molecule, biologic for understanding drug classes
  - Properties: approval_status, mechanism for real-world context

### Educational Relationship Patterns

```cypher
-- Basic relationship (Beginner)
(Gene)-[:ENCODES]->(Protein)

-- Two-hop path (Intermediate) 
(Gene)-[:ENCODES]->(Protein)-[:ASSOCIATED_WITH]->(Disease)

-- Complex pathway (Advanced)
(Gene)-[:ENCODES]->(Protein)-[:ASSOCIATED_WITH]->(Disease)<-[:TREATS]-(Drug)

-- Derived knowledge (Expert)
(Gene)-[:LINKED_TO]->(Disease)  // Computed from gene→protein→disease
```

## 🛠️ Educational Technology Stack

### Learning-Focused Tools
- **Jupyter Notebooks**: Interactive, step-by-step tutorials
- **Streamlit Educational Mode**: Tabbed interface for different learning activities
- **Progressive Exercises**: Structured from basic to advanced
- **Multiple Agent Examples**: Show different approaches and trade-offs

### Core Technologies
- **Python 3.10+**: Accessible language for students
- **Neo4j**: Industry-standard graph database
- **LangGraph**: Modern AI workflow framework
- **Anthropic Claude**: Powerful and educational AI models

### Educational Enhancements
- **Clear Commenting**: Every function explains educational purpose
- **Print Statements**: Show workflow progress for learning
- **Error Handling**: Graceful failures with learning opportunities
- **Modular Design**: Students can understand and modify components

## 🎯 Learning Objectives Architecture

### Knowledge Graph Mastery
1. **Conceptual Understanding**: Graph vs. relational thinking
2. **Query Skills**: Cypher from basic to advanced patterns
3. **Schema Design**: How to model domain knowledge as graphs
4. **Performance**: Understanding indexes, constraints, optimization

### LangGraph Workflow Skills
1. **State Management**: How information flows between steps
2. **Node Design**: Creating processing functions with clear purposes
3. **Workflow Assembly**: Connecting nodes into coherent processes
4. **Error Handling**: Graceful failure and recovery patterns

### Biomedical Application Knowledge
1. **Domain Understanding**: Gene→Protein→Disease→Drug relationships
2. **Query Patterns**: Common biomedical questions as graph traversals
3. **Real Applications**: Drug discovery, personalized medicine use cases
4. **Ethical Considerations**: Responsible AI in healthcare contexts

## 🔧 Educational Customization Points

### 1. Adding New Learning Modules
```python
# Easy to extend with new educational components
def new_learning_concept(state: LearningState) -> LearningState:
    """Educational function with clear learning objective"""
    # Teaching point: What this step demonstrates
    # Implementation with learning comments
    return state
```

### 2. Progressive Difficulty Levels
- **Beginner**: Pre-built queries and templates
- **Intermediate**: Guided workflow modification
- **Advanced**: Custom agent development
- **Expert**: Real-world application building

### 3. Assessment Integration
- **Self-Check Exercises**: Built into Streamlit interface
- **Progress Tracking**: Completion of difficulty levels
- **Portfolio Projects**: Culminating applications

### 4. Multiple Learning Modalities
- **Visual Learners**: Graph visualizations and diagrams
- **Hands-on Learners**: Interactive coding exercises
- **Reading Learners**: Comprehensive documentation
- **Project Learners**: Real-world application building

## 📈 Performance for Education

### Optimized for Learning
1. **Simplified Code**: Readability over micro-optimizations
2. **Educational Logging**: Progress visibility for students
3. **Sample Data Size**: Large enough to be interesting, small enough to understand
4. **Response Time**: Balance between realism and classroom usability

### Scalability Considerations
1. **Multiple Students**: Streamlit can handle classroom-sized groups
2. **Concurrent Learning**: Neo4j supports multiple simultaneous learners
3. **Resource Management**: Reasonable API usage for educational budgets

## 🛡️ Educational Security

### Student-Safe Environment
1. **Limited Scope**: Controlled dataset prevents inappropriate queries
2. **Safe APIs**: Educational rate limits on external services
3. **No Real Data**: Synthetic biomedical data for ethical learning
4. **Clear Boundaries**: Students understand this is educational, not clinical

### Learning-Focused Access
1. **Open Source**: Students can examine all code
2. **Local Development**: No external system dependencies required
3. **Version Control**: Students learn Git workflows safely

## 🚀 Deployment for Education

### Classroom Setup
- **Individual Laptops**: Each student runs locally
- **Shared Database**: Optional classroom Neo4j instance
- **Cloud Options**: Neo4j Aura free tier for accessibility

### Instructor Support
- **Teaching Materials**: Comprehensive guides and lesson plans
- **Assessment Tools**: Built-in exercises and project rubrics
- **Technical Support**: Clear setup and troubleshooting guides

This educational architecture provides a comprehensive learning platform that teaches both technical skills and domain knowledge through practical, engaging applications.