"""
📚 EDUCATIONAL EXAMPLE: LangGraph-Powered AI Agent for Life Sciences Knowledge Graph Queries

⚠️ NOTE: This agent is NOT used in the web application. It serves as an educational
reference to demonstrate advanced LangGraph features for students.

This module implements an intelligent agent that can understand natural language
questions about biomedical relationships and convert them into precise graph database
queries. The agent uses LangGraph for workflow orchestration and Anthropic's Claude
for natural language understanding.

The agent follows a multi-step pipeline:
1. Question Classification - Determines the type of biomedical question
2. Entity Extraction - Identifies specific genes, proteins, diseases, drugs mentioned
3. Cypher Generation - Converts the question into a Neo4j Cypher query
4. Query Execution - Runs the query safely against the graph database
5. Response Formatting - Converts results back to natural language

Key Features:
- Handles complex biomedical terminology and relationships
- Generates safe, parameterized database queries
- Provides structured error handling and recovery
- Maintains conversation state throughout the workflow
- Supports various question types (gene-disease, drug-target, pathway analysis, etc.)

Example Question Types Supported:
- "What genes are associated with diabetes?"
- "Which drugs target the protein PROT_ALPHA?"
- "Show me the pathway from GENE_BETA to available treatments"
- "What diseases is the protein encoded by GENE_GAMMA linked to?"
"""

import json
import logging
from typing import Any, Dict, List, Optional, TypedDict

from anthropic import Anthropic
from langgraph.graph import END, StateGraph

from .graph_interface import GraphInterface

# Configure logging for agent operations
logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """
    Defines the state structure that flows through the LangGraph workflow.

    This typed dictionary ensures type safety and documents the data that
    passes between different nodes in the agent workflow. Each field represents
    a piece of information that gets populated or modified as the agent processes
    a user's question.

    Fields:
        user_question: The original natural language question from the user
        question_type: Classified category (e.g., 'gene_disease', 'drug_target', 'pathway')
        entities: List of extracted biomedical entities with their types
                 (e.g., [{'type': 'gene', 'name': 'GENE_ALPHA'}, ...])
        cypher_query: The generated Neo4j Cypher query string
        query_results: Raw results from database query execution
        final_answer: The natural language response to return to the user
        error: Error message if something goes wrong during processing
    """

    user_question: str
    question_type: Optional[str]
    entities: Optional[List[Dict[str, str]]]
    cypher_query: Optional[str]
    query_results: Optional[List[Dict[str, Any]]]
    final_answer: Optional[str]
    error: Optional[str]


