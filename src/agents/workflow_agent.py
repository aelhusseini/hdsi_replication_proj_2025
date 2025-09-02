"""
🎓 ACTIVE AGENT: Educational LangGraph Workflow for Biomedical Knowledge Graphs

✅ This is the primary agent used in the web application!

This educational agent demonstrates core LangGraph workflow concepts through
biomedical AI applications. Users learn by building real AI systems that answer
biomedical questions using natural language processing and graph databases.

Learning Focus:
1. LangGraph workflow orchestration and state management
2. Knowledge graph querying with natural language interfaces
3. Multi-step AI reasoning for complex domain questions
4. Integration of language models with structured knowledge

Educational Design:
- Simple, transparent 5-step workflow for clarity
- Extensive comments and print statements for learning
- Real biomedical examples with genes, proteins, diseases, drugs
- Progressive complexity from basic to advanced concepts
"""

import json
from typing import Dict, List, Optional, TypedDict

from anthropic import Anthropic
from langgraph.graph import END, StateGraph

from .graph_interface import GraphInterface


class WorkflowState(TypedDict):
    """
    State that flows through our simplified workflow.

    Think of this as a shared notebook that each step can read and write to.
    Each field gets filled in as we progress through the workflow.
    """

    user_question: str  # Original question from user
    question_type: Optional[str]  # What kind of biomedical question is this?
    entities: Optional[List[str]]  # Important terms we found (genes, diseases, etc.)
    cypher_query: Optional[str]  # The database query we generated
    results: Optional[List[Dict]]  # What we found in the database
    final_answer: Optional[str]  # Human-readable response
    error: Optional[str]  # If something went wrong


