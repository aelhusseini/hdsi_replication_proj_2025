# 🎓 Educational Setup Guide

## 📚 For Students and Educators

This guide helps you set up the Life Sciences Knowledge Graph Agent for educational use. The setup is designed to be approachable for undergraduate students learning LangGraph and knowledge graphs.

## 🎯 Learning Objectives Setup

After completing this setup, you'll be ready to:
- **Explore knowledge graphs** with real biomedical data
- **Learn LangGraph workflows** through hands-on exercises
- **Practice Cypher queries** with immediate feedback
- **Build AI applications** that combine language models with structured data

## 📋 Prerequisites Installation

### 1. Install Python 3.10+

**For Students**: Python is the programming language we'll use for everything.

Check your Python version:
```bash
python3 --version
```

**If you need to install Python:**
- **macOS**: Download from python.org or use `brew install python`
- **Windows**: Download from python.org and add to PATH
- **Linux**: Use your package manager (e.g., `sudo apt install python3`)

### 2. Install PDM (Python Dependency Manager)

**For Students**: PDM helps us manage all the code libraries we need.

```bash
# macOS/Linux
curl -sSL https://pdm.fming.dev/install-pdm.py | python3 -

# Or using pip if you prefer
pip install --user pdm

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://pdm.fming.dev/install-pdm.py -UseBasicParsing).Content | python -
```

### 3. Install Neo4j Community Edition

**For Students**: Neo4j is our graph database - where we store the biomedical knowledge.

#### 🐳 Option A: Docker (Recommended for Learning)
**Easiest setup, works everywhere:**

```bash
# Start Neo4j in a container
docker run \
    --name neo4j-learning \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/student123 \
    -v neo4j-data:/data \
    neo4j:5-community
```

#### 💻 Option B: Direct Installation
**For more hands-on experience:**

1. Go to https://neo4j.com/download-center/#community
2. Download Neo4j Desktop (easier) or Community Server
3. Follow the installation wizard
4. Set initial password to `student123` (or remember what you use!)

#### ☁️ Option C: Neo4j Aura Free (Cloud)
**No installation needed:**

1. Visit https://neo4j.com/aura/
2. Sign up for free tier
3. Create a new database
4. Save the connection details

## 🚀 Educational Project Setup

### 1. Get the Learning Materials

**For Students**: This downloads all the code and exercises.

```bash
# If you have git (recommended)
git clone <repository-url>
cd hdsi_replication_proj_2025

# If you downloaded a ZIP file
unzip hdsi_replication_proj_2025.zip
cd hdsi_replication_proj_2025
```

### 2. Set Up Your Learning Environment

**For Students**: This installs all the tools we need for the course.

```bash
# Install everything we need
pdm install

# This creates a virtual environment with all dependencies
```

**What this does:**
- Creates an isolated Python environment for our project
- Installs LangGraph, Streamlit, Neo4j drivers, and other tools
- Downloads educational Jupyter notebooks and exercises

### 3. Configure Your Settings

**For Students**: We need to tell the system how to connect to your database and AI services.

Copy the example settings:
```bash
cp .env.example .env
```

Edit `.env` file with your information:
```bash
# For students: You need an Anthropic Claude API key
# Get one free at: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Neo4j connection (adjust if needed)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=student123

# Learning mode settings
APP_ENV=development
LOG_LEVEL=INFO
```

**🔑 Getting API Keys:**
- **Anthropic**: Sign up at https://console.anthropic.com/ (free credits available)
- **Educational discounts**: Ask your instructor about educational API credits

### 4. Test Your Database Connection

**For Students**: Let's make sure everything can talk to each other.

```bash
# Quick connection test
pdm run python -c "from neo4j import GraphDatabase; driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'student123')); print('✅ Neo4j Connected!'); driver.close()"
```

**Expected output:** `✅ Neo4j Connected!`

### 5. Load Educational Data

**For Students**: This fills your database with biomedical knowledge to explore.

```bash
# Load our sample biomedical knowledge graph
pdm run load-data
```

**What you should see:**
```
🚀 Starting Simple Biomedical Knowledge Graph Loader
This educational version focuses on core concepts!

📋 Step 1: Database Preparation
✅ Connected to Neo4j!
🧹 Cleared existing data
🔧 Created database constraints

📋 Step 2: Loading Entities (Nodes)
📍 Loading 30 genes...
✅ Genes loaded!
🧪 Loading 30 proteins...
✅ Proteins loaded and linked to genes!
🏥 Loading 15 diseases...
✅ Diseases loaded!
💊 Loading 20 drugs...
✅ Drugs loaded!

📋 Step 3: Creating Relationships (Edges)
🔗 Creating 30 protein-disease associations...
✅ Protein-disease associations created!
💉 Creating 25 drug treatment relationships...
✅ Drug treatment relationships created!
🎯 Creating 25 drug-protein target relationships...
✅ Drug-protein target relationships created!

📋 Step 4: Computing Derived Relationships
🧬 Creating derived gene-disease links...
✅ Created 30 gene-disease links!

📊 KNOWLEDGE GRAPH SUMMARY
==================================================
🧬 Genes: 30
🧪 Proteins: 30
🏥 Diseases: 15
💊 Drugs: 20

🔗 Relationships:
   ENCODES: 30
   LINKED_TO: 30
   ASSOCIATED_WITH: 30
   TREATS: 25
   TARGETS: 25
==================================================
🎉 Knowledge graph is ready for learning!
```

