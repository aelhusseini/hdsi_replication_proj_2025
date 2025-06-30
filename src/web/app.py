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
    page_title="Life Sciences Knowledge Graph Agent",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for crisp, modern UI
st.markdown(
    """
<style>
    /* Global styling */
    .main {
        padding-top: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Typography improvements */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
    }
    
    .stMarkdown h1 {
        font-size: 2.5rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    .stMarkdown h2 {
        font-size: 1.75rem;
        color: #374151;
    }
    
    .stMarkdown h3 {
        font-size: 1.25rem;
        color: #4b5563;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f9fafb;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e5e7eb;
        border-bottom: none;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: #6b7280;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #3b82f6;
        border-color: #3b82f6;
    }
    
    /* Card-like containers */
    .query-result, .stExpander {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    
    /* Text input styling */
    .stTextInput > div > div {
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    
    .stTextArea > div > div {
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    
    /* Info/Success/Warning boxes */
    .stInfo {
        background-color: #eff6ff;
        border: 1px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stSuccess {
        background-color: #f0fdf4;
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stWarning {
        background-color: #fffbeb;
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background-color: #fef2f2;
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        
        .stColumns > div {
            padding: 0 0.25rem;
        }
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
    
    # Tabs for different learning activities with improved spacing
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📚 Concepts", "🧪 Try the Agent", "🔍 Explore Queries", "🏋️ Exercises"]
    )

    with tab1:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                        padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                        border: 1px solid #93c5fd;">
                <h2 style="margin: 0 0 0.5rem 0; color: #1e40af; text-align: center;">
                    📚 Learn the Fundamentals
                </h2>
                <p style="margin: 0; text-align: center; color: #3730a3;">
                    Master the core concepts behind knowledge graphs and AI workflows
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        concept_choice = st.selectbox(
            "🎯 Choose a concept to explore:",
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
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                        padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                        border: 1px solid #86efac;">
                <h2 style="margin: 0 0 0.5rem 0; color: #15803d; text-align: center;">
                    🧪 Try the Workflow Agent
                </h2>
                <p style="margin: 0; text-align: center; color: #166534;">
                    Ask questions and see how our LangGraph workflow processes them step by step
                </p>
            </div>
            """,
            unsafe_allow_html=True,
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
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%); 
                        padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                        border: 1px solid #fcd34d;">
                <h2 style="margin: 0 0 0.5rem 0; color: #d97706; text-align: center;">
                    🔍 Explore Database Queries
                </h2>
                <p style="margin: 0; text-align: center; color: #92400e;">
                    Try writing your own Cypher queries and see the results instantly
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%); 
                        padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                        border: 1px solid #f9a8d4;">
                <h2 style="margin: 0 0 0.5rem 0; color: #be185d; text-align: center;">
                    🏋️ Learning Exercises
                </h2>
                <p style="margin: 0; text-align: center; color: #9d174d;">
                    Practice your skills with progressively challenging exercises
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

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

    # Header with improved spacing
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem; color: #1f2937;">
                🧬 Life Sciences Knowledge Graph Agent
            </h1>
            <p style="font-size: 1.2rem; color: #6b7280; margin-top: 0;">
                Learn LangGraph and Knowledge Graphs through biomedical AI applications
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar with improved styling
    with st.sidebar:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; margin: -1rem -1rem 1.5rem -1rem; 
                        border-radius: 0 0 12px 12px;">
                <h3 style="color: white; margin: 0; text-align: center;">
                    📚 Learning Resources
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown(
            """
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        border: 1px solid #e5e7eb; margin-bottom: 1rem;">
                <p style="margin: 0 0 1rem 0; font-weight: 500; color: #374151;">
                    📚 <strong>Tutorial Notebook</strong>
                </p>
                <p style="margin: 0; font-size: 0.9rem; color: #6b7280;">
                    Check out <code>docs/tutorials/langgraph-tutorial.ipynb</code>
                </p>
            </div>
            
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        border: 1px solid #e5e7eb;">
                <p style="margin: 0 0 1rem 0; font-weight: 500; color: #374151;">
                    🎯 <strong>Learning Goals</strong>
                </p>
                <ul style="margin: 0; padding-left: 1.2rem; color: #6b7280; font-size: 0.9rem;">
                    <li>Understand knowledge graphs</li>
                    <li>Learn LangGraph workflows</li>
                    <li>Practice Cypher queries</li>
                    <li>Build AI applications</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Display schema info with improved styling
        if st.checkbox("🔍 Show Database Schema"):
            schema = graph_interface.get_schema_info()
            
            st.markdown(
                """
                <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                            border: 1px solid #e5e7eb; margin-top: 1rem;">
                """,
                unsafe_allow_html=True,
            )
            
            st.markdown("**🏷️ Node Types**")
            st.json(schema["node_labels"])
            
            st.markdown("**🔗 Relationship Types**")
            st.json(schema["relationship_types"])
            
            st.markdown("</div>", unsafe_allow_html=True)

    # Main content area - Interactive learning interface
    main_interface(workflow_agent, graph_interface)

    # Application Footer with improved styling
    st.markdown(
        """
        <div style="margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                    border-radius: 12px; text-align: center; border: 1px solid #e5e7eb;">
            <p style="margin: 0; color: #64748b; font-size: 0.9rem; font-weight: 500;">
                🚀 Built with <strong>Streamlit</strong>, <strong>LangGraph</strong>, 
                <strong>Neo4j</strong>, and <strong>Anthropic Claude</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
