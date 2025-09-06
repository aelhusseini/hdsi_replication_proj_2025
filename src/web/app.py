"""
Interactive Learning Web Application for LangGraph and Knowledge Graphs

This Streamlit application provides an educational interface for learning:
- LangGraph workflow concepts through biomedical AI applications
- Knowledge graph fundamentals with real biomedical data
- Cypher query construction and optimization
- AI integration patterns with graph databases

Educational Features:
- Interactive workflow agent demonstration
- Progressive learning exercises from beginner to advanced
- Real-time query testing and visualization
- Step-by-step workflow transparency
- Hands-on practice with biomedical knowledge graphs

The application uses only the WorkflowAgent for educational clarity,
demonstrating core LangGraph concepts without production complexity.
"""

import os
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

# Add src directory to path for imports
src_dir = Path(__file__).parent.parent
sys.path.append(str(src_dir))

from agents.graph_interface import GraphInterface  # noqa: E402
from agents.workflow_agent import WorkflowAgent  # noqa: E402

# Load environment variables and configure page
load_dotenv()
st.set_page_config(page_title="Helix Navigator", page_icon="🔬", layout="wide")

# Constants
EXAMPLE_QUESTIONS = [
    "Which drugs have high efficacy for treating diseases?",
    "Which approved drugs treat cardiovascular diseases?",
    "Which genes encode proteins that are biomarkers for diseases?",
    "What drugs target proteins with high confidence disease associations?",
    "Which approved drugs target specific proteins?",
    "Which genes are linked to multiple disease categories?",
    "What proteins have causal associations with diseases?",
]

QUERY_EXAMPLES = {
    "Browse gene catalog": "MATCH (g:Gene) RETURN g.gene_name, g.chromosome, g.function ORDER BY g.gene_name LIMIT 15",
    "High-efficacy treatments": (
        "MATCH (dr:Drug)-[t:TREATS]->(d:Disease) "
        "WHERE t.efficacy IN ['high', 'very_high'] "
        "RETURN dr.drug_name, d.disease_name, t.efficacy "
        "ORDER BY t.efficacy DESC, dr.drug_name LIMIT 20"
    ),
    "Multi-pathway drug discovery": (
        "MATCH (dr:Drug)-[:TARGETS]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease) "
        "WHERE dr.approval_status = 'approved' "
        "RETURN dr.drug_name, p.protein_name, d.disease_name, d.category "
        "ORDER BY d.category, dr.drug_name LIMIT 25"
    ),
    "Treatment options by disease category": (
        "MATCH (dr:Drug)-[:TREATS]->(d:Disease) "
        "RETURN d.category, count(DISTINCT dr) as available_drugs "
        "ORDER BY available_drugs DESC"
    ),
    "Biomarker discovery": (
        "MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[a:ASSOCIATED_WITH]->(d:Disease) "
        "WHERE a.association_type = 'biomarker' AND a.confidence IN ['high', 'very_high'] "
        "RETURN g.gene_name, p.protein_name, d.disease_name, d.category "
        "ORDER BY d.category, g.gene_name LIMIT 30"
    ),
    "Custom query": "",
}



@st.cache_resource
def initialize_agent():
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not password or not anthropic_key:
        st.error("Please set NEO4J_PASSWORD and ANTHROPIC_API_KEY in your .env file")
        st.stop()

    graph_interface = GraphInterface(uri, user, password)
    workflow_agent = WorkflowAgent(graph_interface, anthropic_key)

    return workflow_agent, graph_interface


def create_network_visualization(results, relationship_type):
    if not results or len(results) == 0:
        return None

    # Extract nodes and edges
    nodes = set()
    edges = []
    for result in results:
        keys = list(result.keys())
        if len(keys) >= 2:
            source, target = str(result[keys[0]]), str(result[keys[1]])
            nodes.add(source)
            nodes.add(target)
            edges.append((source, target))

    if not nodes:
        return None

    # Create simple network visualization
    import networkx as nx

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Use circular layout as fallback since spring_layout might require scipy
    try:
        pos = nx.spring_layout(G)
    except ImportError:
        # Fallback to circular layout if scipy is missing
        pos = nx.circular_layout(G)
    except Exception:
        # Ultimate fallback to random layout
        pos = nx.random_layout(G)

    # Create traces
    edge_trace = go.Scatter(
        x=sum([[pos[edge[0]][0], pos[edge[1]][0], None] for edge in G.edges()], []),
        y=sum([[pos[edge[0]][1], pos[edge[1]][1], None] for edge in G.edges()], []),
        mode="lines",
        line=dict(width=1, color="#888"),
        hoverinfo="none",
    )

    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode="markers+text",
        text=list(G.nodes()),
        textposition="top center",
        marker=dict(size=15, color="lightblue"),
    )

    return go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode="closest",
            margin=dict(b=0, l=0, r=0, t=40),
            title=f"{relationship_type} Network",
            height=400,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )


