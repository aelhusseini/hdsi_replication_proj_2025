"""
Progressive Learning Exercises for LangGraph and Knowledge Graphs

This module contains structured exercises that build from basic concepts
to advanced implementations, designed for beginner to advanced users.

To use these exercises:
1. Set up your environment with: pdm install
2. Load data with: pdm run load-data
3. Start with Level 1 exercises and progress through each level
4. Use the actual entity names from the database (TP53, BRCA1, Hypertension, Lisinopril, etc.)

Required imports for practical use:
```python
from src.agents.graph_interface import GraphInterface
from src.agents.workflow_agent import WorkflowAgent, WorkflowState
```
"""

from typing import Any, Dict, List, cast

# ============================================================================
# LEVEL 1: Knowledge Graph Fundamentals
# ============================================================================

LEVEL_1_EXERCISES = {
    "title": "Level 1: Knowledge Graph Fundamentals",
    "description": "Learn the basics of nodes, relationships, and graph thinking",
    "exercises": [
        {
            "id": "1.1",
            "title": "Understanding Nodes and Relationships",
            "difficulty": "Beginner",
            "description": """
            In our biomedical knowledge graph, we have 4 types of nodes:
            - Genes (genetic sequences)
            - Proteins (encoded by genes)
            - Diseases (medical conditions)
            - Drugs (treatments)
            Task: Write simple queries to explore each node type.
            """,
            "tasks": [
                {
                    "question": "Find 5 genes in our database",
                    "hint": "Use MATCH (g:Gene) RETURN ...",
                    "solution": "MATCH (g:Gene) RETURN g.gene_name LIMIT 5",
                    "learning_point": "Basic node matching with labels",
                },
                {
                    "question": "Find all diseases and their categories",
                    "hint": "Disease nodes have a 'category' property",
                    "solution": "MATCH (d:Disease) RETURN d.disease_name, d.category",
                    "learning_point": "Accessing node properties",
                },
                {
                    "question": "Find drugs that are 'small_molecule' type",
                    "hint": "Use WHERE to filter by the 'type' property",
                    "solution": (
                        "MATCH (dr:Drug) WHERE dr.type = 'small_molecule' "
                        "RETURN dr.drug_name"
                    ),
                    "learning_point": "Filtering nodes with WHERE clause",
                },
            ],
        },
        {
            "id": "1.2",
            "title": "Basic Relationships",
            "difficulty": "Beginner",
            "description": """
            Relationships connect nodes and represent biological interactions:
            - ENCODES: Gene → Protein
            - TREATS: Drug → Disease
            - TARGETS: Drug → Protein
            - ASSOCIATED_WITH: Protein → Disease
            - LINKED_TO: Gene → Disease
            """,
            "tasks": [
                {
                    "question": "Find which proteins are encoded by genes",
                    "hint": "Use the ENCODES relationship",
                    "solution": (
                        "MATCH (g:Gene)-[:ENCODES]->(p:Protein) "
                        "RETURN g.gene_name, p.protein_name LIMIT 5"
                    ),
                    "learning_point": "Following relationships between nodes",
                },
                {
                    "question": "Find which drugs treat diseases",
                    "hint": "Use the TREATS relationship",
                    "solution": (
                        "MATCH (dr:Drug)-[:TREATS]->(d:Disease) "
                        "RETURN dr.drug_name, d.disease_name LIMIT 5"
                    ),
                    "learning_point": "Understanding directional relationships",
                },
            ],
        },
    ],
}

# ============================================================================
# LEVEL 2: Cypher Query Mastery
# ============================================================================

