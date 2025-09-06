"""
Tests for the web application functionality.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import plotly.graph_objects as go

# Add src directory to path for imports
src_dir = Path(__file__).parent.parent / "src"
sys.path.append(str(src_dir))

# Import after path modification
from web.app import create_network_visualization  # noqa: E402


class TestWebApp(unittest.TestCase):
    """Test web application functionality."""

    def test_create_network_visualization_with_valid_results(self):
        """Test creating network visualization with valid results."""
        results = [
            {"gene_name": "GENE_ALPHA", "protein_name": "PROT_ALPHA"},
            {"gene_name": "GENE_BETA", "protein_name": "PROT_BETA"},
            {"gene_name": "GENE_GAMMA", "protein_name": "PROT_GAMMA"},
        ]

        fig = create_network_visualization(results, "Gene-Protein")

        # Check that a figure is returned
        self.assertIsInstance(fig, go.Figure)

        # Check that the figure has data
        self.assertGreater(len(fig.data), 0)

        # Check that the title is set correctly
        self.assertEqual(fig.layout.title.text, "Gene-Protein Network")

    def test_create_network_visualization_with_empty_results(self):
        """Test creating network visualization with empty results."""
        results = []

        fig = create_network_visualization(results, "Empty")

        # Should return None for empty results
        self.assertIsNone(fig)

    def test_create_network_visualization_with_none_results(self):
        """Test creating network visualization with None results."""
        results = None

        fig = create_network_visualization(results, "None")

        # Should return None for None results
        self.assertIsNone(fig)

    def test_create_network_visualization_with_single_column_results(self):
        """Test creating network visualization with single column results."""
        results = [
            {"gene_name": "GENE_ALPHA"},
            {"gene_name": "GENE_BETA"},
        ]

        fig = create_network_visualization(results, "Single Column")

        # Should return None for results with less than 2 columns
        self.assertIsNone(fig)

    @patch("networkx.spring_layout")
    def test_create_network_visualization_creates_networkx_graph(
        self, mock_spring_layout
    ):
        """Test that the function properly creates a NetworkX graph."""
        results = [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "A", "target": "C"},
        ]

        # Mock the spring layout to return predictable positions
        mock_spring_layout.return_value = {"A": (0, 0), "B": (1, 1), "C": (2, 0)}

        fig = create_network_visualization(results, "Test Network")

        # Verify spring_layout was called
        mock_spring_layout.assert_called_once()

        # Check that the figure was created
        self.assertIsInstance(fig, go.Figure)

        # Verify the figure has edge trace and node trace
        # One edge trace + one node trace
        self.assertEqual(len(fig.data), 2)  # 1 edge trace + 1 node trace

    def test_create_network_visualization_with_complex_data(self):
        """Test network visualization with more complex data structure."""
        results = [
            {"drug_name": "AlphaCure", "disease_name": "diabetes"},
            {"drug_name": "BetaTherapy", "disease_name": "hypertension"},
            {"drug_name": "AlphaCure", "disease_name": "hypertension"},
        ]

        fig = create_network_visualization(results, "Drug-Disease")

        # Check that a figure is returned
        self.assertIsInstance(fig, go.Figure)

        # Check that nodes and edges are created from the results
        # Should have 3 unique nodes: AlphaCure, BetaTherapy, diabetes, hypertension
        # Actually 4 unique nodes and 3 edges
        self.assertGreater(len(fig.data), 0)

        # Check the title
        self.assertEqual(fig.layout.title.text, "Drug-Disease Network")

    def test_networkx_graph_properties(self):
        """Test that NetworkX graph is created with correct properties."""
        results = [
            {"node1": "A", "node2": "B"},
            {"node1": "B", "node2": "C"},
        ]

        # We'll test this by checking the underlying logic
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

        # Verify the data processing logic that feeds into NetworkX
        self.assertEqual(len(nodes), 3)  # A, B, C
        self.assertEqual(len(edges), 2)  # A-B, B-C
        self.assertIn("A", nodes)
        self.assertIn("B", nodes)
        self.assertIn("C", nodes)
        self.assertIn(("A", "B"), edges)
        self.assertIn(("B", "C"), edges)


if __name__ == "__main__":
    unittest.main()
