# 🎓 User Guide

## 📚 Getting Started with Learning

Welcome to the Life Sciences Knowledge Graph Agent learning platform! This guide will help you learn LangGraph and knowledge graphs through hands-on biomedical AI applications.

## 🎯 Learning Interface Overview

### Main Interface Components

1. **📚 Concepts Tab**:
   - Learn knowledge graph fundamentals
   - Understand LangGraph workflows
   - Practice Cypher query patterns
   - Explore biomedical applications

2. **🧪 Try the Agent Tab**:
   - Interactive workflow demonstration
   - Step-by-step process visualization
   - See how LangGraph state flows between nodes
   - Educational logging and explanations

3. **🔍 Explore Queries Tab**:
   - Practice writing Cypher queries
   - Pre-built examples for learning
   - Safe query execution environment
   - Immediate feedback and visualization

4. **🏋️ Exercises Tab**:
   - Progressive difficulty levels
   - Hands-on coding challenges
   - Self-assessment opportunities
   - Guided learning pathways

### Advanced Features

1. **Natural Language Processing**: Interactive agent responses
2. **Database Query Interface**: Direct Cypher query execution
3. **Visualization Tools**: Network graphs and charts

## 🧠 Educational Learning Paths

### 🎓 Beginner Level (Weeks 1-2)

**Learning Goals:**
- Understand what knowledge graphs are
- Learn basic graph terminology (nodes, edges, relationships)
- Practice simple Cypher queries
- Explore our biomedical dataset

**Recommended Activities:**
1. Start with **📚 Concepts Tab** → "Knowledge Graphs"
2. Try **🔍 Explore Queries Tab** → Simple examples
3. Complete **🏋️ Exercises Tab** → "Exercise 1: Basic Queries"

### 🎓 Intermediate Level (Weeks 3-4)

**Learning Goals:**
- Understand LangGraph workflow concepts
- Learn state management in AI agents
- Practice multi-hop relationship queries
- Build custom workflow components

**Recommended Activities:**
1. Study **📚 Concepts Tab** → "LangGraph Workflows"
2. Use **🧪 Try the Agent Tab** → Watch step-by-step processing
3. Complete **🏋️ Exercises Tab** → "Exercise 2: Relationship Patterns"

### 🎓 Advanced Level (Weeks 5-6)

**Learning Goals:**
- Design complex biomedical queries
- Understand real-world applications
- Modify and extend agent workflows
- Build portfolio projects

**Recommended Activities:**
1. Master **🔍 Explore Queries Tab** → Complex pathways
2. Complete **🏋️ Exercises Tab** → "Exercise 3: Complex Pathways"
3. Explore the educational agent code in `agent/educational_agent.py`

## 🔍 Supported Question Types

### Educational Examples by Difficulty

#### 1. 🟢 Beginner: Basic Entity Queries
```
Examples:
- "What genes are associated with diabetes?" (single relationship)
- "What drugs treat hypertension?" (direct connection)
- "What protein does GENE_ALPHA encode?" (simple lookup)
```

#### 2. 🟡 Intermediate: Two-Hop Relationships  
```
Examples:
- "What diseases is PROT_ALPHA associated with?" (protein → disease)
- "Which proteins does BetaTherapy target?" (drug → protein)
- "Show diseases linked to GENE_GAMMA" (gene → protein → disease)
```

#### 3. 🟠 Advanced: Multi-Step Pathways
```
Examples:
- "Show me the complete pathway from genes to drugs for diabetes"
- "What's the molecular pathway for treating hypertension?"
- "How do genes connect to drug treatments for cancer?"
```

#### 4. 🔴 Expert: Analytical Queries
```
Examples:
- "Which drugs have the highest efficacy for neurological diseases?"
- "Find genes linked to multiple diseases through protein associations"
- "Compare treatment options across different disease categories"
```

## 💡 Learning Tips for Students

### 🎯 Query Construction Tips

1. **Start Simple**: Begin with single-entity queries
   - ✅ Good: "What does GENE_ALPHA encode?"
   - ❌ Avoid: Complex multi-part questions initially

2. **Use Our Sample Data**: Stick to entities we know exist
   - ✅ Good: "hypertension", "diabetes", "GENE_ALPHA", "PROT_BETA"
   - ❌ Avoid: Real gene names not in our educational dataset

