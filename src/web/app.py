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

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Helix Navigator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    .main {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        font-weight: 500;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 500;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)


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

    # Create nodes and edges based on result structure
    nodes = set()
    edges = []

    for result in results:
        keys = list(result.keys())
        if len(keys) >= 2:
            source = str(result[keys[0]])
            target = str(result[keys[1]])
            nodes.add(source)
            nodes.add(target)
            edges.append((source, target))

    if not nodes:
        return None

    # Create plotly figure
    import networkx as nx

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    pos = nx.spring_layout(G)

    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                line=dict(width=2, color="#888"),
                hoverinfo="none",
            )
        )

    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode="markers+text",
        text=[node for node in G.nodes()],
        textposition="top center",
        marker=dict(size=20, color="lightblue", line=dict(width=2, color="darkblue")),
    )

    fig = go.Figure(data=edge_trace + [node_trace])
    fig.update_layout(
        showlegend=False,
        hovermode="closest",
        margin=dict(b=0, l=0, r=0, t=40),
        title=f"{relationship_type} Network",
        height=500,
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)

    return fig


def display_learning_workflow_steps():
    st.markdown(
        """
    ### Understanding the LangGraph Workflow

    Our agent follows these steps to answer your questions:
    """
    )

    steps = [
        (
            "**1. Classify**",
            "Determine what type of biomedical question this is "
            "(gene-disease, drug-treatment, etc.)",
        ),
        (
            "**2. Extract**",
            "Find important biomedical terms like gene names, diseases, and drugs",
        ),
        ("**3. Generate**", "Create a Cypher database query to find the answer"),
        ("**4. Execute**", "Run the query against our knowledge graph"),
        ("**5. Format**", "Convert results into a human-readable answer"),
    ]

    for step_name, description in steps:
        st.markdown(f"{step_name}: {description}")

    st.info(
        "**Key Learning Point**: Each step reads the current state, "
        "does its work, and updates the state for the next step. "
        "This is the core concept of LangGraph!"
    )


def display_knowledge_graph_concepts():
    st.markdown(
        """
    ### Knowledge Graph Fundamentals

    **What is a Knowledge Graph?**
    A knowledge graph represents information as nodes (entities) and relationships (edges).

    **Our Biomedical Graph:**
    - **Genes**: Genetic sequences (e.g., TP53, BRCA1)
    - **Proteins**: Encoded by genes (e.g., TP53_protein)
    - **Diseases**: Medical conditions (e.g., diabetes, hypertension)
    - **Drugs**: Medications (e.g., Lisinopril, Metformin)

    **Relationships:**
    - Gene `--[ENCODES]-->` Protein
    - Gene `--[LINKED_TO]-->` Disease
    - Protein `--[ASSOCIATED_WITH]-->` Disease
    - Drug `--[TREATS]-->` Disease
    - Drug `--[TARGETS]-->` Protein
    """
    )