class LifeScienceAgent:
    """
    An intelligent agent for querying life sciences knowledge graphs using natural language.

    This agent combines the power of large language models (Claude) with graph database
    queries to answer complex questions about biomedical relationships. It uses LangGraph
    to orchestrate a multi-step workflow that ensures reliable, accurate responses.

    The agent is designed to be:
    - Robust: Handles errors gracefully and provides meaningful feedback
    - Safe: Uses parameterized queries to prevent injection attacks
    - Intelligent: Understands biomedical context and terminology
    - Extensible: Easy to add new question types and response formats

    Workflow Overview:
        User Question → Classification → Entity Extraction → Query Generation
        → Database Execution → Response Formatting → Natural Language Answer

    Example Usage:
        >>> agent = LifeScienceAgent(graph_interface, api_key)
        >>> result = agent.answer_question("What genes are linked to Alzheimer's disease?")
        >>> print(result['final_answer'])

    Supported Question Categories:
        - gene_disease: Questions about genes associated with diseases
        - protein_disease: Questions about proteins linked to diseases
        - drug_treatment: Questions about drugs that treat diseases
        - drug_target: Questions about molecular targets of drugs
        - gene_protein: Questions about genes encoding proteins
        - pathway: Complex multi-hop relationship queries
    """

    def __init__(self, graph_interface: GraphInterface, anthropic_api_key: str):
        """
        Initialize the Life Science Agent with database connection and AI capabilities.

        Args:
            graph_interface: An initialized GraphInterface for database operations
            anthropic_api_key: API key for Anthropic Claude services

        Note:
            The agent immediately retrieves schema information from the database
            and builds its workflow graph. This ensures it understands the available
            data structure before processing any queries.
        """
        self.graph_db = graph_interface
        self.anthropic = Anthropic(api_key=anthropic_api_key)
        # Get schema info to understand what data is available in the database
        self.schema_info = self.graph_db.get_schema_info()
        # Build the LangGraph workflow that defines the agent's processing pipeline
        self.workflow: Any = self._build_workflow()

    def _get_response_text(self, response: Any) -> str:
        """
        Safely extract text content from Anthropic API responses.

        Anthropic API responses can contain different types of content blocks.
        This utility method safely extracts text content while handling
        potential type variations and missing data.

        Args:
            response: Raw response object from Anthropic API

        Returns:
            The text content as a string, or empty string if not available
        """
        if response.content and len(response.content) > 0:
            content = response.content[0]
            if hasattr(content, "text"):
                return str(content.text)
        return ""

    def _build_workflow(self) -> Any:
        """
        Construct the LangGraph workflow that defines the agent's processing pipeline.

        This method creates a directed graph that represents the flow of information
        from a user's natural language question to a final answer. Each node in the
        graph represents a processing step, and edges define the order of execution.

        Workflow Steps:
            1. classify_question: Determine the type of biomedical question
            2. extract_entities: Find specific genes, proteins, diseases, drugs mentioned
            3. generate_cypher: Convert question + entities into a Neo4j query
            4. execute_query: Run the query against the database
            5. format_response: Convert results into natural language
            6. handle_error: Gracefully handle any failures (conditional)

        Returns:
            Compiled LangGraph workflow ready for execution

        Note:
            The workflow includes conditional error handling that routes to
            error handling if query execution fails, otherwise proceeds to
            normal response formatting.
        """
        workflow = StateGraph(AgentState)

        # Define processing nodes - each corresponds to a method of this class
        workflow.add_node("classify_question", self.classify_question)
        workflow.add_node("extract_entities", self.extract_entities)
        workflow.add_node("generate_cypher", self.generate_cypher_query)
        workflow.add_node("execute_query", self.execute_query)
        workflow.add_node("format_response", self.format_response)
        workflow.add_node("handle_error", self.handle_error)

        # Define the happy path flow
        workflow.add_edge("classify_question", "extract_entities")
        workflow.add_edge("extract_entities", "generate_cypher")
        workflow.add_edge("generate_cypher", "execute_query")
        workflow.add_edge("execute_query", "format_response")
        workflow.add_edge("format_response", END)

        # Define conditional error handling
        # If query execution fails, route to error handler instead of response formatter
        workflow.add_conditional_edges(
            "execute_query",
            lambda x: "handle_error" if x.get("error") else "format_response",
            {"handle_error": "handle_error", "format_response": "format_response"},
        )
        workflow.add_edge("handle_error", END)

        # Set the starting point of the workflow
        workflow.set_entry_point("classify_question")

        return workflow.compile()

    def classify_question(self, state: AgentState) -> AgentState:
        """
        Classify the user's question into a biomedical category.

        This is the first step in the agent workflow. Understanding the question type
        helps the agent choose appropriate query patterns and entity extraction strategies.
        The classification guides how the query will be constructed in later steps.

        Args:
            state: Current agent state containing the user's question

        Returns:
            Updated state with question_type field populated

        Categories:
            - gene_disease: "What genes are associated with diabetes?"
            - protein_disease: "What diseases involve protein PROT_ALPHA?"
            - drug_treatment: "What drugs treat hypertension?"
            - drug_target: "What proteins does drug X target?"
            - gene_protein: "What protein does gene Y encode?"
            - general: Fallback for other biomedical questions

        Note:
            Uses Claude Haiku for fast classification with minimal token usage.
        """
        prompt = f"""Classify this biomedical question into one of these categories:
        - gene_disease: Questions about genes and diseases
        - protein_disease: Questions about proteins and diseases
        - drug_treatment: Questions about drugs treating diseases
        - drug_target: Questions about drug targets
        - gene_protein: Questions about genes encoding proteins
        - general: Other biomedical questions

        Question: {state['user_question']}

        Respond with just the category name."""

        response = self.anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}],
        )

        state["question_type"] = self._get_response_text(response).strip() or "general"
        logger.info(f"Question classified as: {state['question_type']}")
        return state

    def extract_entities(self, state: AgentState) -> AgentState:
        """
        Extract specific biomedical entities mentioned in the user's question.

        This step identifies the concrete entities (gene names, protein names, diseases, drugs)
        that the user is asking about. These entities will be used to construct precise
        database queries that target specific nodes in the knowledge graph.

        Args:
            state: Current agent state with user question and question type

        Returns:
            Updated state with entities field containing list of found entities

        Entity Types Detected:
            - gene: Gene symbols like "GENE_ALPHA", "BRCA1", "TP53"
            - protein: Protein names like "PROT_BETA", "insulin", "hemoglobin"
            - disease: Disease names like "diabetes", "cancer", "Alzheimer"
            - drug: Drug names like "aspirin", "AlphaCure", "BetaTherapy"

        Returns:
            List of dictionaries with 'type' and 'name' keys for each entity found

        Example Output:
            [
                {"type": "gene", "name": "GENE_ALPHA"},
                {"type": "disease", "name": "diabetes"}
            ]

        Error Handling:
            If entity extraction fails, returns empty list to allow workflow to continue
            with generic query patterns.
        """
        prompt = f"""Extract biomedical entities from this question. Look for:
        - Gene names (e.g., GENE_ALPHA, GENE_BETA)
        - Protein names (e.g., PROT_ALPHA, PROT_BETA)
        - Disease names (e.g., Diabetes, Hypertension)
        - Drug names (e.g., AlphaCure, BetaTherapy)

        Question: {state['user_question']}

        Return ONLY a valid JSON array of objects with 'type' and 'name' fields.
        Example: [{{"type": "disease", "name": "Diabetes"}}]
        If no entities found, return: []"""

        response = self.anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )

        try:
            response_text = self._get_response_text(response).strip()
            # Try to extract JSON if response contains extra text
            if response_text.startswith("["):
                entities = json.loads(response_text)
            else:
                # Look for JSON array in the response
                import re

                json_match = re.search(r"\[.*\]", response_text, re.DOTALL)
                if json_match:
                    entities = json.loads(json_match.group())
                else:
                    entities = []

            state["entities"] = entities
            logger.info(f"Extracted entities: {entities}")
        except (json.JSONDecodeError, AttributeError) as e:
            state["entities"] = []
            logger.warning(f"Failed to extract entities: {e}")
            logger.debug(
                "Response: %s", self._get_response_text(response) or "No content"
            )

        return state

    def generate_cypher_query(self, state: AgentState) -> AgentState:
        """Generate a Cypher query based on the question."""
        schema_str = f"""
        Node types: {', '.join(self.schema_info['node_labels'])}
        Relationship types: {', '.join(self.schema_info['relationship_types'])}
        Node properties: {json.dumps(self.schema_info['node_properties'], indent=2)}
        """

        entities_str = (
            json.dumps(state.get("entities", []), indent=2)
            if state.get("entities")
            else "No specific entities found"
        )

        prompt = f"""Generate a Neo4j Cypher query for this biomedical question.

        Database Schema:
        {schema_str}

        Question: {state['user_question']}
        Question Type: {state.get('question_type', 'general')}
        Extracted Entities: {entities_str}

        Generate only the Cypher query, no explanation. Make sure to:
        1. Use proper node labels (Gene, Protein, Disease, Drug)
        2. Use proper relationship types:
           - Gene -[:LINKED_TO]-> Disease (for gene-disease associations)
           - Gene -[:ENCODES]-> Protein
           - Protein -[:ASSOCIATED_WITH]-> Disease
           - Drug -[:TREATS]-> Disease
           - Drug -[:TARGETS]-> Protein
        3. Use case-insensitive matching with toLower() for better results
        4. Return meaningful data with proper aliases
        5. Limit results to 20 for performance"""

        response = self.anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        cypher_query = self._get_response_text(response).strip()

        # Clean up the query
        if cypher_query.startswith("```"):
            cypher_query = cypher_query.split("```")[1]
            if cypher_query.startswith("cypher"):
                cypher_query = cypher_query[6:].strip()

        state["cypher_query"] = cypher_query
        logger.info(f"Generated Cypher query: {cypher_query}")
        return state

    def execute_query(self, state: AgentState) -> AgentState:
        """Execute the Cypher query against the database."""
        try:
            if not state.get("cypher_query"):
                raise ValueError("No Cypher query generated")

            # Validate query first
            cypher_query = state.get("cypher_query", "")
            if not cypher_query or not self.graph_db.validate_query(cypher_query):
                raise ValueError("Invalid Cypher query")

            results = self.graph_db.execute_query(cypher_query)
            state["query_results"] = results
            logger.info(f"Query returned {len(results)} results")
        except Exception as e:
            state["error"] = str(e)
            logger.error(f"Query execution error: {e}")

        return state

    def format_response(self, state: AgentState) -> AgentState:
        """Format the query results into a natural language response."""
        if not state.get("query_results"):
            state["final_answer"] = (
                "I couldn't find any information matching your question."
            )
            return state

        query_results = state.get("query_results") or []
        results_str = json.dumps(query_results[:5], indent=2)  # Show first 5 results

        prompt = f"""Convert these results into a clear natural language answer.

        Original Question: {state['user_question']}

        Query Results:
        {results_str}

        Total Results: {len(query_results)}

        Provide a concise, informative answer that directly addresses the question.
        If there are many results, summarize the key findings."""

        response = self.anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        answer = self._get_response_text(response).strip()
        state["final_answer"] = answer or "Unable to generate response."
        return state

    def handle_error(self, state: AgentState) -> AgentState:
        """
        Handle errors that occur during query processing.

        This method provides graceful error recovery when the workflow encounters
        problems like invalid queries, database connection issues, or AI service
        failures. Instead of crashing, it provides helpful feedback to the user.

        Args:
            state: Current agent state containing error information

        Returns:
            Updated state with user-friendly error message in final_answer

        Note:
            This is the error handling node in the LangGraph workflow, reached
            only when the execute_query step fails.
        """
        error_msg = state.get("error", "An unknown error occurred")
        state["final_answer"] = (
            f"I encountered an error: {error_msg}. Please try rephrasing your question."
        )
        return state

    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Main entry point for processing natural language questions about biomedical data.

        This is the public interface that external code uses to interact with the agent.
        It orchestrates the entire workflow from question to answer, handling all the
        complexity of AI reasoning, query generation, and database interaction.

        Args:
            question: Natural language question about genes, proteins, diseases, or drugs

        Returns:
            Dictionary containing:
            - answer: Natural language response to the question
            - cypher_query: The generated Neo4j query (for transparency/debugging)
            - entities: List of biomedical entities extracted from the question
            - results_count: Number of database records found
            - error: Error message if something went wrong (None if successful)

        Example Usage:
            >>> agent = LifeScienceAgent(graph_interface, api_key)
            >>> result = agent.answer_question("What genes are associated with diabetes?")
            >>> print(result['answer'])
            "Based on the knowledge graph, several genes are associated with diabetes..."
            >>> print(f"Found {result['results_count']} results")
            >>> print(f"Query used: {result['cypher_query']}")

        Workflow Steps Executed:
            1. Question classification (gene_disease, drug_target, etc.)
            2. Entity extraction (specific genes, diseases, etc. mentioned)
            3. Cypher query generation (converts to database query)
            4. Query execution (runs against Neo4j database)
            5. Response formatting (converts results to natural language)

        Error Handling:
            Returns error information in the result dictionary rather than raising
            exceptions, allowing calling code to handle issues gracefully.
        """
        initial_state = AgentState(
            user_question=question,
            question_type=None,
            entities=None,
            cypher_query=None,
            query_results=None,
            final_answer=None,
            error=None,
        )

        # Run the workflow
        final_state = self.workflow.invoke(initial_state)

        # Log the final query for debugging
        if final_state.get("cypher_query"):
            logger.info(f"Final Cypher query: {final_state.get('cypher_query')}")

        return {
            "answer": final_state.get("final_answer", "Unable to process question"),
            "cypher_query": final_state.get("cypher_query"),
            "entities": final_state.get("entities", []),
            "results_count": len(final_state.get("query_results", [])),
            "error": final_state.get("error"),
        }