class WorkflowAgent:
    """
    An educational LangGraph workflow agent for biomedical knowledge graphs.

    This agent demonstrates the fundamental LangGraph workflow pattern:
    Input → Classify → Extract → Generate → Execute → Format → Output

    Educational Value:
    - Learn LangGraph state management through clear examples
    - Understand multi-step AI reasoning with biomedical applications
    - See how natural language converts to structured graph queries
    - Experience real-world AI agent architecture patterns

    Workflow Steps:
    1. Classify: Determine the type of biomedical question
    2. Extract: Find specific entities (genes, diseases, drugs)
    3. Generate: Create appropriate Cypher database queries
    4. Execute: Run queries against the Neo4j knowledge graph
    5. Format: Convert results into human-readable responses

    Comparison to Other Agents:
    - vs AdvancedWorkflowAgent: Same workflow, simpler implementation
    - vs TemplateQueryAgent: Uses AI vs pre-written templates
    """

    def __init__(self, graph_interface: GraphInterface, anthropic_api_key: str):
        self.graph_db = graph_interface
        self.anthropic = Anthropic(api_key=anthropic_api_key)

        # Get the database structure so we know what data is available
        self.schema = self.graph_db.get_schema_info()

        # Build our workflow - this is the heart of LangGraph!
        self.workflow = self._create_workflow()

    def _create_workflow(self):
        """
        Create our LangGraph workflow - the heart of the educational agent.

        This method demonstrates core LangGraph concepts:
        - Building a state graph with connected processing nodes
        - Defining workflow steps and their relationships
        - Creating a linear pipeline for educational clarity

        Think of this as building a flowchart where each step processes
        the shared state and passes it to the next step.
        """
        # Step 1: Create the graph structure
        workflow = StateGraph(WorkflowState)

        # Step 2: Add our processing nodes (each node is a function)
        workflow.add_node("classify", self.classify_question)
        workflow.add_node("extract", self.extract_entities)
        workflow.add_node("generate", self.generate_query)
        workflow.add_node("execute", self.execute_query)
        workflow.add_node("format", self.format_answer)

        # Step 3: Connect the nodes (define the flow)
        workflow.add_edge("classify", "extract")  # classify → extract
        workflow.add_edge("extract", "generate")  # extract → generate
        workflow.add_edge("generate", "execute")  # generate → execute
        workflow.add_edge("execute", "format")  # execute → format
        workflow.add_edge("format", END)  # format → END

        # Step 4: Set where to start
        workflow.set_entry_point("classify")

        # Step 5: Compile into executable workflow
        return workflow.compile()

    def classify_question(self, state: WorkflowState) -> WorkflowState:
        """
        Step 1: Figure out what type of biomedical question this is.

        This helps us choose the right query pattern later.
        Common types: gene-disease, drug-treatment, protein-function
        """
        prompt = f"""
        What type of biomedical question is this? Choose one:
        - gene_disease: asking about genes and diseases
        - drug_treatment: asking about drugs and treatments
        - protein_function: asking about proteins and their roles
        - general: other biomedical questions

        Question: {state['user_question']}

        Just respond with the type (like "gene_disease").
        """

        # Ask Claude to classify the question
        response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=20,
            messages=[{"role": "user", "content": prompt}],
        )

        # Extract the response and update our state
        content = response.content[0]
        if hasattr(content, "text"):
            question_type = content.text.strip()
        else:
            question_type = str(content)
        state["question_type"] = question_type

        print(f"🔍 Question classified as: {question_type}")
        return state

    def extract_entities(self, state: WorkflowState) -> WorkflowState:
        """
        Step 2: Find the important biomedical terms in the question.

        These are the specific things we'll search for in our knowledge graph.
        Examples: "diabetes", "GENE_ALPHA", "aspirin"
        """
        prompt = f"""
        Extract the important biomedical terms from this question.
        Look for specific names of:
        - Genes (like GENE_ALPHA, BRCA1)
        - Diseases (like diabetes, cancer)
        - Drugs (like aspirin, AlphaCure)
        - Proteins (like PROT_BETA, insulin)

        Question: {state['user_question']}

        Return just a simple list like: ["diabetes", "GENE_ALPHA"]
        If you don't find any specific terms, return: []
        """

        response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            # Try to parse the list from Claude's response
            content = response.content[0]
            if hasattr(content, "text"):
                response_text = content.text.strip()
            else:
                response_text = str(content)
            entities = json.loads(response_text)
            state["entities"] = entities
            print(f"🧬 Found entities: {entities}")
        except Exception:
            # If parsing fails, just use empty list
            state["entities"] = []
            print("🧬 No specific entities found")

        return state

    def generate_query(self, state: WorkflowState) -> WorkflowState:
        """
        Step 3: Create a database query to find the answer.

        This is where we convert natural language into Cypher (Neo4j's query language).
        This is one of the most important learning concepts!
        """
        # Build context about our database structure
        schema_info = f"""
        Our knowledge graph has:
        - Nodes: {', '.join(self.schema['node_labels'])}
        - Relationships: {', '.join(self.schema['relationship_types'])}
        Common patterns:
        - Gene -[:ENCODES]-> Protein
        - Gene -[:LINKED_TO]-> Disease
        - Drug -[:TREATS]-> Disease
        - Drug -[:TARGETS]-> Protein
        """

        entities_text = f"Important terms: {state.get('entities', [])}"

        prompt = f"""
        Create a Neo4j Cypher query to answer this biomedical question.
        {schema_info}

        Question: {state['user_question']}
        Question type: {state.get('question_type', 'general')}
        {entities_text}

        Guidelines:
        1. Use MATCH to find patterns
        2. Use WHERE to filter (like: WHERE toLower(d.disease_name)
           CONTAINS toLower("diabetes"))
        3. Use RETURN to get results
        4. Add LIMIT 10 for performance
        Return ONLY the Cypher query, nothing else.
        """

        response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )

        # Clean up the query (remove code block formatting if present)
        content = response.content[0]
        if hasattr(content, "text"):
            cypher_query = content.text.strip()
        else:
            cypher_query = str(content)
        if cypher_query.startswith("```"):
            lines = cypher_query.split("\n")
            cypher_query = "\n".join(
                line
                for line in lines
                if not line.startswith("```") and not line.startswith("cypher")
            )

        state["cypher_query"] = cypher_query
        print(f"🔧 Generated query: {cypher_query}")
        return state

    def execute_query(self, state: WorkflowState) -> WorkflowState:
        """
        Step 4: Run our query against the knowledge graph.

        This is where we actually search the database and get results.
        """
        try:
            # Execute the query we generated
            query = state.get("cypher_query")
            if query:
                results = self.graph_db.execute_query(query)
            else:
                results = []
            state["results"] = results
            print(f"📊 Found {len(results)} results")

        except Exception as e:
            # If something goes wrong, save the error
            state["error"] = f"Query failed: {str(e)}"
            state["results"] = []
            print(f"❌ Query error: {e}")

        return state

    def format_answer(self, state: WorkflowState) -> WorkflowState:
        """
        Step 5: Convert our database results into a human-readable answer.

        This takes the raw data and makes it understandable for users.
        """
        # Handle errors first
        if state.get("error"):
            state["final_answer"] = (
                f"Sorry, I had trouble with that question: {state['error']}"
            )
            return state

        # Handle empty results
        results = state.get("results")
        if not results or len(results) == 0:
            state["final_answer"] = (
                "I didn't find any information for that question. "
                "Try asking about genes, diseases, or drugs in our database."
            )
            return state

        # Format the results nicely
        # results already defined above
        prompt = f"""
        Convert these database results into a clear, informative answer.
        Original question: {state['user_question']}
        Database results: {json.dumps(results[:5], indent=2)}
        Total results found: {len(results)}

        Make the answer:
        1. Easy to understand for users
        2. Informative about the biomedical relationships
        3. Mention how many results were found

        Keep it concise but helpful.
        """

        response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.content[0]
        if hasattr(content, "text"):
            state["final_answer"] = content.text.strip()
        else:
            state["final_answer"] = str(content)
        print("✅ Generated final answer")
        return state

    def answer_question(self, question: str) -> Dict[str, object]:
        """
        Main method: Answer a biomedical question using our LangGraph workflow.

        This is what users will call to see the agent in action.
        It runs through all our steps and returns the complete result.
        """
        print("\n🎓 Learning Workflow Starting...")
        print(f"Question: {question}\n")

        # Create initial state
        initial_state = WorkflowState(
            user_question=question,
            question_type=None,
            entities=None,
            cypher_query=None,
            results=None,
            final_answer=None,
            error=None,
        )

        # Run the workflow! This is where LangGraph magic happens
        final_state = self.workflow.invoke(initial_state)

        print("\n🎯 Workflow Complete!\n")

        # Return everything for detailed inspection
        return {
            "answer": final_state.get("final_answer", "No answer generated"),
            "question_type": final_state.get("question_type"),
            "entities": final_state.get("entities", []),
            "cypher_query": final_state.get("cypher_query"),
            "results_count": len(final_state.get("results", [])),
            "raw_results": final_state.get("results", [])[
                :3
            ],  # Show first 3 for learning
            "error": final_state.get("error"),
        }


