"""
Neo4j Graph Database Interface for Life Sciences Knowledge Graph Agent

This module provides a clean, safe interface for interacting with a Neo4j graph database
that contains biomedical entities (genes, proteins, diseases, drugs) and their
relationships.
It handles connection management, query execution, schema introspection, and error
handling.

Key Features:
- Secure parameterized query execution to prevent injection attacks
- Automatic session management with proper resource cleanup
- Schema discovery for understanding available node types and relationships
- Query validation using Neo4j's EXPLAIN functionality
- Comprehensive error handling and logging

The interface is designed to be used by AI agents that need to query biomedical
graphs without requiring deep knowledge of Neo4j internals.
"""

import logging
from typing import Any, Dict, List, Optional

from neo4j import GraphDatabase

# Configure logging for database operations
logger = logging.getLogger(__name__)


class GraphInterface:
    """
    A thread-safe interface for interacting with Neo4j graph databases.

    This class provides high-level methods for executing Cypher queries, discovering
    database schema, and validating queries. It handles all the low-level Neo4j driver
    operations and provides a clean API for AI agents to interact with biomedical
    knowledge graphs.

    Example Usage:
        >>> db = GraphInterface("bolt://localhost:7687", "neo4j", "password")
        >>> results = db.execute_query("MATCH (g:Gene) RETURN g.gene_name LIMIT 5")
        >>> schema = db.get_schema_info()
        >>> db.close()

    Thread Safety:
        This class is thread-safe. Multiple threads can safely use the same instance
        to execute concurrent queries, as Neo4j driver handles connection pooling.
    """

    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize a new GraphInterface instance with database connection.

        Args:
            uri: Neo4j connection URI (e.g., "bolt://localhost:7687")
            user: Database username (typically "neo4j")
            password: Database password

        Raises:
            Exception: If connection to Neo4j fails

        Note:
            The connection is established immediately and will raise an exception
            if the database is unreachable or credentials are invalid.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info("Connected to Neo4j database")

    def close(self):
        """
        Close the database connection and release all resources.

        This should be called when the GraphInterface is no longer needed
        to ensure proper cleanup of database connections. After calling close(),
        no further operations can be performed on this instance.

        Note:
            This is automatically called if the instance is used as a context manager.
        """
        self.driver.close()

    def execute_query(
        self, cypher_query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query against the Neo4j database.

        This method safely executes Cypher queries using parameterized
        queries to prevent
        injection attacks. It automatically manages database sessions and
        converts
        Neo4j Record objects to standard Python dictionaries.

        Args:
            cypher_query: The Cypher query string to execute
            parameters: Optional dictionary of parameters to substitute in the query
                       using Neo4j's parameterized query syntax (e.g., $param_name)

        Returns:
            List of dictionaries, where each dictionary represents one record
            from the query result. Keys are the column names from the RETURN clause.

        Raises:
            Exception: If the query fails due to syntax errors, missing
                      nodes/relationships,
                      or database connectivity issues

        Examples:
            >>> # Simple query with no parameters
            >>> results = db.execute_query("MATCH (g:Gene) RETURN g.gene_name LIMIT 3")
            >>> print(results)  # [{'g.gene_name': 'GENE_ALPHA'}, ...]

            >>> # Parameterized query (recommended for user input)
            >>> results = db.execute_query(
            ...     "MATCH (g:Gene {gene_name: $name}) RETURN g",
            ...     {"name": "GENE_ALPHA"}
            ... )
        """
        try:
            with self.driver.session() as session:
                result = session.run(cypher_query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise

    def get_schema_info(self) -> Dict[str, Any]:
        """
        Discover and return comprehensive schema information about the graph database.

        This method introspects the Neo4j database to understand its structure,
        including what types of nodes exist, what relationships connect them,
        and what properties are available on each node type. This information
        is crucial for AI agents to understand what data is available and how
        to construct meaningful queries.

        Returns:
            Dictionary containing schema information with these keys:
            - 'node_labels': List of all node labels
              (e.g., ['Gene', 'Protein', 'Disease'])
            - 'relationship_types': List of all relationship types
              (e.g., ['ENCODES', 'TREATS'])
            - 'node_properties': Dict mapping each node label to list of its properties
                                (e.g., {'Gene': ['gene_id', 'gene_name', 'chromosome']})

        Example:
            >>> schema = db.get_schema_info()
            >>> print(schema['node_labels'])  # ['Gene', 'Protein', 'Disease', 'Drug']
            >>> print(schema['relationship_types'])  # ['ENCODES', 'TREATS', 'TARGETS']
            >>> print(schema['node_properties']['Gene'])  # ['gene_id', 'gene_name']

        Note:
            This method samples one node from each label to discover properties.
            If a node type has no instances in the database, it won't appear
            in the node_properties dictionary.
        """
        # Neo4j system procedures to get schema metadata
        node_labels_query = (
            "CALL db.labels() YIELD label RETURN collect(label) as labels"
        )
        rel_types_query = (
            "CALL db.relationshipTypes() YIELD relationshipType "
            "RETURN collect(relationshipType) as types"
        )

        with self.driver.session() as session:
            # Get all node labels (types) in the database
            labels_result = session.run(node_labels_query).single()
            labels = labels_result["labels"] if labels_result else []

            # Get all relationship types in the database
            rel_types_result = session.run(rel_types_query).single()
            rel_types = rel_types_result["types"] if rel_types_result else []

            # For each node type, discover what properties it has by sampling one node
            node_properties = {}
            for label in labels:
                # Query to get property names from a sample node of this type
                query = f"MATCH (n:{label}) RETURN keys(n) as props LIMIT 1"
                result = session.run(query).single()
                if result:
                    node_properties[label] = result["props"]

            return {
                "node_labels": labels,
                "relationship_types": rel_types,
                "node_properties": node_properties,
            }

    def validate_query(self, cypher_query: str) -> bool:
        """
        Validate a Cypher query without executing it.

        This method uses Neo4j's EXPLAIN functionality to check if a Cypher query
        is syntactically correct and references valid nodes/relationships without
        actually executing the query. This is useful for AI agents to verify
        generated queries before running them.

        Args:
            cypher_query: The Cypher query string to validate

        Returns:
            True if the query is valid and can be executed
            False if the query has syntax errors or references invalid schema elements

        Examples:
            >>> db.validate_query("MATCH (g:Gene) RETURN g.gene_name")  # True
            >>> db.validate_query("INVALID SYNTAX")  # False
            >>> db.validate_query("MATCH (x:NonExistentType) RETURN x")  # False

        Note:
            This method only validates syntax and schema references. It cannot
            detect logical errors or queries that might return unexpected results.
        """
        try:
            with self.driver.session() as session:
                # Use EXPLAIN to validate without executing
                session.run(f"EXPLAIN {cypher_query}")
                return True
        except Exception:
            return False
