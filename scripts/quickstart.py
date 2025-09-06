#!/usr/bin/env python3
"""
Helix Navigator - Quick Start Verification Script

This script verifies that the biomedical knowledge graph system is properly
configured and functional. It performs comprehensive setup checks, database
connectivity testing, and demonstrates core functionality through sample queries.

The script validates:
- Environment variable configuration
- Neo4j database connection and data availability
- Basic query execution through the GraphInterface
- System readiness for interactive use

Usage:
    python scripts/quickstart.py

Prerequisites:
    - Neo4j database running with biomedical data loaded
    - Environment variables configured in .env file
    - Required Python dependencies installed

Environment Variables Required:
    NEO4J_PASSWORD: Password for Neo4j database
    ANTHROPIC_API_KEY: API key for Anthropic Claude (for AI agent features)
    NEO4J_URI: Database URI (optional, defaults to bolt://localhost:7687)
    NEO4J_USER: Database username (optional, defaults to neo4j)
"""

import logging
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from dotenv import load_dotenv  # noqa: E402

from src.agents.graph_interface import GraphInterface  # noqa: E402

# Basic query functionality using GraphInterface

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def check_environment() -> bool:
    """
    Verify that all required environment variables are properly configured.

    This function checks for the presence of essential environment variables
    needed for the knowledge graph system to operate correctly. Missing variables
    will prevent the system from connecting to external services.

    Required Variables:
        NEO4J_PASSWORD: Authentication for Neo4j database access
        ANTHROPIC_API_KEY: Authentication for AI-powered query processing

    Optional Variables (with defaults):
        NEO4J_URI: Database connection URI (defaults to bolt://localhost:7687)
        NEO4J_USER: Database username (defaults to neo4j)

    Returns:
        True if all required environment variables are set
        False if any required variables are missing

    Note:
        Logs detailed error messages for missing variables to help with
        troubleshooting configuration issues.
    """
    required_vars = ["NEO4J_PASSWORD", "ANTHROPIC_API_KEY"]
    missing = []

    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        logger.error(f"Missing environment variables: {', '.join(missing)}")
        logger.error("Please set them in your .env file")
        return False

    logger.info("✓ Environment variables configured")
    return True


def test_neo4j_connection() -> bool:
    """
    Test Neo4j database connectivity and verify data availability.

    This function establishes a connection to the Neo4j database and performs
    a basic query to verify both connectivity and data presence. The test helps
    identify common setup issues before attempting complex operations.

    Connection Test:
        1. Establishes database connection using environment variables
        2. Executes a simple node count query
        3. Verifies that biomedical data is available
        4. Properly closes the connection

    Returns:
        True if database is accessible and contains data
        False if connection fails or no data is found

    Common Failure Causes:
        - Neo4j database not running
        - Incorrect connection credentials
        - Database is empty (data not loaded)
        - Network connectivity issues
        - Firewall blocking database port

    Note:
        If connection succeeds but no data is found, suggests running
        the data loading script to populate the database.
    """
    try:
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "")

        if not password:
            raise ValueError("NEO4J_PASSWORD environment variable is required")

        graph = GraphInterface(uri, user, password)

        # Execute basic connectivity test query
        result = graph.execute_query("MATCH (n) RETURN count(n) as count")
        count = result[0]["count"] if result else 0

        graph.close()

        if count > 0:
            logger.info(f"✓ Neo4j connected successfully ({count} nodes found)")
            return True
        else:
            logger.warning("⚠ Neo4j connected but no data found")
            logger.info("  Run 'pdm run load-data' to load the dataset")
            return False

    except Exception as e:
        logger.error(f"✗ Neo4j connection failed: {e}")
        return False


