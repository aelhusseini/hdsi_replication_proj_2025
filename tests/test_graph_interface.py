"""
Tests for the graph interface module.
"""

from unittest.mock import Mock, patch

from src.agents.graph_interface import GraphInterface


class TestGraphInterface:

    @patch("src.agents.graph_interface.GraphDatabase")
    def test_init(self, mock_graph_db):
        """Test GraphInterface initialization."""
        GraphInterface("bolt://localhost:7687", "neo4j", "password")
        mock_graph_db.driver.assert_called_once_with(
            "bolt://localhost:7687", auth=("neo4j", "password")
        )

    @patch("src.agents.graph_interface.GraphDatabase")
    def test_execute_query(self, mock_graph_db):
        """Test query execution."""
        # Setup mock
        mock_driver = Mock()
        mock_session = Mock()
        mock_result = Mock()
        mock_record = Mock()
        mock_record.data.return_value = {"name": "test"}
        mock_result.__iter__ = Mock(return_value=iter([mock_record]))

        mock_session_cm = Mock()
        mock_session_cm.__enter__ = Mock(return_value=mock_session)
        mock_session_cm.__exit__ = Mock(return_value=None)
        mock_driver.session.return_value = mock_session_cm
        mock_session.run.return_value = mock_result
        mock_graph_db.driver.return_value = mock_driver

        # Test
        interface = GraphInterface("bolt://localhost:7687", "neo4j", "password")
        results = interface.execute_query("MATCH (n) RETURN n LIMIT 1")

        assert results == [{"name": "test"}]
        mock_session.run.assert_called_once_with("MATCH (n) RETURN n LIMIT 1", {})

    @patch("src.agents.graph_interface.GraphDatabase")
    def test_get_schema_info(self, mock_graph_db):
        """Test schema information retrieval."""
        # Setup mock
        mock_driver = Mock()
        mock_session = Mock()

        # Mock label query result
        labels_result = Mock()
        labels_result.single.return_value = {
            "labels": ["Gene", "Protein", "Disease", "Drug"]
        }

        # Mock relationship types result
        types_result = Mock()
        types_result.single.return_value = {"types": ["ENCODES", "TREATS", "TARGETS"]}

        # Mock property queries for each label type
        gene_props = Mock()
        gene_props.single.return_value = {"props": ["gene_id", "gene_name"]}

        protein_props = Mock()
        protein_props.single.return_value = {"props": ["protein_id", "protein_name"]}

        disease_props = Mock()
        disease_props.single.return_value = {"props": ["disease_id", "disease_name"]}

        drug_props = Mock()
        drug_props.single.return_value = {"props": ["drug_id", "drug_name"]}

        mock_session.run.side_effect = [
            labels_result,
            types_result,
            gene_props,
            protein_props,
            disease_props,
            drug_props,
        ]
        mock_session_cm = Mock()
        mock_session_cm.__enter__ = Mock(return_value=mock_session)
        mock_session_cm.__exit__ = Mock(return_value=None)
        mock_driver.session.return_value = mock_session_cm
        mock_graph_db.driver.return_value = mock_driver

        # Test
        interface = GraphInterface("bolt://localhost:7687", "neo4j", "password")
        schema = interface.get_schema_info()

        assert "node_labels" in schema
        assert "relationship_types" in schema
        assert "node_properties" in schema
        assert "Gene" in schema["node_labels"]
        assert "ENCODES" in schema["relationship_types"]

    @patch("src.agents.graph_interface.GraphDatabase")
    def test_validate_query(self, mock_graph_db):
        """Test query validation."""
        # Setup mock
        mock_driver = Mock()
        mock_session = Mock()

        mock_session_cm = Mock()
        mock_session_cm.__enter__ = Mock(return_value=mock_session)
        mock_session_cm.__exit__ = Mock(return_value=None)
        mock_driver.session.return_value = mock_session_cm
        mock_graph_db.driver.return_value = mock_driver

        # Test valid query
        interface = GraphInterface("bolt://localhost:7687", "neo4j", "password")
        assert interface.validate_query("MATCH (n) RETURN n") is True

        # Test invalid query
        mock_session.run.side_effect = Exception("Invalid query")
        assert interface.validate_query("INVALID QUERY") is False
