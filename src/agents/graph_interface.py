"""Neo4j Graph Database Interface

Simplified wrapper for Neo4j interactions with built-in security and error handling.
"""

import logging
from typing import Any, Dict, List, Optional, cast

from neo4j import GraphDatabase, Query

# Configure logging for database operations
logger = logging.getLogger(__name__)


class GraphInterface:
    """Thread-safe Neo4j database wrapper with security and error handling."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info("Connected to Neo4j database")

    def close(self):
        """Close database connection."""
        self.driver.close()

    def execute_query(
        self, cypher_query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute parameterized Cypher query and return results as dictionaries."""
        try:
            with self.driver.session() as session:
                result = session.run(cast(Query, cypher_query), parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise

    def get_schema_info(self) -> Dict[str, Any]:
        """Get database schema: node labels, relationship types, and properties."""
        with self.driver.session() as session:
            # Get node labels and relationship types
            labels_result = session.run(
                cast(
                    Query,
                    "CALL db.labels() YIELD label RETURN collect(label) as labels",
                )
            ).single()
            rel_types_result = session.run(
                cast(
                    Query,
                    "CALL db.relationshipTypes() YIELD relationshipType RETURN collect(relationshipType) as types",
                )
            ).single()

            labels = labels_result["labels"] if labels_result else []
            rel_types = rel_types_result["types"] if rel_types_result else []

            # Get properties for each node type
            node_properties = {}
            for label in labels:
                query = f"MATCH (n:{label}) RETURN keys(n) as props LIMIT 1"
                result = session.run(cast(Query, query)).single()
                if result:
                    node_properties[label] = result["props"]

            # Get properties for each relationship type
            rel_properties = {}
            for rel_type in rel_types:
                query = f"MATCH ()-[r:{rel_type}]->() RETURN keys(r) as props LIMIT 1"
                result = session.run(cast(Query, query)).single()
                if result:
                    rel_properties[rel_type] = result["props"]

            return {
                "node_labels": labels,
                "relationship_types": rel_types,
                "node_properties": node_properties,
                "relationship_properties": rel_properties,
            }

    def get_property_values(self, label: str, property_name: str) -> List[str]:
        """Get distinct values for a property across nodes/relationships."""
        try:
            query = f"MATCH (n:{label}) RETURN DISTINCT n.{property_name} as value LIMIT 20"
            if label.startswith("REL_"):  # Handle relationships
                rel_type = label.replace("REL_", "")
                query = f"MATCH ()-[r:{rel_type}]->() RETURN DISTINCT r.{property_name} as value LIMIT 20"
            
            with self.driver.session() as session:
                result = session.run(cast(Query, query))
                return [record["value"] for record in result if record["value"] is not None]
        except Exception:
            return []

    def validate_query(self, cypher_query: str) -> bool:
        """Validate Cypher query syntax using EXPLAIN without execution."""
        try:
            with self.driver.session() as session:
                session.run(cast(Query, f"EXPLAIN {cypher_query}"))
                return True
        except Exception:
            return False
