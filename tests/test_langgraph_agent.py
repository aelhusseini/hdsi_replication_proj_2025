"""
Tests for the LangGraph agent module.
"""

from unittest.mock import Mock, patch

from src.agents.langgraph_agent import AgentState, LifeScienceAgent


class TestLifeScienceAgent:

    @patch("src.agents.langgraph_agent.Anthropic")
    def setup_method(self, method, mock_anthropic):
        """Setup test fixtures."""
        self.mock_graph_interface = Mock()
        self.mock_graph_interface.get_schema_info.return_value = {
            "node_labels": ["Gene", "Protein", "Disease", "Drug"],
            "relationship_types": ["ENCODES", "TREATS", "TARGETS"],
            "node_properties": {
                "Gene": ["gene_id", "gene_name"],
                "Protein": ["protein_id", "protein_name"],
            },
        }

        self.mock_anthropic_client = Mock()
        mock_anthropic.return_value = self.mock_anthropic_client

        self.agent = LifeScienceAgent(self.mock_graph_interface, "test_api_key")

    def test_classify_question(self):
        """Test question classification."""
        state = AgentState(
            user_question="What genes are associated with diabetes?",
            question_type=None,
            entities=None,
            cypher_query=None,
            query_results=None,
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
        state = AgentState(
            user_question="What drugs treat hypertension?",
            question_type="drug_treatment",
            entities=None,
            cypher_query=None,
            query_results=None,
            final_answer=None,
            error=None,
        )

        mock_response = Mock()
        mock_response.content = [
            Mock(text='[{"type": "disease", "name": "hypertension"}]')
        ]
        self.mock_anthropic_client.messages.create.return_value = mock_response

        result = self.agent.extract_entities(state)

        assert result["entities"] == [{"type": "disease", "name": "hypertension"}]
        assert len(result["entities"]) == 1

    def test_generate_cypher_query(self):
        """Test Cypher query generation."""
        state = AgentState(
            user_question="What protein does GENE_ALPHA encode?",
            question_type="gene_protein",
            entities=[{"type": "gene", "name": "GENE_ALPHA"}],
            cypher_query=None,
            query_results=None,
            final_answer=None,
            error=None,
        )

        expected_query = (
            "MATCH (g:Gene {gene_name: 'GENE_ALPHA'})-[:ENCODES]->(p:Protein) "
            "RETURN g.gene_name as gene, p.protein_name as protein"
        )

        mock_response = Mock()
        mock_response.content = [Mock(text=expected_query)]
        self.mock_anthropic_client.messages.create.return_value = mock_response

        result = self.agent.generate_cypher_query(state)

        assert "MATCH" in result["cypher_query"]
        assert "GENE_ALPHA" in result["cypher_query"]
        assert "ENCODES" in result["cypher_query"]

    def test_execute_query_success(self):
        """Test successful query execution."""
        state = AgentState(
            user_question="Test question",
            question_type="test",
            entities=None,
            cypher_query="MATCH (n) RETURN n LIMIT 1",
            query_results=None,
            final_answer=None,
            error=None,
        )

        expected_results = [{"name": "test_node"}]
        self.mock_graph_interface.validate_query.return_value = True
        self.mock_graph_interface.execute_query.return_value = expected_results

        result = self.agent.execute_query(state)

        assert result["query_results"] == expected_results
        assert result["error"] is None

    def test_execute_query_error(self):
        """Test query execution with error."""
        state = AgentState(
            user_question="Test question",
            question_type="test",
            entities=None,
            cypher_query="INVALID QUERY",
            query_results=None,
            final_answer=None,
            error=None,
        )

        self.mock_graph_interface.validate_query.return_value = False

        result = self.agent.execute_query(state)

        assert result["error"] is not None
        assert "Invalid Cypher query" in result["error"]

    def test_format_response(self):
        """Test response formatting."""
        state = AgentState(
            user_question="What genes are associated with diabetes?",
            question_type="gene_disease",
            entities=None,
            cypher_query=None,
            query_results=[
                {"gene": "GENE_ALPHA", "disease": "Diabetes"},
                {"gene": "GENE_BETA", "disease": "Diabetes"},
            ],
            final_answer=None,
            error=None,
        )

        expected_answer = (
            "Two genes are associated with diabetes: GENE_ALPHA and GENE_BETA."
        )
        mock_response = Mock()
        mock_response.content = [Mock(text=expected_answer)]
        self.mock_anthropic_client.messages.create.return_value = mock_response

        result = self.agent.format_response(state)

        assert result["final_answer"] == expected_answer

    def test_answer_question_integration(self):
        """Test the full answer_question workflow."""
        # Mock all the responses
        mock_responses = [
            Mock(content=[Mock(text="gene_disease")]),  # classify
            Mock(
                content=[Mock(text='[{"type": "disease", "name": "diabetes"}]')]
            ),  # extract
            Mock(
                content=[
                    Mock(
                        text="MATCH (g:Gene)-[:LINKED_TO]->(d:Disease) "
                        "WHERE d.disease_name = 'Diabetes' RETURN g, d"
                    )
                ]
            ),  # generate
            Mock(
                content=[
                    Mock(text="GENE_ALPHA and GENE_BETA are associated with diabetes.")
                ]
            ),  # format
        ]
        self.mock_anthropic_client.messages.create.side_effect = mock_responses

        self.mock_graph_interface.validate_query.return_value = True
        self.mock_graph_interface.execute_query.return_value = [
            {"gene": "GENE_ALPHA", "disease": "Diabetes"}
        ]

        result = self.agent.answer_question("What genes are associated with diabetes?")

        assert "answer" in result
        assert "cypher_query" in result
        assert "entities" in result
        assert "results_count" in result
        assert result["results_count"] == 1