def display_learning_workflow_steps():
    st.subheader("LangGraph Workflows")
    st.markdown("""
    LangGraph builds **multi-step AI agents** that follow structured workflows. Instead of one-shot responses, 
    agents maintain state and work through problems step by step.
    """)

    st.markdown("**Key Benefits:**")
    st.markdown("• Each step builds on the previous one's output")
    st.markdown("• Transparent - you can see the agent's reasoning process")
    st.markdown("• Reliable - structured approach reduces errors")
    
    st.markdown("---")
    
    st.markdown("**Our Agent's 5-Step Process:**")

    steps = [
        ("1. Classify", "Determine what type of question this is"),
        ("2. Extract", "Find key terms like gene names or diseases"),
        ("3. Generate", "Build a database query based on the question"),
        ("4. Execute", "Run the query and get results"),
        ("5. Format", "Turn database results into a readable answer"),
    ]

    for step_name, description in steps:
        st.markdown(f"**{step_name}**: {description}")

    st.markdown("---")
    st.markdown("**Question Classification Types:**")
    st.markdown("The agent can identify and handle these types of biomedical questions:")
    
    question_types = [
        ("gene_disease", "Questions about genes and diseases", "Which genes are linked to heart disease?"),
        ("drug_treatment", "Questions about drugs and treatments", "What drugs treat hypertension?"),
        ("protein_function", "Questions about proteins and functions", "What proteins does TP53 encode?"),
        ("general_db", "Database exploration queries", "Show me all available genes"),
        ("general_knowledge", "Biomedical concept questions", "What is hypertension?"),
    ]
    
    for qtype, description, example in question_types:
        st.markdown(f"• **{qtype}**: {description}")
        st.markdown(f"  *Example: \"{example}\"*")

    st.info("Each step updates the shared state, allowing complex reasoning chains.")


def display_knowledge_graph_concepts():
    st.subheader("Knowledge Graph Fundamentals")
    st.markdown("""
    Knowledge graphs store information as connected networks of **nodes** (entities) and **relationships** (edges). 
    Think of it like a social network, but for data - everything is connected to everything else.
    """)

    st.markdown("**Why Use Knowledge Graphs?**")
    st.markdown("• Find complex patterns across connected data")
    st.markdown("• Naturally represent real-world relationships")
    st.markdown("• Query using graph languages like Cypher")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Entities (Nodes):**")
        entities = [
            "**Genes** (TP53, BRCA1, MYC)",
            "**Proteins** (TP53, BRCA1, MYC_iso1)", 
            "**Diseases** (Hypertension, Heart_Failure)",
            "**Drugs** (Lisinopril, Metoprolol)",
        ]
        for entity in entities:
            st.markdown(f"• {entity}")
    
    with col2:
        st.markdown("**Relationships (Edges):**")
        relationships = [
            "**ENCODES** - Gene → Protein",
            "**LINKED_TO** - Gene → Disease",
            "**TREATS** - Drug → Disease", 
            "**TARGETS** - Drug → Protein",
            "**ASSOCIATED_WITH** - Protein → Disease"
        ]
        for rel in relationships:
            st.markdown(f"• {rel}")
    
    st.info("Each relationship can have properties like confidence scores or efficacy ratings.")


