# Claude Code Configuration

This file contains configuration and context for Claude Code when working with this biomedical knowledge graph learning project.

## 🎓 Project Overview

This is a **learning platform** designed to teach undergraduate students **LangGraph and knowledge graphs** through hands-on biomedical AI applications. Students learn by building real AI systems that answer biomedical questions using Neo4j graph databases, LangGraph workflows, and Anthropic Claude for natural language processing.

**Learning Focus**: Learn by doing - students build working AI applications while mastering industry-standard tools.

## 🛠️ Key Learning Technologies
- **Neo4j**: Graph database (industry-standard for knowledge storage)
- **LangGraph**: AI agent workflow orchestration (modern AI development framework)
- **Anthropic Claude**: Natural language understanding (educational-friendly AI)
- **Streamlit**: Interactive web interface (approachable for students)
- **PDM**: Python dependency management (modern Python tooling)
- **Python 3.10+**: Programming language (accessible and widely used)

## 📁 Educational Project Structure

```
├── src/                       # 🔧 Source code
│   ├── agents/                   # 🎓 Three Agent Types for Progressive Learning
│   │   ├── educational_agent.py    # 🎓 ACTIVE: Simplified LangGraph (used in web app)
│   │   ├── simple_agent.py         # 📚 EXAMPLE: Template-based (beginner reference)
│   │   ├── langgraph_agent.py      # 📚 EXAMPLE: Full-featured (advanced reference)
│   │   └── graph_interface.py      # Neo4j database interface
│   └── web/                      # 🌐 Interactive Streamlit interface
│       └── app.py                  # Main learning interface
├── educational/               # 📚 All learning materials
│   ├── exercises/
│   │   └── learning_exercises.py  # 🏋️ Progressive exercises (4 difficulty levels)
│   ├── tutorials/
│   │   └── tutorial_langgraph_knowledge_graphs.ipynb  # 📓 Interactive tutorial
│   └── guides/
│       └── LEARNING_GUIDE.md      # 6-week curriculum guide
├── data/                      # 📊 Educational biomedical datasets (synthetic)
├── docs/                      # 📚 Technical documentation
│   ├── USER_GUIDE.md             # Student learning guide
│   ├── SETUP_GUIDE.md            # Educational setup instructions
│   ├── ARCHITECTURE.md           # Learning-focused architecture
│   ├── DEMO_SCRIPT.md            # Educational demonstration script
│   └── PROJECT_SUMMARY.md        # Project overview
├── scripts/                   # 🔧 Learning utilities
│   ├── simple_load_data.py       # Simplified data loader (educational)
│   ├── load_data.py              # Full data loader (advanced)
│   └── quickstart.py             # Setup verification
├── tests/                     # ✅ Test suite (17 tests)
├── config/                    # ⚙️ Configuration files
│   └── CLAUDE.md                 # Claude Code configuration
└── __pypackages__/            # PDM dependencies (auto-managed)
```

## 🎓 Educational Commands

### Student Learning Workflow
```bash
# 1. Setup: Install dependencies
pdm install

# 2. Data: Load educational biomedical dataset
pdm run load-data    # or: python scripts/simple_load_data.py

# 3. Verify: Check system setup
pdm run quickstart

# 4. Learn: Start interactive web interface
pdm run app          # Interactive learning interface

# 5. Tutorial: Open Jupyter notebook tutorial
jupyter notebook tutorial_langgraph_knowledge_graphs.ipynb

# 6. Validate: Run all tests
pdm run test         # Should see 17 tests pass

# 7. Quality: Check code formatting
pdm run lint && pdm run format
```

### Advanced Development Workflow
```bash
# Full data loading (larger dataset)
python scripts/load_data.py

# Specific agent testing
pdm run test tests/test_educational_agent.py  # (when created)

# Performance testing
pdm run test -k "integration"
```

### 🔑 Environment Setup
```bash
# Copy example environment file
cp .env.example .env

# Edit with your credentials (required for students)
# NEO4J_PASSWORD=student123  # (or your chosen password)
# ANTHROPIC_API_KEY=sk-ant-your-key  # (get free credits at console.anthropic.com)
```

## 📋 Educational Development Guidelines

### 🎯 Learning Objectives
- **Week 1-2**: Basic graph concepts and simple queries
- **Week 3-4**: LangGraph workflows and state management  
- **Week 5-6**: Complex agents and real-world applications

### 📐 Code Quality (Learning-Focused)
- **Line length**: 88 characters (industry standard)
- **Formatting**: Black + isort (`pdm run format`)
- **Linting**: Flake8 + MyPy (`pdm run lint`)
- **Testing**: Pytest (`pdm run test` - all 17 tests should pass)
- **Comments**: Extensive educational comments in `educational_agent.py`

### 🗄️ Database Operations (Student Safety)
- Use educational synthetic data (safe for learning)
- Always use parameterized queries (prevent injection)
- Use GraphInterface class for all database interactions
- Clear/rebuild database with `simple_load_data.py` for fresh starts
- Schema designed for educational exploration

### 🤖 AI Agent Development (Progressive Learning)
- **EducationalAgent**: 🎓 ACTIVE - Simplified LangGraph used in web app (learning-focused with print statements)
- **SimpleAgent**: 📚 EXAMPLE - Template-based queries (beginner-friendly reference)
- **LifeScienceAgent**: 📚 EXAMPLE - Full-featured (advanced students reference)
- Always validate generated Cypher queries before execution
- Handle errors gracefully with educational feedback

**Note**: The web application uses only EducationalAgent. The other agents serve as educational examples for students to study different implementation approaches.

## 🔐 Educational Environment Variables