def run_sample_queries() -> bool:
    """
    Execute representative queries to demonstrate system functionality.

    This function runs a curated set of sample queries that showcase the
    different types of biomedical questions the knowledge graph can answer.
    The queries test various relationship types and demonstrate the system's
    capability to retrieve meaningful biomedical information.

    Sample Query Types:
        1. Gene-Disease Associations: "What genes are associated with diabetes?"
        2. Drug Treatments: "What drugs treat hypertension?"
        3. Gene-Protein Encoding: "What protein does gene encode?"

    Each query demonstrates:
        - Different node types (genes, proteins, diseases, drugs)
        - Various relationship types (LINKED_TO, TREATS, ENCODES)
        - Result formatting and data presentation
        - System performance with real biomedical data

    Returns:
        True if all sample queries execute successfully
        False if any query fails or system encounters errors

    Error Handling:
        Gracefully handles query failures and provides diagnostic information
        to help identify issues with data loading or system configuration.

    Note:
        Query results are limited to first few entries for readability,
        but full result counts are displayed to show data completeness.
    """
    try:
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "")

        if not password:
            raise ValueError("NEO4J_PASSWORD environment variable is required")

        graph = GraphInterface(uri, user, password)

        logger.info("\n📊 Running sample queries...\n")

        # Query 1: Gene-Disease associations (demonstrates LINKED_TO relationships)
        logger.info("Query 1: What genes are associated with diabetes?")
        query = """MATCH (g:Gene)-[:LINKED_TO]->(d:Disease)
                   WHERE toLower(d.disease_name) CONTAINS toLower('diabetes')
                   RETURN g.gene_name as gene, d.disease_name as disease LIMIT 20"""
        results = graph.execute_query(query)
        if results:
            logger.info(f"Found {len(results)} genes:")
            for r in results[:3]:  # Show first 3 results
                logger.info(f"  - {r['gene']}")
            if len(results) > 3:
                logger.info(f"  ... and {len(results) - 3} more")

        # Query 2: Drug treatments (demonstrates TREATS relationships)
        logger.info("\nQuery 2: What drugs treat hypertension?")
        query = """MATCH (dr:Drug)-[t:TREATS]->(d:Disease)
                   WHERE toLower(d.disease_name) CONTAINS toLower('hypertension')
                   RETURN dr.drug_name as drug, d.disease_name as disease, 
                          t.efficacy as efficacy ORDER BY t.efficacy DESC LIMIT 20"""
        results = graph.execute_query(query)
        if results:
            logger.info(f"Found {len(results)} drugs:")
            for r in results[:3]:  # Show first 3 results with efficacy
                efficacy = r.get("efficacy", "unknown")
                logger.info(f"  - {r['drug']} (efficacy: {efficacy})")

        # Query 3: Gene-protein encoding (demonstrates ENCODES relationships)
        logger.info("\nQuery 3: What protein does GENE_ALPHA encode?")
        query = """MATCH (g:Gene)-[:ENCODES]->(p:Protein)
                   WHERE g.gene_name = 'GENE_ALPHA'
                   RETURN g.gene_name as gene, p.protein_name as protein, 
                          p.molecular_weight as molecular_weight"""
        results = graph.execute_query(query)
        if results:
            r = results[0]
            weight = r.get("molecular_weight", "unknown")
            logger.info(f"  - {r['gene']} encodes {r['protein']} (MW: {weight})")

        graph.close()
        logger.info("\n✓ Sample queries completed successfully")
        return True

    except Exception as e:
        logger.error(f"✗ Query execution failed: {e}")
        return False


def print_next_steps():
    """
    Display guidance for next steps after successful setup verification.

    This function provides clear, actionable instructions for users to begin
    exploring the knowledge graph system. It covers both interactive web interface
    usage and direct database exploration options.

    Guidance Includes:
        - How to start the interactive Streamlit web application
        - Example questions to explore system capabilities
        - Direct database access through Neo4j browser
        - References to additional documentation

    User Journey:
        1. Verification complete (this script)
        2. Start web application for interactive queries
        3. Explore with natural language questions
        4. Optionally examine raw data in Neo4j browser
        5. Consult documentation for advanced usage
    """
    print("\n" + "=" * 50)
    print("🎉 Setup Verification Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Start the Streamlit app:")
    print("   $ pdm run app")
    print("\n2. Open your browser to:")
    print("   http://localhost:8501")
    print("\n3. Try asking questions like:")
    print("   - What genes are associated with diabetes?")
    print("   - What drugs treat hypertension?")
    print("   - What protein does GENE_ALPHA encode?")
    print("\n4. Explore the Neo4j browser:")
    print("   http://localhost:7474")
    print("\nFor more information, see docs/USER_GUIDE.md")


def main():
    """
    Main orchestration function for comprehensive setup verification.

    This function coordinates the complete verification process, ensuring that
    all system components are properly configured and functional before the
    user begins interactive exploration.

    Verification Process:
        1. Environment Configuration Check
           - Validates required environment variables
           - Ensures authentication credentials are available

        2. Database Connectivity Test
           - Verifies Neo4j database connection
           - Confirms biomedical data is loaded and accessible

        3. Functional Query Testing
           - Executes representative queries across different entity types
           - Validates system can retrieve meaningful biomedical information

        4. Success Guidance
           - Provides clear next steps for system exploration
           - Directs users to interactive interfaces and documentation

    Exit Codes:
        0: All verification steps completed successfully
        1: Critical failure in environment or database connectivity

    Note:
        Sample query failures are treated as warnings rather than fatal errors,
        as the system may still be functional for basic operations.
    """
    logger.info("🚀 Helix Navigator - Quick Start")
    logger.info("=" * 50)

    # Phase 1: Environment verification
    if not check_environment():
        sys.exit(1)

    # Phase 2: Database connectivity test
    if not test_neo4j_connection():
        sys.exit(1)

    # Phase 3: Functional verification through sample queries
    if not run_sample_queries():
        logger.warning("Sample queries failed, but setup might still work")

    # Phase 4: Success guidance
    print_next_steps()


if __name__ == "__main__":
    main()
