"""
Streamlit web application for Life Sciences Knowledge Graph Agent.
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
    page_title="Life Sciences Knowledge Graph Agent",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
    }
    .query-result {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def initialize_agent():
    """Initialize the workflow agent and database connection."""
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


def display_results_table(results):
    """Display results in a formatted table."""
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
        return df
    else:
        st.info("No results found.")
        return None


def create_network_visualization(results, relationship_type):
    """Create a network visualization of results."""
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
    """Display information about the LangGraph workflow steps."""
    st.markdown(
        """
    ### 🎓 Understanding the LangGraph Workflow

    Our agent follows these steps to answer your questions:
    """
    )

    steps = [
        (
            "1️⃣ **Classify**",
            "Determine what type of biomedical question this is "
            "(gene-disease, drug-treatment, etc.)",
        ),
        (
            "2️⃣ **Extract**",
            "Find important biomedical terms like gene names, diseases, and drugs",
        ),
        ("3️⃣ **Generate**", "Create a Cypher database query to find the answer"),
        ("4️⃣ **Execute**", "Run the query against our knowledge graph"),
        ("5️⃣ **Format**", "Convert results into a human-readable answer"),
    ]

    for step_name, description in steps:
        st.markdown(f"{step_name}: {description}")

    st.info(
        "💡 **Key Learning Point**: Each step reads the current state, "
        "does its work, and updates the state for the next step. "
        "This is the core concept of LangGraph!"
    )


def display_knowledge_graph_concepts():
    """Display information about knowledge graphs."""
    st.markdown(
        """
    ### 🕸️ Knowledge Graph Fundamentals

    **What is a Knowledge Graph?**
    A knowledge graph represents information as nodes (entities) and relationships
    (edges).

    **Our Biomedical Graph:**
    - 🧬 **Genes**: Genetic sequences (e.g., GENE_ALPHA)
    - 🧪 **Proteins**: Encoded by genes (e.g., PROT_BETA)
    - 🏥 **Diseases**: Medical conditions (e.g., diabetes)
    - 💊 **Drugs**: Medications (e.g., AlphaCure)

    **Relationships:**
    - Gene `--[ENCODES]-->` Protein
    - Gene `--[LINKED_TO]-->` Disease
    - Protein `--[ASSOCIATED_WITH]-->` Disease
    - Drug `--[TREATS]-->` Disease
    - Drug `--[TARGETS]-->` Protein
    """
    )


def main_interface(workflow_agent, graph_interface):
    """Main interface with interactive learning exercises."""
    st.header("🧬 Life Sciences Knowledge Graph Agent")

    # Tabs for different learning activities
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📚 Concepts", "🧪 Try the Agent", "🔍 Explore Queries", "🏋️ Exercises"]
    )

    with tab1:
        st.subheader("Learn the Fundamentals")

        concept_choice = st.selectbox(
            "Choose a concept to learn:",
            [
                "Knowledge Graphs",
                "LangGraph Workflows",
                "Cypher Queries",
                "Biomedical Applications",
            ],
        )

        if concept_choice == "Knowledge Graphs":
            display_knowledge_graph_concepts()

            # Interactive schema exploration
            if st.button("Explore Our Database Schema"):
                schema = graph_interface.get_schema_info()
                st.json(schema)

        elif concept_choice == "LangGraph Workflows":
            display_learning_workflow_steps()

        elif concept_choice == "Cypher Queries":
            st.markdown(
                """
            ### 🔧 Cypher Query Language

            Cypher is Neo4j's query language for graphs. Think of it like SQL for
            graphs!

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
            ### 🧬 Real-World Applications

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
        st.subheader("🧪 Try the Workflow Agent")
        st.markdown(
            "Ask questions and see how our LangGraph workflow processes them "
            "step by step!"
        )

        # Example questions for users
        example_questions = [
            "What genes are associated with diabetes?",
            "What drugs treat hypertension?",
            "What protein does GENE_ALPHA encode?",
            "What diseases is PROT_BETA associated with?",
            "What are the targets of AlphaCure?",
        ]

        st.markdown("**Try these example questions:**")
        selected_example = st.selectbox("Choose an example:", [""] + example_questions)

        question_input = st.text_input(
            "Your question:",
            value=selected_example if selected_example else "",
            placeholder="Ask about genes, proteins, diseases, or drugs...",
        )

        if st.button("🚀 Run Workflow Agent", type="primary"):
            if question_input:
                with st.spinner("Running agent workflow..."):
                    result = workflow_agent.answer_question(question_input)

                st.success("✅ Workflow Complete!")

                # Display detailed results for learning
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📊 Workflow Results")
                    st.write(f"**Question Type:** {result['question_type']}")
                    st.write(f"**Entities Found:** {result['entities']}")
                    st.write(f"**Results Count:** {result['results_count']}")

                with col2:
                    st.subheader("🔧 Generated Query")
                    if result["cypher_query"]:
                        st.code(result["cypher_query"], language="cypher")

                st.subheader("💬 Final Answer")
                st.info(result["answer"])

                # Show some raw results for learning
                if result.get("raw_results"):
                    with st.expander("🔍 View Raw Database Results (First 3)"):
                        st.json(result["raw_results"])
            else:
                st.warning("Please enter a question!")

    with tab3:
        st.subheader("🔍 Explore Database Queries")
        st.markdown("Try writing your own Cypher queries!")

        # Pre-built queries for learning
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

        if st.button("▶️ Execute Query"):
            if query_text.strip():
                try:
                    with st.spinner("Executing query..."):
                        results = graph_interface.execute_query(query_text)

                    st.success(
                        f"✅ Query executed successfully! Found {len(results)} results."
                    )

                    if results:
                        df = pd.DataFrame(results)
                        st.dataframe(df, use_container_width=True)

                        # Simple visualization if applicable
                        if len(df.columns) >= 2:
                            fig = create_network_visualization(results, "Query Results")
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No results found.")

                except Exception as e:
                    st.error(f"❌ Query error: {str(e)}")
                    st.info("💡 Try checking your syntax or using simpler patterns!")
            else:
                st.warning("Please enter a query!")

    with tab4:
        st.subheader("🏋️ Learning Exercises")

        exercise_choice = st.selectbox(
            "Choose an exercise:",
            [
                "Exercise 1: Basic Queries",
                "Exercise 2: Relationship Patterns",
                "Exercise 3: Complex Pathways",
            ],
        )

        if exercise_choice == "Exercise 1: Basic Queries":
            st.markdown(
                """
            ### 🎯 Exercise 1: Write Basic Queries

            **Your Task:** Write Cypher queries for these questions:

            1. Find all diseases in our database
            2. Find all drugs with their types
            3. Find proteins with molecular weight greater than 50
            """
            )

            exercise1_query = st.text_area(
                "Your answer for question 1:",
                placeholder="MATCH (d:Disease) RETURN ...",
            )

            if st.button("Check Answer 1"):
                if "MATCH (d:Disease) RETURN" in exercise1_query:
                    st.success("✅ Great! You're using the correct pattern!")
                else:
                    st.info("💡 Hint: Use MATCH (d:Disease) RETURN d.disease_name")

        elif exercise_choice == "Exercise 2: Relationship Patterns":
            st.markdown(
                """
            ### 🎯 Exercise 2: Understand Relationships

            **Your Task:** Write queries to find:

            1. All drugs that treat any disease
            2. All proteins associated with diabetes
            3. Complete pathway: Gene → Protein → Disease
            """
            )

            exercise2_query = st.text_area(
                "Your answer:", placeholder="MATCH (dr:Drug)-[:TREATS]->(d:Disease) ..."
            )

            if st.button("Try Your Query"):
                if exercise2_query.strip():
                    try:
                        results = graph_interface.execute_query(exercise2_query)
                        st.success(f"✅ Query works! Found {len(results)} results.")
                        if results:
                            st.dataframe(pd.DataFrame(results[:5]))
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info(
                            "💡 Check your relationship syntax: -[:RELATIONSHIP_NAME]->"
                        )

        elif exercise_choice == "Exercise 3: Complex Pathways":
            st.markdown(
                """
            ### 🎯 Exercise 3: Complex Pathway Analysis

            **Your Task:** Find all complete pathways from genes to treatments:
            `Gene → Protein → Disease ← Drug`

            This requires connecting 4 node types with 3 relationships!
            """
            )

            exercise3_query = st.text_area(
                "Your complex query:",
                placeholder=(
                    "MATCH (g:Gene)-[:ENCODES]->(p:Protein)"
                    "-[:ASSOCIATED_WITH]->(d:Disease)<-[:TREATS]-(dr:Drug) ..."
                ),
            )

            if st.button("Test Complex Query"):
                if exercise3_query.strip():
                    try:
                        results = graph_interface.execute_query(exercise3_query)
                        st.success(
                            f"🎉 Advanced query successful! "
                            f"Found {len(results)} complete pathways."
                        )
                        if results:
                            st.dataframe(pd.DataFrame(results[:3]))
                            # Celebration for completing advanced exercise!
                            st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info(
                            "💡 Complex queries need careful relationship chaining. "
                            "Check each step!"
                        )


def main():
    # Initialize agents
    workflow_agent, graph_interface = initialize_agent()

    # Header
    st.title("🧬 Life Sciences Knowledge Graph Agent")
    st.markdown(
        "Learn LangGraph and Knowledge Graphs through biomedical AI applications!"
    )

    # Sidebar
    with st.sidebar:
        st.subheader("Learning Resources")
        st.markdown(
            """
        📚 **Tutorial Notebook**: Check out `tutorial_langgraph_knowledge_graphs.ipynb`

        🎯 **Learning Goals**:
        - Understand knowledge graphs
        - Learn LangGraph workflows
        - Practice Cypher queries
        - Build AI applications
        """
        )

        # Display schema info
        if st.checkbox("Show Database Schema"):
            schema = graph_interface.get_schema_info()
            st.subheader("Node Types")
            st.write(schema["node_labels"])
            st.subheader("Relationship Types")
            st.write(schema["relationship_types"])

    # Main content area - Interactive learning interface
    main_interface(workflow_agent, graph_interface)

    # Application Footer and Technology Attribution
    st.divider()
    st.markdown(
        """
    <div style="text-align: center; color: #888;">
        Built with Streamlit, LangGraph, Neo4j, and Anthropic Claude
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