def main_interface(workflow_agent, graph_interface):
    tab1, tab2, tab3 = st.tabs(["Concepts", "Try the Agent", "Explore Queries"])

    with tab1:
        st.header("Learn the Fundamentals")
        st.markdown("Master the core concepts behind knowledge graphs and AI workflows")

        concept_choice = st.selectbox(
            "Choose a concept to explore:",
            [
                "Knowledge Graphs",
                "LangGraph Workflows",
                "Cypher Queries",
            ],
        )

        if concept_choice == "Knowledge Graphs":
            display_knowledge_graph_concepts()

            # Schema exploration
            if st.button("Explore Our Database Schema"):
                schema = graph_interface.get_schema_info()
                st.json(schema)

        elif concept_choice == "LangGraph Workflows":
            display_learning_workflow_steps()

        elif concept_choice == "Cypher Queries":
            st.markdown("### Cypher Query Language")
            st.markdown("Cypher is a query language for graph databases.")

            st.markdown("**Basic Pattern:**")
            st.code(
                "MATCH (pattern) WHERE (conditions) RETURN (results)", language="cypher"
            )

            st.markdown("**Examples:**")
            examples = [
                "MATCH (g:Gene) RETURN g.gene_name LIMIT 5",
                "MATCH (g:Gene)-[:ENCODES]->(p:Protein) RETURN g.gene_name, p.protein_name LIMIT 5",
                "MATCH (dr:Drug)-[:TREATS]->(d:Disease) WHERE toLower(d.disease_name) CONTAINS 'diabetes' RETURN dr.drug_name",
            ]
            for example in examples:
                st.code(example, language="cypher")


    with tab2:
        st.header("Try the Workflow Agent")
        st.markdown("Ask questions and see how the LangGraph workflow processes them step by step")

        st.markdown("**Try these example questions:**")
        selected_example = st.selectbox("Choose an example:", [""] + EXAMPLE_QUESTIONS)

        question_input = st.text_input(
            "Your question:",
            value=selected_example if selected_example else "",
            placeholder="Ask about genes, proteins, diseases, or drugs...",
        )

        if st.button("Run Workflow Agent", type="primary"):
            if question_input:
                with st.spinner("Running agent workflow..."):
                    result = workflow_agent.answer_question(question_input)

                st.success("Workflow Complete!")

                # Display detailed results for learning
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Workflow Results")
                    st.write(f"**Question Type:** {result['question_type']}")
                    st.write(f"**Entities Found:** {result['entities']}")
                    st.write(f"**Results Count:** {result['results_count']}")

                with col2:
                    st.subheader("Generated Query")
                    if result["cypher_query"]:
                        st.code(result["cypher_query"], language="cypher")

                st.subheader("Final Answer")
                st.info(result["answer"])

                # Show raw results
                if result.get("raw_results"):
                    with st.expander("View Raw Database Results (First 3)"):
                        st.json(result["raw_results"])
            else:
                st.warning("Please enter a question!")

    with tab3:
        st.header("Explore Database Queries")
        st.markdown("Try writing your own Cypher queries and see the results")

        selected_query = st.selectbox(
            "Choose a query to try:", list(QUERY_EXAMPLES.keys())
        )

        query_text = st.text_area(
            "Cypher Query:",
            value=QUERY_EXAMPLES[selected_query],
            height=100,
        )

        if st.button("Execute Query"):
            if query_text.strip():
                try:
                    with st.spinner("Executing query..."):
                        results = graph_interface.execute_query(query_text)

                    st.success(
                        f"Query executed successfully! Found {len(results)} results."
                    )

                    if results:
                        df = pd.DataFrame(results)
                        st.dataframe(df, width='stretch')

                        # Network visualization
                        if len(df.columns) >= 2:
                            try:
                                fig = create_network_visualization(
                                    results, "Query Results"
                                )
                                if fig:
                                    st.plotly_chart(fig, width='stretch')
                            except ImportError as e:
                                st.info(
                                    f"Network visualization unavailable (missing dependency: {e})"
                                )
                            except Exception as e:
                                st.info(f"Network visualization unavailable: {str(e)}")
                    else:
                        st.info("No results found.")

                except Exception as e:
                    st.error(f"Query error: {str(e)}")
                    st.info("Try checking your syntax or using simpler patterns!")
            else:
                st.warning("Please enter a query!")


def main():
    # Initialize agents
    workflow_agent, graph_interface = initialize_agent()

    # Header
    st.title("Helix Navigator")
    st.markdown("Interactive biomedical AI discovery platform powered by LangGraph & knowledge graphs")

    # Main interface
    main_interface(workflow_agent, graph_interface)


if __name__ == "__main__":
    main()
