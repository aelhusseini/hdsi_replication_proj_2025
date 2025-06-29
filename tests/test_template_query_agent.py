"""
Tests for the template query agent module.
"""

from unittest.mock import Mock

from src.agents.template_query_agent import TemplateQueryAgent


class TestTemplateQueryAgent:

    def setup_method(self):
        """Setup test fixtures."""
        self.mock_graph_interface = Mock()
        self.agent = TemplateQueryAgent(self.mock_graph_interface)

    def test_get_genes_for_disease(self):
        """Test getting genes for a disease."""
        expected_results = [
            {"gene": "GENE_ALPHA", "disease": "Diabetes"},
            {"gene": "GENE_BETA", "disease": "Diabetes"},
        ]
        self.mock_graph_interface.execute_query.return_value = expected_results

        results = self.agent.get_genes_for_disease("diabetes")

        assert results == expected_results
        self.mock_graph_interface.execute_query.assert_called_once()
        call_args = self.mock_graph_interface.execute_query.call_args
        assert "diabetes" in str(call_args)

    def test_get_drugs_for_disease(self):
        """Test getting drugs for a disease."""
        expected_results = [
            {"drug": "AlphaCure", "disease": "Hypertension", "efficacy": "high"},
            {"drug": "BetaTherapy", "disease": "Hypertension", "efficacy": "medium"},
        ]
        self.mock_graph_interface.execute_query.return_value = expected_results

        results = self.agent.get_drugs_for_disease("hypertension")

        assert results == expected_results
        assert len(results) == 2
        assert results[0]["efficacy"] == "high"

    def test_get_protein_for_gene(self):
        """Test getting protein encoded by a gene."""
        expected_results = [
            {"gene": "GENE_ALPHA", "protein": "PROT_ALPHA", "molecular_weight": 45000}
        ]
        self.mock_graph_interface.execute_query.return_value = expected_results

        results = self.agent.get_protein_for_gene("GENE_ALPHA")

        assert results == expected_results
        assert results[0]["molecular_weight"] == 45000

    def test_get_diseases_for_protein(self):
        """Test getting diseases associated with a protein."""
        expected_results = [
            {"protein": "PROT_BETA", "disease": "Cancer", "association_type": "causal"},
            {
                "protein": "PROT_BETA",
                "disease": "Diabetes",
                "association_type": "risk_factor",
            },
        ]
        self.mock_graph_interface.execute_query.return_value = expected_results

        results = self.agent.get_diseases_for_protein("PROT_BETA")

        assert results == expected_results
        assert len(results) == 2

    def test_get_drug_targets(self):
        """Test getting protein targets of a drug."""
        expected_results = [
            {
                "drug": "AlphaCure",
                "protein": "PROT_ALPHA",
                "interaction_type": "inhibition",
            }
        ]
        self.mock_graph_interface.execute_query.return_value = expected_results

        results = self.agent.get_drug_targets("AlphaCure")

        assert results == expected_results
        assert results[0]["interaction_type"] == "inhibition"

    def test_get_pathway_for_disease(self):
        """Test getting complete pathway for a disease."""
        expected_results = [
            {
                "gene": "GENE_ALPHA",
                "protein": "PROT_ALPHA",
                "disease": "Diabetes",
                "drug": "AlphaCure",
            }
        ]
        self.mock_graph_interface.execute_query.return_value = expected_results

        results = self.agent.get_pathway_for_disease("diabetes")

        assert results == expected_results
        assert "gene" in results[0]
        assert "drug" in results[0]