LEVEL_2_EXERCISES = {
    "title": "Level 2: Cypher Query Mastery",
    "description": "Master the Cypher query language for complex graph traversal",
    "exercises": [
        {
            "id": "2.1",
            "title": "Advanced Filtering and Patterns",
            "difficulty": "Intermediate",
            "description": """
            Learn to combine multiple conditions and traverse longer paths.
            """,
            "tasks": [
                {
                    "question": "Find genes on chromosome 1 that encode proteins",
                    "hint": "Combine node filtering with relationship traversal",
                    "solution": (
                        "MATCH (g:Gene)-[:ENCODES]->(p:Protein) "
                        "WHERE g.chromosome = '1' "
                        "RETURN g.gene_name, p.protein_name"
                    ),
                    "learning_point": "Combining WHERE clauses with relationships",
                },
                {
                    "question": "Find high-efficacy drugs for neurological diseases",
                    "hint": "Filter by disease category and treatment efficacy",
                    "solution": (
                        "MATCH (dr:Drug)-[t:TREATS]->(d:Disease) "
                        "WHERE d.category = 'neurological' AND t.efficacy = 'high' "
                        "RETURN dr.drug_name, d.disease_name"
                    ),
                    "learning_point": "Accessing relationship properties",
                },
                {
                    "question": "Find the most common disease categories",
                    "hint": "Use GROUP BY and COUNT functions",
                    "solution": (
                        "MATCH (d:Disease) "
                        "RETURN d.category, count(*) as disease_count "
                        "ORDER BY disease_count DESC"
                    ),
                    "learning_point": "Aggregation and sorting in Cypher",
                },
            ],
        },
        {
            "id": "2.2",
            "title": "Multi-hop Relationships",
            "difficulty": "Intermediate",
            "description": """
            Traverse multiple relationships to find complex biological pathways.
            """,
            "tasks": [
                {
                    "question": "Find the complete path: Gene → Protein → Disease",
                    "hint": "Chain two relationships together",
                    "solution": (
                        "MATCH (g:Gene)-[:ENCODES]->(p:Protein)"
                        "-[:ASSOCIATED_WITH]->(d:Disease) "
                        "RETURN g.gene_name, p.protein_name, d.disease_name LIMIT 5"
                    ),
                    "learning_point": "Chaining multiple relationships",
                },
                {
                    "question": (
                        "Find genes that are indirectly linked to treatments "
                        "(Gene → Protein → Disease ← Drug)"
                    ),
                    "hint": (
                        "Use 3 relationships to connect genes to drugs "
                        "through proteins and diseases"
                    ),
                    "solution": (
                        "MATCH (g:Gene)-[:ENCODES]->(p:Protein)"
                        "-[:ASSOCIATED_WITH]->(d:Disease)<-[:TREATS]-(dr:Drug) "
                        "RETURN g.gene_name, dr.drug_name, d.disease_name LIMIT 5"
                    ),
                    "learning_point": (
                        "Complex path traversal and bidirectional relationships"
                    ),
                },
            ],
        },
    ],
}

# ============================================================================
# LEVEL 3: LangGraph Workflows
# ============================================================================

LEVEL_3_EXERCISES = {
    "title": "Level 3: LangGraph Workflows",
    "description": "Build AI agents with multi-step reasoning workflows",
    "exercises": [
        {
            "id": "3.1",
            "title": "Understanding State Flow",
            "difficulty": "Advanced",
            "description": """
            Learn how information flows through LangGraph workflows
            using state management.
            """,
            "tasks": [
                {
                    "question": "Trace through our learning agent's workflow",
                    "hint": "Follow the state from initial question to final answer",
                    "code_example": """
# Example state progression:
initial_state = {
    'user_question': 'What genes are associated with diabetes?',
    'question_type': None,
    'entities': None,
    'cypher_query': None,
    'results': None,
    'final_answer': None
}

# After classify step:
state = {
    'user_question': 'What genes are associated with diabetes?',
    'question_type': 'gene_disease',  # Added by classify
    'entities': None,
    'cypher_query': None,
    'results': None,
    'final_answer': None
}

# Continue tracing through extract, generate, execute, format...
                    """,
                    "learning_point": "State management and data flow in LangGraph",
                }
            ],
        },
        {
            "id": "3.2",
            "title": "Building Custom Workflow Nodes",
            "difficulty": "Advanced",
            "description": """
            Create your own workflow nodes and understand the
            LangGraph architecture.
            """,
            "tasks": [
                {
                    "question": "Add a validation node to check generated queries",
                    "hint": (
                        "Create a function that validates Cypher syntax "
                        "before execution"
                    ),
                    "code_template": """
def validate_query(state: WorkflowState) -> WorkflowState:
    \"\"\"Validate the generated Cypher query before execution.\"\"\"
    query = state.get('cypher_query')
    if query:
        # Add your validation logic here
        if graph_db.validate_query(query):
            # Query is valid, continue
            pass
        else:
            # Query is invalid, set error
            state['error'] = 'Generated query is invalid'
    return state
                    """,
                    "learning_point": "Custom node creation and error handling",
                },
                {
                    "question": (
                        "Add conditional routing based on question complexity"
                    ),
                    "hint": (
                        "Use add_conditional_edges to route simple vs complex "
                        "questions differently"
                    ),
                    "code_template": """
# Add this to your workflow:
workflow.add_conditional_edges(
    'classify',
    lambda state: (
        'simple_path' if is_simple_question(state) else 'complex_path'
    ),
    {
        'simple_path': 'simple_handler',
        'complex_path': 'extract_entities'
    }
)
                    """,
                    "learning_point": "Conditional workflow routing",
                },
            ],
        },
    ],
}

