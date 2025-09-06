"""
Tests for the workflow agent module.
"""

from unittest.mock import Mock, patch

from src.agents.workflow_agent import WorkflowAgent, WorkflowState


class TestWorkflowAgent:

    @patch("src.agents.workflow_agent.Anthropic")
    def setup_method(self, method, mock_anthropic):
        """Setup test fixtures."""
        self.mock_graph_interface = Mock()
        self.mock_graph_interface.get_schema_info.return_value = {
            "node_labels": ["Gene", "Protein", "Disease", "Drug"],
            "relationship_types": ["ENCODES", "TREATS", "TARGETS"],
            "node_properties": {
                "Gene": ["gene_id", "gene_name"],
                "Protein": ["protein_id", "protein_name"],
                "Disease": ["disease_id", "disease_name"],
                "Drug": ["drug_id", "drug_name"],
            },
            "relationship_properties": {},
        }
        self.mock_graph_interface.get_property_values.return_value = [
            "diabetes",
            "hypertension",
            "cancer",
        ]

        self.mock_anthropic_client = Mock()
        mock_anthropic.return_value = self.mock_anthropic_client

        self.agent = WorkflowAgent(self.mock_graph_interface, "test_api_key")

    def test_classify_question(self):
        """Test question classification."""
        state = WorkflowState(
            user_question="What genes are associated with diabetes?",
            question_type=None,
            entities=None,
            cypher_query=None,
            results=None,
            final_answer=None,
            error=None,
        )

        mock_response = Mock()
        mock_response.content = [Mock(text="gene_disease")]
        self.mock_anthropic_client.messages.create.return_value = mock_response

        result = self.agent.classify_question(state)

        assert result["question_type"] == "gene_disease"
        self.mock_anthropic_client.messages.create.assert_called_once()

    def test_extract_entities(self):
        """Test entity extraction."""
        state = WorkflowState(
            user_question="What drugs treat hypertension?",
            question_type="drug_treatment",
            entities=None,
            cypher_query=None,
            results=None,
            final_answer=None,
            error=None,
        )

        mock_response = Mock()
        mock_response.content = [Mock(text='["hypertension", "drugs"]')]
        self.mock_anthropic_client.messages.create.return_value = mock_response

        result = self.agent.extract_entities(state)

        assert result["entities"] == ["hypertension", "drugs"]
        assert len(result["entities"]) == 2

    def test_answer_question_integration(self):
        """Test the full answer_question workflow."""
        # Mock all the responses
        mock_responses = [
            Mock(content=[Mock(text="drug_treatment")]),  # classify
            Mock(content=[Mock(text='["hypertension"]')]),  # extract
            Mock(
                content=[
                    Mock(
                        text="MATCH (dr:Drug)-[:TREATS]->(d:Disease) "
                        "WHERE toLower(d.disease_name) CONTAINS 'hypertension' "
                        "RETURN dr.drug_name, d.disease_name LIMIT 10"
                    )
                ]
            ),  # generate
            Mock(
                content=[
                    Mock(text="Several drugs treat hypertension including AlphaCure.")
                ]
            ),  # format
        ]
        self.mock_anthropic_client.messages.create.side_effect = mock_responses

        self.mock_graph_interface.execute_query.return_value = [
            {"drug_name": "AlphaCure", "disease_name": "Hypertension"}
        ]

        result = self.agent.answer_question("What drugs treat hypertension?")

        assert "answer" in result
        assert "cypher_query" in result
        assert "entities" in result
        assert "results_count" in result
        assert result["results_count"] == 1