Create `.env` file with these educational-friendly settings:
```bash
# Anthropic API Configuration (get free credits for education)
ANTHROPIC_API_KEY=sk-ant-your_educational_api_key_here

# Neo4j Database Configuration (local development)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=student123  # or your chosen password

# Application Configuration
APP_ENV=learning     # Optimized for learning
LOG_LEVEL=INFO       # Good for debugging while learning
```

## 📊 Educational Database Schema

### 🧬 Node Types (Designed for Learning)
- **Gene**: Educational genes (GENE_ALPHA, GENE_BETA, etc.) with clear naming
- **Protein**: Proteins (PROT_ALPHA, PROT_BETA, etc.) with educational properties
- **Disease**: Common diseases (diabetes, hypertension, etc.) for relevance
- **Drug**: Sample drugs (AlphaCure, BetaTherapy, etc.) for learning scenarios

### 🔗 Relationship Types (Core Graph Concepts)
- **ENCODES**: Gene → Protein (central dogma of biology)
- **LINKED_TO**: Gene → Disease (derived relationships for advanced learning)
- **ASSOCIATED_WITH**: Protein → Disease (experimental associations)
- **TREATS**: Drug → Disease (therapeutic relationships)
- **TARGETS**: Drug → Protein (molecular mechanisms)

**Educational Design**: Clear, learnable relationships that demonstrate graph thinking!

## 🛠️ Educational Troubleshooting

### 🎓 Common Student Issues

1. **"Neo4j Connection Failed" (Most Common)**
   ```bash
   # Step 1: Check if Neo4j is running (look for Neo4j Desktop or Docker)
   # Step 2: Verify password in .env matches what you set
   # Step 3: Run diagnostics
   pdm run quickstart
   
   # Educational tip: This teaches database connectivity concepts!
   ```

2. **"API Key Not Working"**
   ```bash
   # Check .env file has correct ANTHROPIC_API_KEY format
   # Visit https://console.anthropic.com/ for free educational credits
   # Make sure key starts with 'sk-ant-'
   ```

3. **"No Results Found" in Queries**
   ```bash
   # Check if data is loaded: python scripts/simple_load_data.py
   # Use educational entity names: GENE_ALPHA, diabetes, AlphaCure
   # Try simpler queries first in the Explore Queries tab
   ```

4. **"Import Errors"**
   ```bash
   # Make sure you're in project root directory
   # Reinstall dependencies: pdm install
   # Educational note: This teaches Python project structure!
   ```

5. **"Tests Failing"**
   ```bash
   # Should see "17 passed" - if not, check setup
   pdm run test -v  # verbose output for debugging
   
   # Run specific test file for learning
   pdm run test tests/test_graph_interface.py
   ```

6. **"Jupyter Notebook Won't Open"**
   ```bash
   # Install Jupyter: pdm add jupyter
   # Or open .ipynb files in VS Code
   # Alternative: Use the web interface Educational Mode instead
   ```

## 📁 File Patterns for Students

**Safe to ignore** (auto-generated):
- `__pycache__/` - Python bytecode cache
- `.mypy_cache/` - Type checker cache  
- `.pytest_cache/` - Test cache
- `__pypackages__/` - PDM dependencies (auto-managed)
- `.pdm-build/` - Build artifacts

**Focus on these** (your code):
- `src/agents/` - AI agent implementations (study these!)
- `src/web/app.py` - Main interface (modify for projects)
- `educational/exercises/learning_exercises.py` - Practice exercises
- `educational/tutorials/tutorial_*.ipynb` - Interactive learning materials

## ⚡ Educational Performance Notes

- **Database queries**: Limited to 10-20 results (good for learning, not overwhelming)
- **AI models**: Haiku for simple tasks, Sonnet for complex (cost-effective for education)
- **Caching**: Streamlit caches agents (faster response for classroom use)
- **Educational data**: Small datasets optimized for learning and exploration

## 🔒 Educational Security & Safety

- **Synthetic data**: No real patient/clinical data (safe for learning)
- **Environment isolation**: Local development environment for safe learning
- **API limits**: Educational rate limits prevent excessive usage
- **Version control**: Never commit `.env` files (use `.env.example`)
- **Input validation**: All user inputs validated (good security practices)

## 🧪 Educational Testing Strategy

- **17 comprehensive tests**: Cover all major functionality
- **Mock dependencies**: Safe testing without external services
- **Educational data**: Small, predictable test datasets
- **Learning opportunity**: Students can read tests to understand expected behavior
- **CI/CD ready**: Tests run quickly for iterative development

## 📚 Educational Documentation Standards

- **Student-friendly**: Clear explanations with learning objectives
- **Progressive complexity**: Beginner → Intermediate → Advanced
- **Code examples**: Working examples in every major section
- **Biological context**: Real-world applications to motivate learning
- **Portfolio ready**: Students can showcase projects built with this platform

## 🚀 Educational Deployment Options

**For Students** (Recommended):
1. Local development with Docker Neo4j
2. Neo4j Aura free tier (cloud)
3. Classroom shared Neo4j instance

**For Instructors**:
1. Classroom server deployment
2. Student portfolio hosting (Streamlit Cloud)
3. Assessment integration with LMS systems

## 🎓 Student Contribution Guidelines

**Learning by Contributing**:
1. Run tests first: `pdm run test` (should see 17 passed)
2. Check code quality: `pdm run lint && pdm run format`
3. Add educational comments to your modifications
4. Create learning exercises for other students
5. Document your learning journey in project README
6. Follow the educational code patterns and conventions

**Portfolio Development**:
- Build on the educational foundation provided
- Create domain-specific variations (finance, social networks, etc.)
- Showcase progressive skill development
- Document real learning outcomes achieved