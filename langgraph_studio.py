"""
LangGraph Studio Integration for Helix Navigator

This module provides the graph factory function specifically for LangGraph Studio
visualization and debugging. It creates an instance of the educational biomedical
workflow agent that can be visualized and interacted with in LangGraph Studio.

Purpose:
- Enable visual debugging of the 5-step biomedical workflow
- Provide interactive testing interface for educational purposes
- Support step-by-step execution tracing for learning

The graph created here is identical to the one used in the Streamlit web app,
ensuring consistency between the educational interface and debugging tools.
"""

import os
from dotenv import load_dotenv
from src.agents.workflow_agent import WorkflowAgent
from src.agents.graph_interface import GraphInterface

# Load environment variables
load_dotenv()

def create_graph():
    """
    Create and return the workflow graph for LangGraph Studio.
    
    This function sets up the biomedical knowledge graph agent
    and returns the compiled LangGraph workflow.
    """
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

# Create the graph instance
graph = create_graph()