"""
📚 REFERENCE EXAMPLE: Simple Template-Based Agent for Common Life Sciences Queries

⚠️ NOTE: This agent is NOT used in the web application. It serves as a reference
to demonstrate template-based query approaches for users.

This module provides a straightforward, high-performance alternative to the AI-powered
LangGraph agent. Instead of using natural language processing, it offers pre-built
query templates for the most common biomedical questions.

Key Benefits:
- Fast execution (no AI inference delay)
- Predictable results (deterministic queries)
- Simple API (method names match question types)
- Reliable performance (no dependency on external AI services)
- Learning value (shows direct Cypher query patterns)

When to Use:
- Applications requiring sub-second response times
- Scenarios where AI services are unavailable or expensive
- Learning how to construct Cypher queries for biomedical data
- Batch processing or automated analysis workflows
- Integration with systems that need predictable query behavior

Supported Query Patterns:
- Gene-Disease associations
- Drug-Disease treatments
- Gene-Protein encoding relationships
- Protein-Disease associations
- Drug-Protein targets
- Complete pathway analysis
"""

from typing import Any, Dict, List

from .graph_interface import GraphInterface


class TemplateQueryAgent:
    """
    A template-based agent for executing common biomedical queries.

    This agent provides fast, reliable access to biomedical relationships using
    pre-written Cypher query templates. Each method corresponds to a common
    question pattern and returns structured results without AI processing.

    The agent is designed for:
    - High-throughput applications requiring consistent performance
    - Learning purposes to understand graph query patterns
    - Baseline comparison against AI-generated queries
    - Production systems where deterministic behavior is required

    Query Templates:
        All queries are optimized for the biomedical knowledge graph schema
        and include proper relationship types, performance optimizations,
        and result limiting for practical use.

    Example Usage:
        >>> agent = TemplateQueryAgent(graph_interface)
        >>> genes = agent.get_genes_for_disease("diabetes")
        >>> drugs = agent.get_drugs_for_disease("hypertension")
        >>> pathways = agent.get_pathway_for_disease("cancer")
    """

    def __init__(self, graph_interface: GraphInterface):
        """
        Initialize the SimpleAgent with a database connection.

        Args:
            graph_interface: An initialized GraphInterface for database operations

        Note:
            The agent loads all query templates at initialization for fast access.
            Templates are stored as parameterized Cypher queries that use safe
            parameter substitution to prevent injection attacks.
        """
        self.graph_db = graph_interface
        # Pre-compiled Cypher query templates for common biomedical questions
        # Each template uses parameterized queries ($param) for safe execution
        self.query_templates = {
            # Find genes that are associated with a specific disease
            "genes_for_disease": """
                MATCH (g:Gene)-[:LINKED_TO]->(d:Disease)
                WHERE toLower(d.disease_name) CONTAINS toLower($disease)
                RETURN g.gene_name as gene, d.disease_name as disease
                LIMIT 20
            """,
            "drugs_for_disease": """
                MATCH (dr:Drug)-[t:TREATS]->(d:Disease)
                WHERE toLower(d.disease_name) CONTAINS toLower($disease)
                RETURN dr.drug_name as drug, d.disease_name as disease,
                       t.efficacy as efficacy, t.stage as stage
                ORDER BY CASE t.efficacy
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    ELSE 3 END
                LIMIT 20
            """,
            "protein_encoded_by_gene": """
                MATCH (g:Gene)-[:ENCODES]->(p:Protein)
                WHERE toLower(g.gene_name) CONTAINS toLower($gene)
                RETURN g.gene_name as gene, p.protein_name as protein,
                       p.molecular_weight as molecular_weight
            """,
            "diseases_for_protein": """
                MATCH (p:Protein)-[a:ASSOCIATED_WITH]->(d:Disease)
                WHERE toLower(p.protein_name) CONTAINS toLower($protein)
                RETURN p.protein_name as protein, d.disease_name as disease,
                       a.association_type as association_type,
                       a.confidence as confidence
                ORDER BY CASE a.confidence
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    ELSE 3 END
                LIMIT 20
            """,
            "drug_targets": """
                MATCH (dr:Drug)-[t:TARGETS]->(p:Protein)
                WHERE toLower(dr.drug_name) CONTAINS toLower($drug)
                RETURN dr.drug_name as drug, p.protein_name as protein,
                       t.interaction_type as interaction_type, t.affinity as affinity
                LIMIT 20
            """,
            "pathway_analysis": """
                MATCH path = (g:Gene)-[:ENCODES]->(p:Protein)
                      -[:ASSOCIATED_WITH]->(d:Disease)<-[:TREATS]-(dr:Drug)
                WHERE toLower(d.disease_name) CONTAINS toLower($disease)
                RETURN g.gene_name as gene, p.protein_name as protein,
                       d.disease_name as disease, dr.drug_name as drug
                LIMIT 20
            """,
        }

    def get_genes_for_disease(self, disease: str) -> List[Dict[str, Any]]:
        """
        Find genes that are associated with a specific disease.

        This method searches for genes that have a LINKED_TO relationship with
        the specified disease in the knowledge graph. It uses case-insensitive
        matching to find diseases whose names contain the search term.

        Args:
            disease: Disease name or partial name to search for (e.g., "diabetes", "cancer")
                    Case-insensitive matching allows flexible searches

        Returns:
            List of dictionaries, each containing:
            - 'gene': Gene name (e.g., "GENE_ALPHA")
            - 'disease': Full disease name from database (e.g., "Type 2 Diabetes")

            Limited to 20 results for performance. Empty list if no associations found.

        Example:
            >>> agent = TemplateQueryAgent(graph_interface)
            >>> results = agent.get_genes_for_disease("diabetes")
            >>> for result in results:
            ...     print(f"Gene {result['gene']} is linked to {result['disease']}")
            Gene GENE_ALPHA is linked to Type 2 Diabetes
            Gene GENE_BETA is linked to Type 1 Diabetes

        Note:
            Uses the biomedical knowledge graph's Gene-Disease association data.
            Results reflect known scientific literature at the time of database creation.
        """
        return self.graph_db.execute_query(
            self.query_templates["genes_for_disease"], {"disease": disease}
        )

    def get_drugs_for_disease(self, disease: str) -> List[Dict[str, Any]]:
        """
        Find drugs that are used to treat a specific disease.

        This method searches for drugs that have a TREATS relationship with
        the specified disease. Results are ordered by treatment efficacy
        (high > medium > low) to prioritize the most effective treatments.

        Args:
            disease: Disease name or partial name to search for (e.g., "hypertension")
                    Case-insensitive matching allows flexible searches

        Returns:
            List of dictionaries, each containing:
            - 'drug': Drug name (e.g., "AlphaCure", "BetaTherapy")
            - 'disease': Full disease name from database
            - 'efficacy': Treatment efficacy level ("high", "medium", "low")
            - 'stage': Clinical trial stage or approval status

            Results ordered by efficacy (best treatments first).
            Limited to 20 results for performance.

        Example:
            >>> agent = TemplateQueryAgent(graph_interface)
            >>> treatments = agent.get_drugs_for_disease("hypertension")
            >>> for treatment in treatments:
            ...     print(f"{treatment['drug']} treats {treatment['disease']} "
            ...           f"with {treatment['efficacy']} efficacy")
            AlphaCure treats Hypertension with high efficacy
            BetaTherapy treats Essential Hypertension with medium efficacy

        Note:
            Efficacy and stage information reflect clinical trial data and
            regulatory approval status at the time of database creation.
        """
        return self.graph_db.execute_query(
            self.query_templates["drugs_for_disease"], {"disease": disease}
        )

    def get_protein_for_gene(self, gene: str) -> List[Dict[str, Any]]:
        """
        Find the protein(s) encoded by a specific gene.

        This method searches for proteins that have an ENCODES relationship from
        the specified gene. Most genes encode a single protein, but some may
        encode multiple protein variants or isoforms.

        Args:
            gene: Gene name or symbol to search for (e.g., "GENE_ALPHA", "BRCA1")
                  Case-insensitive matching allows flexible searches

        Returns:
            List of dictionaries, each containing:
            - 'gene': Gene name from database
            - 'protein': Protein name encoded by the gene
            - 'molecular_weight': Protein molecular weight (if available)

            Returns all protein variants if gene encodes multiple proteins.
            Empty list if gene not found or doesn't encode any proteins.

        Example:
            >>> agent = TemplateQueryAgent(graph_interface)
            >>> proteins = agent.get_protein_for_gene("GENE_ALPHA")
            >>> for protein in proteins:
            ...     print(f"Gene {protein['gene']} encodes protein {protein['protein']}")
            ...     if protein['molecular_weight']:
            ...         print(f"  Molecular weight: {protein['molecular_weight']} kDa")
            Gene GENE_ALPHA encodes protein PROT_ALPHA
              Molecular weight: 45.2 kDa

        Note:
            Molecular weight may not be available for all proteins.
            Reflects the central dogma of molecular biology: DNA → RNA → Protein.
        """
        return self.graph_db.execute_query(
            self.query_templates["protein_encoded_by_gene"], {"gene": gene}
        )

    def get_diseases_for_protein(self, protein: str) -> List[Dict[str, Any]]:
        """
        Find diseases that are associated with a specific protein.

        This method searches for diseases that have an ASSOCIATED_WITH relationship
        with the specified protein. Results are ordered by association confidence
        (high > medium > low) to prioritize the most reliable associations.

        Args:
            protein: Protein name to search for (e.g., "PROT_ALPHA", "insulin")
                    Case-insensitive matching allows flexible searches

        Returns:
            List of dictionaries, each containing:
            - 'protein': Protein name from database
            - 'disease': Disease name associated with the protein
            - 'association_type': Type of association (e.g., "causal", "biomarker", "therapeutic_target")
            - 'confidence': Confidence level of association ("high", "medium", "low")

            Results ordered by confidence (most reliable associations first).
            Limited to 20 results for performance.

        Example:
            >>> agent = TemplateQueryAgent(graph_interface)
            >>> associations = agent.get_diseases_for_protein("PROT_ALPHA")
            >>> for assoc in associations:
            ...     print(f"Protein {assoc['protein']} is associated with {assoc['disease']}")
            ...     print(f"  Type: {assoc['association_type']}, Confidence: {assoc['confidence']}")
            Protein PROT_ALPHA is associated with Alzheimer's Disease
              Type: causal, Confidence: high
            Protein PROT_ALPHA is associated with Diabetes
              Type: biomarker, Confidence: medium

        Note:
            Association types reflect different roles proteins play in disease:
            - causal: Protein dysfunction directly causes disease
            - biomarker: Protein levels indicate disease presence/progression
            - therapeutic_target: Protein is targeted by disease treatments
        """
        return self.graph_db.execute_query(
            self.query_templates["diseases_for_protein"], {"protein": protein}
        )

    def get_drug_targets(self, drug: str) -> List[Dict[str, Any]]:
        """
        Find protein targets of a specific drug.

        This method searches for proteins that have a TARGETS relationship with
        the specified drug. Drug-target interactions are fundamental to understanding
        how medications work at the molecular level.

        Args:
            drug: Drug name to search for (e.g., "AlphaCure", "aspirin")
                  Case-insensitive matching allows flexible searches

        Returns:
            List of dictionaries, each containing:
            - 'drug': Drug name from database
            - 'protein': Protein name targeted by the drug
            - 'interaction_type': Type of drug-protein interaction (e.g., "inhibitor", "agonist", "antagonist")
            - 'affinity': Binding affinity strength (e.g., "high", "medium", "low")

            Limited to 20 results for performance.
            Empty list if drug not found or has no known protein targets.

        Example:
            >>> agent = TemplateQueryAgent(graph_interface)
            >>> targets = agent.get_drug_targets("AlphaCure")
            >>> for target in targets:
            ...     print(f"Drug {target['drug']} targets protein {target['protein']}")
            ...     print(f"  Interaction: {target['interaction_type']}, Affinity: {target['affinity']}")
            Drug AlphaCure targets protein PROT_BETA
              Interaction: inhibitor, Affinity: high
            Drug AlphaCure targets protein PROT_GAMMA
              Interaction: antagonist, Affinity: medium

        Note:
            Interaction types describe how the drug affects protein function:
            - inhibitor: Reduces or blocks protein activity
            - agonist: Activates or enhances protein function
            - antagonist: Blocks protein's natural ligand binding
            Affinity indicates how strongly the drug binds to the protein.
        """
        return self.graph_db.execute_query(
            self.query_templates["drug_targets"], {"drug": drug}
        )

    def get_pathway_for_disease(self, disease: str) -> List[Dict[str, Any]]:
        """
        Analyze complete biological pathways from genes to treatments for a disease.

        This method performs pathway analysis by finding complete paths from genes
        through proteins to diseases and their treatments. It reveals the biological
        pathway: Gene → Protein → Disease ← Drug, showing how genetic factors
        lead to disease and how drugs provide treatment.

        Args:
            disease: Disease name to analyze pathways for (e.g., "cancer", "diabetes")
                    Case-insensitive matching allows flexible searches

        Returns:
            List of dictionaries, each representing a complete pathway:
            - 'gene': Gene involved in the disease pathway
            - 'protein': Protein encoded by the gene
            - 'disease': Disease name from database
            - 'drug': Drug that treats the disease

            Each record represents one complete biological pathway.
            Limited to 20 results for performance.

        Example:
            >>> agent = TemplateQueryAgent(graph_interface)
            >>> pathways = agent.get_pathway_for_disease("diabetes")
            >>> for pathway in pathways:
            ...     print(f"Pathway: {pathway['gene']} → {pathway['protein']} → ")
            ...     print(f"         {pathway['disease']} ← {pathway['drug']}")
            Pathway: GENE_ALPHA → PROT_ALPHA → Type 2 Diabetes ← AlphaCure
            Pathway: GENE_BETA → PROT_BETA → Type 1 Diabetes ← BetaTherapy

        Use Cases:
            - Drug discovery: Identify potential drug targets for genetic diseases
            - Personalized medicine: Connect patient genetics to treatment options
            - Research planning: Understand complete biological mechanisms
            - Systems biology: Analyze multi-level disease networks

        Note:
            This represents a simplified view of complex biological pathways.
            Real pathways often involve multiple genes, proteins, and regulatory
            mechanisms not captured in this basic four-node pattern.
        """
        return self.graph_db.execute_query(
            self.query_templates["pathway_analysis"], {"disease": disease}
        )