### 6. Verify Your Learning Environment

**For Students**: Let's make sure you can explore the data.

Open Neo4j Browser at http://localhost:7474 (or your Aura console) and try:

```cypher
// See what we have
MATCH (n) RETURN labels(n)[0] as type, count(n) as count

// Explore some relationships
MATCH (g:Gene)-[:ENCODES]->(p:Protein) RETURN g.gene_name, p.protein_name LIMIT 5
```

## 🎓 Start Learning!

### Option 1: Interactive Tutorial (Recommended for Beginners)
```bash
# Start Jupyter notebook tutorial
jupyter notebook tutorial_langgraph_knowledge_graphs.ipynb
```

### Option 2: Web Interface (Great for Visual Learners)
```bash
# Start the educational web app
pdm run app
```

Then visit http://localhost:8501 and select **"🎓 Educational Mode"**

### Option 3: Quick Test (Verify Everything Works)
```bash
# Run a quick validation
pdm run quickstart
```

## 🧪 Running Tests

**For Students**: Make sure everything is working correctly.

```bash
# Test everything
pdm run test

# You should see 17 tests pass
```

## 🔧 Troubleshooting for Students

### "Can't connect to Neo4j" 

**Problem**: Connection refused or authentication failed
**Solutions**:
1. Check Neo4j is running: look for Neo4j Desktop or Docker container
2. Verify password in `.env` matches what you set
3. Make sure ports 7474 and 7687 aren't blocked
4. Try Neo4j Aura (cloud) if local setup is difficult

### "Anthropic API key not working"

**Problem**: Invalid API key errors
**Solutions**:
1. Verify key starts with `sk-ant-`
2. Check you have API credits remaining
3. Make sure key is correctly pasted in `.env` file
4. Ask instructor about educational API access

### "Streamlit won't start"

**Problem**: Port conflicts or module errors
**Solutions**:
1. Try a different port: `pdm run streamlit run web/app.py --server.port 8502`
2. Make sure you're in the project directory
3. Check PDM installed correctly: `pdm --version`

### "Jupyter notebook won't open"

**Problem**: Jupyter not found
**Solutions**:
1. Install Jupyter: `pdm add jupyter`
2. Or use: `pip install notebook`
3. Alternative: Open `.ipynb` files in VS Code

## 📚 Learning Path Recommendations

### Week 1-2: Foundations
1. **Start here**: Open `tutorial_langgraph_knowledge_graphs.ipynb`
2. **Practice**: Use Educational Mode in Streamlit
3. **Explore**: Try basic Cypher queries in Neo4j Browser

### Week 3-4: Building Skills
1. **Code exploration**: Read through `agent/educational_agent.py`
2. **Exercises**: Complete Level 1-2 in the web interface
3. **Experimentation**: Modify the educational agent code

### Week 5-6: Advanced Projects
1. **Custom agents**: Build your own workflow variations
2. **Real applications**: Design domain-specific use cases
3. **Portfolio**: Document your learning journey

## 🎯 Success Criteria

**You're ready to start learning when:**
- ✅ Neo4j database loads without errors
- ✅ Web app shows "Educational Mode" with 4 tabs
- ✅ Jupyter notebook opens the tutorial
- ✅ All tests pass (`pdm run test`)
- ✅ You can ask questions in the web interface

## 🆘 Getting Help

### For Students:
1. **Check documentation**: `LEARNING_GUIDE.md` has detailed explanations
2. **Use discussion forums**: Ask classmates and instructors
3. **Office hours**: Bring specific error messages
4. **Online resources**: Neo4j and LangGraph have great documentation

### For Instructors:
1. **Teaching materials**: See `docs/` folder for lesson plans
2. **Assessment tools**: Built-in exercises provide learning checkpoints
3. **Customization**: Easily modify exercises for your curriculum
4. **Technical support**: Detailed troubleshooting in this guide

## 🎉 You're Ready!

Once setup is complete, you have:
- **A working knowledge graph** with biomedical data
- **Three types of agents** showing different approaches
- **Interactive tutorials** for hands-on learning
- **Progressive exercises** from beginner to expert
- **A complete learning environment** for exploring LangGraph and knowledge graphs

**Next step**: Open the tutorial notebook and start your learning journey!

```bash
jupyter notebook tutorial_langgraph_knowledge_graphs.ipynb
```

Happy learning! 🚀🧬🤖