# ============================================================================
# LEVEL 4: Real-World Applications
# ============================================================================

LEVEL_4_EXERCISES = {
    "title": "Level 4: Real-World Applications",
    "description": (
        "Apply your knowledge to build practical biomedical AI applications"
    ),
    "exercises": [
        {
            "id": "4.1",
            "title": "Drug Discovery Assistant",
            "difficulty": "Expert",
            "description": """
            Build a specialized agent for drug discovery research.
            """,
            "tasks": [
                {
                    "question": (
                        "Create an agent that finds potential drug repurposing "
                        "opportunities"
                    ),
                    "hint": (
                        "Find drugs that treat diseases sharing biological pathways"
                    ),
                    "approach": [
                        "1. Identify diseases with shared protein associations",
                        "2. Find drugs that treat one disease",
                        "3. Suggest these drugs for the related disease",
                        "4. Rank by confidence based on shared pathways",
                    ],
                    "learning_point": "Applied AI for scientific discovery",
                }
            ],
        },
        {
            "id": "4.2",
            "title": "Personalized Medicine Advisor",
            "difficulty": "Expert",
            "description": """
            Build an agent that considers genetic factors for treatment
            recommendations.
            """,
            "tasks": [
                {
                    "question": (
                        "Create a workflow that suggests treatments based on "
                        "patient genetics"
                    ),
                    "hint": ("Combine genetic variants with drug effectiveness data"),
                    "approach": [
                        "1. Input: Patient genetic profile and disease",
                        "2. Find genes associated with the disease",
                        "3. Check if patient has relevant genetic variants",
                        "4. Recommend drugs that target affected pathways",
                        "5. Provide confidence scores and explanations",
                    ],
                    "learning_point": "Personalized AI applications in healthcare",
                }
            ],
        },
    ],
}

# ============================================================================
# Exercise Progression System
# ============================================================================

EXERCISE_PROGRESSION: Dict[str, Dict[str, Any]] = {
    "beginner": {
        "requirements": [],
        "exercises": ["1.1", "1.2"],
        "next_level": "intermediate",
    },
    "intermediate": {
        "requirements": ["1.1", "1.2"],
        "exercises": ["2.1", "2.2"],
        "next_level": "advanced",
    },
    "advanced": {
        "requirements": ["1.1", "1.2", "2.1", "2.2"],
        "exercises": ["3.1", "3.2"],
        "next_level": "expert",
    },
    "expert": {
        "requirements": ["1.1", "1.2", "2.1", "2.2", "3.1", "3.2"],
        "exercises": ["4.1", "4.2"],
        "next_level": None,
    },
}

# ============================================================================
# Assessment Rubric
# ============================================================================

ASSESSMENT_CRITERIA = {
    "knowledge_graphs": {
        "novice": "Can identify nodes and relationships in simple examples",
        "competent": "Can write basic Cypher queries for single relationships",
        "proficient": "Can traverse multi-hop relationships and use advanced filtering",
        "expert": "Can design graph schemas and optimize complex queries",
    },
    "langgraph": {
        "novice": "Understands the concept of workflow state",
        "competent": "Can trace state changes through existing workflows",
        "proficient": "Can modify workflows and add new nodes",
        "expert": "Can design complete workflows with conditional logic",
    },
    "biomedical_application": {
        "novice": ("Understands basic biological relationships (gene→protein→disease)"),
        "competent": ("Can formulate biomedical questions as graph queries"),
        "proficient": ("Can build agents for specific biomedical use cases"),
        "expert": ("Can design novel applications and evaluate their impact"),
    },
}

# ============================================================================
# Learning Resources and Next Steps
# ============================================================================

LEARNING_RESOURCES = {
    "documentation": [
        {
            "title": "Neo4j Cypher Manual",
            "url": "https://neo4j.com/docs/cypher-manual/current/",
            "description": "Complete reference for Cypher query language",
        },
        {
            "title": "LangGraph Documentation",
            "url": "https://langchain-ai.github.io/langgraph/",
            "description": "Official LangGraph documentation and tutorials",
        },
        {
            "title": "Graph Databases Book",
            "url": "https://neo4j.com/graph-databases-book/",
            "description": "Free book on graph database concepts and applications",
        },
    ],
    "practice_datasets": [
        {
            "name": "Movie Recommendation Graph",
            "description": (
                "Build a movie recommendation system using "
                "actor/director/genre relationships"
            ),
        },
        {
            "name": "Social Network Analysis",
            "description": ("Analyze friendship networks and information propagation"),
        },
        {
            "name": "Supply Chain Optimization",
            "description": (
                "Model supply chains as graphs for optimization and " "risk analysis"
            ),
        },
    ],
    "project_ideas": [
        {
            "title": "Academic Paper Citation Network",
            "description": (
                "Build a knowledge graph of research papers and their citations"
            ),
            "difficulty": "Intermediate",
            "skills": ["Graph modeling", "Data ingestion", "Network analysis"],
        },
        {
            "title": "Recipe Recommendation Engine",
            "description": (
                "Create a graph of ingredients, recipes, and dietary preferences"
            ),
            "difficulty": "Intermediate",
            "skills": ["Recommendation algorithms", "User modeling", "Graph queries"],
        },
        {
            "title": "Financial Risk Assessment System",
            "description": (
                "Model financial entities and their relationships for " "risk analysis"
            ),
            "difficulty": "Advanced",
            "skills": ["Complex graph traversal", "Real-time updates", "Risk modeling"],
        },
    ],
}