3. **Progress Gradually**: Build complexity step by step
   - 🟢 Start: "What drugs treat diabetes?"
   - 🟡 Then: "What proteins do those drugs target?"
   - 🟠 Finally: "Show complete pathway from genes to treatments"

### 🧠 Learning Strategy

1. **Visual Learning**: Use the network visualizations to understand relationships
2. **Practice Mode**: Try queries in the **🔍 Explore Queries Tab** first
3. **Error Learning**: Don't worry about mistakes - they're part of learning!
4. **Code Reading**: Examine the generated Cypher queries to learn patterns

## 🎯 Structured Learning Exercises

### 📊 Query Practice Templates

When you're ready for more advanced practice, try these structured query patterns:

1. **🧬 Genes for Disease** (Beginner-friendly)
   - Input: Disease name → Output: Associated genes
   - Learning focus: Simple entity relationships

2. **💊 Drugs for Disease** (Beginner-friendly)  
   - Input: Disease name → Output: Treatment options
   - Learning focus: Direct therapeutic relationships

3. **🧪 Protein from Gene** (Intermediate)
   - Input: Gene name → Output: Encoded protein
   - Learning focus: Central dogma of biology

4. **🏥 Diseases for Protein** (Intermediate)
   - Input: Protein name → Output: Associated diseases  
   - Learning focus: Protein function and pathology

5. **🎯 Drug Targets** (Advanced)
   - Input: Drug name → Output: Molecular targets
   - Learning focus: Mechanism of action

6. **🛤️ Disease Pathway Analysis** (Expert)
   - Input: Disease name → Output: Complete pathways
   - Learning focus: Systems-level understanding

## 📊 Understanding Your Results

### 🎓 Educational Result Components

1. **💬 Answer Text**: Human-readable explanation (this is what the LangGraph workflow produces!)
2. **📋 Data Table**: Structured database results (raw Neo4j output)
3. **📈 Learning Metrics**: 
   - **Entities Found**: How many biomedical terms the agent recognized
   - **Results Count**: Number of matches found in the knowledge graph
   - **Question Type**: What category of biomedical question this was
4. **💻 Cypher Query**: The actual database query generated (click to expand and learn!)

### 🔗 Relationship Types in Our Educational Graph

- **🧬 ENCODES**: Gene directly creates protein (central dogma)
- **🔗 LINKED_TO**: Gene indirectly connected to disease (computed relationship)
- **🧪 ASSOCIATED_WITH**: Protein experimentally linked to disease
- **💊 TREATS**: Drug approved or tested for disease
- **🎯 TARGETS**: Drug binds to or affects specific protein

### 📊 Educational Confidence Levels

Our synthetic data includes confidence scores for learning:
- **High (0.8-1.0)**: Strong educational example
- **Medium (0.5-0.7)**: Moderate confidence scenario  
- **Low (0.1-0.4)**: Preliminary evidence example

*Note: These are educational examples, not real clinical data!*

## 🎓 Educational Learning Workflows

### 🟢 Beginner Workflow: Exploring a Disease

**Learning Goal**: Understand basic graph traversal
1. **Start simple**: "What genes are associated with diabetes?"
2. **Follow connection**: Pick a gene → "What protein does GENE_ALPHA encode?"
3. **Expand knowledge**: "What other diseases is PROT_ALPHA associated with?"
4. **Find treatments**: "What drugs target PROT_ALPHA?"

**Key Learning**: See how entities connect in a knowledge graph!

### 🟡 Intermediate Workflow: Drug Discovery Investigation

**Learning Goal**: Understand multi-step reasoning
1. **Start with treatment**: "What are the targets of AlphaCure?"
2. **Explore biology**: "What diseases is PROT_ALPHA associated with?"
3. **Connect pathways**: "Show pathway from genes to AlphaCure for diabetes"

**Key Learning**: See how LangGraph workflows handle complex questions!

### 🟠 Advanced Workflow: Comparative Analysis

**Learning Goal**: Practice analytical thinking
1. **Query disease 1**: "What drugs treat hypertension?"
2. **Query disease 2**: "What drugs treat heart disease?"
3. **Compare results**: Find overlapping treatments and understand why

**Key Learning**: Use knowledge graphs for research questions!

## 🚀 Advanced Learning Features

### 🔍 Database Schema Explorer

