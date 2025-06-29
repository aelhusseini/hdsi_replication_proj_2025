"""
🎓 ACTIVE AGENT: LangGraph Agent for Learning Biomedical Knowledge Graphs

✅ This is the primary agent used in the web application!

This simplified agent is designed specifically for users to learn:
1. LangGraph workflow concepts
2. Knowledge graph querying patterns
3. AI integration with graph databases

Key Learning Objectives:
- Understand state flow in LangGraph
- Learn biomedical relationship patterns
- See how natural language converts to graph queries
- Experience multi-step AI reasoning
"""

import json
from typing import Any, Dict, List, Optional, TypedDict

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
    A simplified LangGraph agent for biomedical knowledge graphs.

    This agent demonstrates the core LangGraph pattern:
    Input → Process → Generate → Execute → Format → Output

    Perfect for understanding:
    - How LangGraph manages workflow state
    - How AI agents break down complex tasks
    - How knowledge graphs answer domain questions
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
        Create our LangGraph workflow.

        This is where we define the steps and how they connect.
        Think of it as building a flowchart for problem-solving.
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
            model="claude-3-haiku-20240307",  # Fast model for simple tasks
            max_tokens=20,
            messages=[{"role": "user", "content": prompt}],
        )

        # Extract the response and update our state
        content = response.content[0]
        question_type = (
            content.text.strip() if hasattr(content, 'text') else str(content)
        )
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
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            # Try to parse the list from Claude's response
            content = response.content[0]
            response_text = (
                content.text.strip() if hasattr(content, 'text') else str(content)
            )
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
            model="claude-3-sonnet-20240229",  # More powerful model
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )

        # Clean up the query (remove code block formatting if present)
        content = response.content[0]
        cypher_query = (
            content.text.strip() if hasattr(content, 'text') else str(content)
        )
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
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.content[0]
        state["final_answer"] = (
            content.text.strip() if hasattr(content, 'text') else str(content)
        )
        print("✅ Generated final answer")
        return state

    def answer_question(self, question: str) -> Dict[str, Any]:
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