def get_exercises_for_level(level: str) -> dict:
    """Get exercises for a specific difficulty level."""
    level_mapping = {
        "beginner": LEVEL_1_EXERCISES,
        "intermediate": LEVEL_2_EXERCISES,
        "advanced": LEVEL_3_EXERCISES,
        "expert": LEVEL_4_EXERCISES,
    }
    return level_mapping.get(level, LEVEL_1_EXERCISES)


def check_prerequisites(completed_exercises: list[str], target_level: str) -> bool:
    """Check if user has completed prerequisites for target level."""
    if target_level not in EXERCISE_PROGRESSION:
        return False

    required = EXERCISE_PROGRESSION[target_level]["requirements"]
    return all(ex in completed_exercises for ex in required)


def get_next_recommended_exercise(completed_exercises: list[str]) -> str:
    """Recommend the next exercise based on completed work."""
    for level, info in EXERCISE_PROGRESSION.items():
        if check_prerequisites(completed_exercises, level):
            exercises = cast(List[str], info.get("exercises", []))
            for exercise_id in exercises:
                if exercise_id not in completed_exercises:
                    return exercise_id
    return "4.2"  # Default to final exercise


# ============================================================================
# PRACTICAL EXAMPLES WITH REAL DATA
# ============================================================================

REAL_DATA_EXAMPLES = {
    "sample_entities": {
        "genes": ["TP53", "BRCA1", "BRCA2", "KRAS", "EGFR"],
        "diseases": [
            "Hypertension",
            "Coronary_Artery_Disease",
            "Heart_Failure",
            "Type2_Diabetes",
            "Breast_Cancer",
        ],
        "drugs": ["Lisinopril", "Enalapril", "Atorvastatin", "Metformin", "Aspirin"],
        "proteins": ["TP53", "BRCA1", "BRCA2_iso1", "KRAS", "EGFR"],
    },
    "working_queries": {
        "basic": [
            "MATCH (g:Gene) WHERE g.gene_name = 'TP53' RETURN g",
            "MATCH (d:Disease) WHERE d.category = 'cardiovascular' RETURN d.disease_name LIMIT 5",
            "MATCH (dr:Drug) WHERE dr.drug_name = 'Lisinopril' RETURN dr",
        ],
        "relationships": [
            "MATCH (g:Gene {gene_name: 'TP53'})-[:ENCODES]->(p:Protein) RETURN p.protein_name",
            "MATCH (dr:Drug {drug_name: 'Lisinopril'})-[:TREATS]->(d:Disease) RETURN d.disease_name",
            "MATCH (dr:Drug)-[:TARGETS]->(p:Protein) WHERE dr.drug_name = 'Enalapril' RETURN p.protein_name",
        ],
        "complex": [
            "MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease) WHERE g.gene_name = 'BRCA1' RETURN d.disease_name",
            "MATCH (dr:Drug)-[:TARGETS]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease) WHERE d.category = 'cardiovascular' RETURN dr.drug_name, d.disease_name LIMIT 5",
        ],
    },
    "common_patterns": {
        "find_treatments": "MATCH (dr:Drug)-[:TREATS]->(d:Disease) WHERE toLower(d.disease_name) CONTAINS $disease_name RETURN dr.drug_name",
        "gene_to_disease": "MATCH (g:Gene)-[:LINKED_TO]->(d:Disease) WHERE g.gene_name = $gene_name RETURN d.disease_name",
        "drug_targets": "MATCH (dr:Drug)-[:TARGETS]->(p:Protein) WHERE dr.drug_name = $drug_name RETURN p.protein_name",
        "pathway_analysis": "MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)<-[:TREATS]-(dr:Drug) RETURN g.gene_name, dr.drug_name, d.disease_name",
    },
}