def main_interface(workflow_agent, graph_interface):

    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Concepts", "Try the Agent", "Explore Queries"])

    with tab1:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                        padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                        border: 1px solid #93c5fd;">
                <h2 style="margin: 0 0 0.5rem 0; color: #1e40af; text-align: center;">
                    Learn the Fundamentals
                </h2>
                <p style="margin: 0; text-align: center; color: #3730a3;">
                    Master the core concepts behind knowledge graphs and AI workflows
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        concept_choice = st.selectbox(
            "Choose a concept to explore:",
            [
                "Knowledge Graphs",
                "LangGraph Workflows",
                "Cypher Queries",
                "Biomedical Applications",
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
            st.markdown(
                """
            ### Cypher Query Language

            Cypher is Neo4j's query language for graphs. Think of it like SQL for graphs!

            **Basic Pattern:**
            ```cypher
            MATCH (pattern)
            WHERE (conditions)
            RETURN (what you want)
            ```

            **Examples:**
            ```cypher
            // Find all genes
            MATCH (g:Gene) RETURN g.gene_name LIMIT 5

            // Find gene-protein relationships
            MATCH (g:Gene)-[:ENCODES]->(p:Protein)
            RETURN g.gene_name, p.protein_name LIMIT 5

            // Find drugs that treat diabetes
            MATCH (dr:Drug)-[:TREATS]->(d:Disease)
            WHERE toLower(d.disease_name) CONTAINS 'diabetes'
            RETURN dr.drug_name, d.disease_name
            ```
            """
            )

        elif concept_choice == "Biomedical Applications":
            st.markdown(
                """
            ### Real-World Applications

            **Drug Discovery:**
            - Find new drug targets
            - Predict drug side effects
            - Repurpose existing drugs

            **Personalized Medicine:**
            - Match patients to treatments based on genetics
            - Predict disease risk
            - Optimize treatment plans

            **Research Acceleration:**
            - Literature mining and synthesis
            - Hypothesis generation
            - Cross-domain connections
            """
            )

    with tab2:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                        padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                        border: 1px solid #86efac;">
                <h2 style="margin: 0 0 0.5rem 0; color: #15803d; text-align: center;">
                    Try the Workflow Agent
                </h2>
                <p style="margin: 0; text-align: center; color: #166534;">
                    Ask questions and see how our LangGraph workflow processes them step by step
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Example questions
        example_questions = [
            "What protein does TP53 encode?",
            "What diseases is BRCA1 linked to?",
            "What drugs treat hypertension?",
            "What drugs treat Alzheimer_Disease?",
            "What genes are associated with diabetes?",
            "What genes are linked to both diabetes and hypertension?",
            "Which genes are linked to neurological disorders?",
            "What proteins are associated with cancer?",
        ]

        st.markdown("**Try these example questions:**")
        selected_example = st.selectbox("Choose an example:", [""] + example_questions)

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
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%); 
                        padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                        border: 1px solid #fcd34d;">
                <h2 style="margin: 0 0 0.5rem 0; color: #d97706; text-align: center;">
                    Explore Database Queries
                </h2>
                <p style="margin: 0; text-align: center; color: #92400e;">
                    Try writing your own Cypher queries and see the results instantly
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Example queries
        query_examples = {
            "Simple: All genes": "MATCH (g:Gene) RETURN g.gene_name LIMIT 5",
            "Relationships: Gene encodes protein": (
                "MATCH (g:Gene)-[:ENCODES]->(p:Protein) "
                "RETURN g.gene_name, p.protein_name LIMIT 5"
            ),
            "Complex: Gene to disease pathway": (
                "MATCH (g:Gene)-[:ENCODES]->(p:Protein)"
                "-[:ASSOCIATED_WITH]->(d:Disease) "
                "RETURN g.gene_name, p.protein_name, d.disease_name LIMIT 5"
            ),
            "Custom query": "",
        }

        selected_query = st.selectbox(
            "Choose a query to try:", list(query_examples.keys())
        )

        query_text = st.text_area(
            "Cypher Query:",
            value=query_examples[selected_query],
            height=100,
            help="Write your Cypher query here",
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
                        st.dataframe(df, use_container_width=True)

                        # Network visualization
                        if len(df.columns) >= 2:
                            fig = create_network_visualization(results, "Query Results")
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
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
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem; color: #1f2937;">
                Helix Navigator
            </h1>
            <p style="font-size: 1.2rem; color: #6b7280; margin-top: 0;">
                Learn LangGraph and Knowledge Graphs through biomedical AI applications
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Main interface
    main_interface(workflow_agent, graph_interface)

    # Footer
    st.markdown(
        """
        <div style="margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                    border-radius: 12px; text-align: center; border: 1px solid #e5e7eb;">
            <p style="margin: 0; color: #64748b; font-size: 0.9rem; font-weight: 500;">
                Built with <strong>Streamlit</strong>, <strong>LangGraph</strong>, and
                <strong>Neo4j</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