# Helper function for users
def demonstrate_workflow_steps():
    """
    Show users what each step in the workflow does.
    This is for learning purposes only.
    """
    steps = [
        ("1. Classify", "Determine what type of biomedical question this is"),
        ("2. Extract", "Find important biomedical terms (genes, diseases, drugs)"),
        ("3. Generate", "Create a database query to find the answer"),
        ("4. Execute", "Run the query against our knowledge graph"),
        ("5. Format", "Convert results into a human-readable answer"),
    ]

    print("🎓 LangGraph Workflow Steps:")
    print("=" * 50)
    for step_name, description in steps:
        print(f"{step_name}: {description}")
    print("=" * 50)
    print(
        "Each step reads the current state, does its work, and updates "
        "the state for the next step!"
    )


def create_workflow_graph(config=None):
    """
    Factory function for LangGraph Studio.
    
    LangGraph Studio expects a factory function that creates the graph.
    This function sets up the agent and returns the compiled workflow.
    """
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    from .graph_interface import GraphInterface
    
    # Get environment variables
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Create graph interface
    graph_interface = GraphInterface(
        uri=neo4j_uri,
        user=neo4j_user,
        password=neo4j_password
    )
    
    # Create workflow agent
    agent = WorkflowAgent(
        graph_interface=graph_interface,
        anthropic_api_key=anthropic_api_key
    )
    
    # Return the compiled workflow
    return agent.workflow


# Create a module-level graph for LangGraph Studio
def get_workflow_graph():
    """Get the workflow graph for LangGraph Studio."""
    return create_workflow_graph()