- **Educational Purpose**: Understand graph structure
- **How to use**: Enable "Show Database Schema" in sidebar
- **What you'll see**: Node types (Gene, Protein, Disease, Drug) and relationships
- **Learning tip**: Use this to understand what questions you can ask!

### 📚 Query History & Pattern Learning

- **Educational Purpose**: Learn from your queries
- **Natural Language mode**: Scroll up to see previous questions
- **Pattern recognition**: Each query shows its Cypher translation
- **Learning strategy**: Compare similar questions to understand query patterns

### 🌐 Interactive Network Visualizations

- **Educational Purpose**: Visual understanding of relationships
- **Features**: 
  - Drag nodes to rearrange and explore
  - Hover for entity details
  - Zoom in/out for different perspectives
- **Learning tip**: Use visualizations to understand complex pathways!

## 🛠️ Troubleshooting for Students

### ❓ "No Results Found"

**Educational Learning Opportunity**: Understanding why queries fail!

**Common Causes & Solutions**:
- **Spelling**: Our entities are case-insensitive, but check spelling
- **Entity names**: Use our sample data - try "GENE_ALPHA", "diabetes", "AlphaCure"
- **Partial matching**: Try "diabet" instead of "diabetes" to catch variations
- **Database check**: Use schema explorer to see what entities exist

### ⏱️ "Slow Responses"

**Educational Learning Point**: Understanding system performance!

**Why it happens**:
- Complex queries take longer (this is normal!)
- Natural language processing adds overhead
- LangGraph workflows have multiple steps

**Learning strategy**: 
- Start with simple queries in **🔍 Explore Queries Tab**
- Graduate to complex questions in **🧪 Try the Agent Tab**

### 🤔 "Unexpected Results"

**Educational Learning Opportunity**: Debugging AI systems!

**Learning approach**:
1. **Review the generated Cypher query** (expand to see it)
2. **Check question interpretation** - did the agent understand correctly?
3. **Try rephrasing** - different words might work better
4. **Use simpler questions first** - build up complexity gradually

## 🎯 Best Learning Practices

### 🎓 Progressive Learning Strategy

1. **🟢 Start Broad, Then Narrow** (Beginner approach)
   - Begin with simple entity queries: "What is diabetes?"
   - Follow interesting connections: "What genes are linked to diabetes?"
   - Deep dive into specific pathways: "Show gene to drug pathway for diabetes"

2. **🔍 Cross-Reference for Learning** (Intermediate skill)
   - Ask the same question different ways
   - Compare results between query modes
   - Look for consistent patterns in the data

3. **🚀 Use All Learning Modes** (Advanced practice)
   - **📚 Concepts Tab**: Theory and fundamentals
   - **🧪 Try Agent Tab**: Interactive workflow learning
   - **🔍 Explore Queries Tab**: Hands-on Cypher practice
   - **🏋️ Exercises Tab**: Structured challenges

## 📚 Educational Limitations & Learning Points

**Important for Students to Understand**:
- **Synthetic data**: Educational examples, not real clinical data
- **Simplified relationships**: Focused on core concepts for learning
- **Limited scope**: Designed for specific learning objectives
- **No clinical validation**: This is for learning, not medical advice!

**Learning Value**: Understanding limitations is part of being a responsible AI practitioner!

## 🆘 Getting Help & Learning Resources

### 🎓 For Students:
- **UI Help**: Hover over interface elements for tooltips
- **Learning Examples**: Check sidebar for sample questions
- **Code Learning**: Review generated Cypher queries (expand to see them)
- **Deep Dive**: Read `LEARNING_GUIDE.md` for detailed curriculum
- **Tutorial**: Work through `tutorial_langgraph_knowledge_graphs.ipynb`

### 👨‍🏫 For Instructors:
- **Architecture Guide**: See `docs/ARCHITECTURE.md` for system design
- **Setup Help**: Check `docs/SETUP_GUIDE.md` for classroom deployment
- **Assessment**: Use built-in exercises for student evaluation

## 🎉 Ready to Learn!

Start your learning journey:
1. **Absolute beginners**: Open the tutorial notebook first
2. **Some experience**: Jump into Educational Mode's **📚 Concepts Tab**
3. **Ready to code**: Try the **🔍 Explore Queries Tab**
4. **Want challenges**: Head to the **🏋️ Exercises Tab**

Happy learning! 🚀🧬🤖