#!/usr/bin/env python3
"""
Neo4j Biomedical Knowledge Graph Data Loader

This script populates a Neo4j graph database with structured biomedical data
including genes, proteins, diseases, drugs, and their complex relationships.
It creates a comprehensive knowledge graph suitable for AI-powered biomedical
query systems and research applications.

The script handles:
- Entity creation (genes, proteins, diseases, drugs)
- Relationship establishment (encodes, treats, targets, associations)
- Database constraints for data integrity
- Derived relationship computation (gene-disease links)
- Complete database rebuild with cleanup

Data Sources:
    Reads CSV files from the data/ directory:
    - genes.csv: Gene entities with chromosomal and functional information
    - proteins.csv: Protein entities with structural data
    - diseases.csv: Disease entities with prevalence and severity data
    - drugs.csv: Drug entities with approval status and mechanisms
    - protein_disease_associations.csv: Protein-disease relationships
    - drug_disease_treatments.csv: Drug treatment relationships
    - drug_protein_targets.csv: Drug-protein target interactions

Usage:
    python scripts/load_data.py

Environment Variables:
    NEO4J_URI: Database connection URI (default: bolt://localhost:7687)
    NEO4J_USER: Database username (default: neo4j)
    NEO4J_PASSWORD: Database password (required)
"""

import logging
import os

import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Neo4jDataLoader:
    """
    A comprehensive data loader for populating Neo4j with biomedical knowledge graph data.

    This class manages the complete process of loading structured biomedical data
    into a Neo4j graph database. It handles entity creation, relationship establishment,
    constraint management, and data integrity verification.

    The loader creates a knowledge graph with the following schema:
    - Nodes: Gene, Protein, Disease, Drug
    - Relationships: ENCODES, ASSOCIATED_WITH, TREATS, TARGETS, LINKED_TO

    Features:
    - Transactional loading with proper error handling
    - Database constraint creation for performance optimization
    - Automated derived relationship computation
    - Complete database rebuilding capability
    - Progress logging throughout the loading process

    Example:
        >>> loader = Neo4jDataLoader("bolt://localhost:7687", "neo4j", "password")
        >>> loader.clear_database()
        >>> loader.create_constraints()
        >>> loader.load_genes(genes_df)
        >>> loader.close()
    """

    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize the data loader with Neo4j database connection.

        Args:
            uri: Neo4j connection URI (e.g., "bolt://localhost:7687")
            user: Database username (typically "neo4j")
            password: Database password

        Raises:
            Exception: If connection to Neo4j fails
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info("Connected to Neo4j database")

    def close(self):
        """
        Close the database connection and release resources.

        Should be called when data loading is complete to ensure proper
        cleanup of database connections.
        """
        self.driver.close()

    def clear_database(self):
        """
        Clear all existing data from the database.

        This method removes all nodes and relationships from the Neo4j database,
        providing a clean slate for fresh data loading. Use with caution as this
        operation is irreversible.

        Warning:
            This will permanently delete ALL data in the database.
            Ensure you have backups if needed before running.
        """
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Cleared existing database")

    def create_constraints(self):
        """
        Create uniqueness constraints for optimal database performance.

        Establishes unique constraints on primary identifier fields for each
        node type. These constraints:
        - Prevent duplicate entities with the same ID
        - Create automatic indexes for fast lookups
        - Ensure data integrity during bulk loading
        - Improve query performance for relationship creation

        Constraints Created:
            - Gene.gene_id: Ensures unique gene identifiers
            - Protein.protein_id: Ensures unique protein identifiers
            - Disease.disease_id: Ensures unique disease identifiers
            - Drug.drug_id: Ensures unique drug identifiers
        """
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (g:Gene) "
            "REQUIRE g.gene_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Protein) "
            "REQUIRE p.protein_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) "
            "REQUIRE d.disease_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (dr:Drug) "
            "REQUIRE dr.drug_id IS UNIQUE",
        ]

        with self.driver.session() as session:
            for constraint in constraints:
                session.run(constraint)
            logger.info("Created database constraints")

    def load_genes(self, df: pd.DataFrame):
        """
        Load gene entities into the Neo4j database.

        Creates Gene nodes with comprehensive genomic information including
        chromosomal location, biological function, and expression levels.

        Args:
            df: DataFrame containing gene data with columns:
                - gene_id: Unique gene identifier
                - gene_name: Human-readable gene name/symbol
                - chromosome: Chromosomal location
                - function: Biological function description
                - expression_level: Gene expression level

        Node Properties Created:
            Each Gene node includes genomic metadata essential for
            biomedical research and pathway analysis.
        """
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    CREATE (g:Gene {
                        gene_id: $gene_id,
                        gene_name: $gene_name,
                        chromosome: $chromosome,
                        function: $function,
                        expression_level: $expression_level
                    })
                    """,
                    gene_id=row["gene_id"],
                    gene_name=row["gene_name"],
                    chromosome=str(row["chromosome"]),
                    function=row["function"],
                    expression_level=row["expression_level"],
                )
            logger.info(f"Loaded {len(df)} genes")

    def load_proteins(self, df: pd.DataFrame):
        """
        Load protein entities and establish gene-protein encoding relationships.

        Creates Protein nodes with structural information and simultaneously
        establishes ENCODES relationships from genes to proteins, representing
        the central dogma of molecular biology (DNA → RNA → Protein).

        Args:
            df: DataFrame containing protein data with columns:
                - protein_id: Unique protein identifier
                - protein_name: Human-readable protein name
                - molecular_weight: Protein molecular weight in kDa
                - structure_type: Protein structural classification
                - gene_id: Reference to encoding gene

        Creates:
            - Protein nodes with structural metadata
            - ENCODES relationships from genes to their encoded proteins

        Note:
            Requires genes to be loaded first since this creates relationships
            to existing Gene nodes.
        """
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    CREATE (p:Protein {
                        protein_id: $protein_id,
                        protein_name: $protein_name,
                        molecular_weight: $molecular_weight,
                        structure_type: $structure_type
                    })
                    """,
                    protein_id=row["protein_id"],
                    protein_name=row["protein_name"],
                    molecular_weight=int(row["molecular_weight"]),
                    structure_type=row["structure_type"],
                )

                # Create ENCODES relationship from gene to protein
                session.run(
                    """
                    MATCH (g:Gene {gene_id: $gene_id})
                    MATCH (p:Protein {protein_id: $protein_id})
                    CREATE (g)-[:ENCODES]->(p)
                    """,
                    gene_id=row["gene_id"],
                    protein_id=row["protein_id"],
                )
            logger.info(f"Loaded {len(df)} proteins with ENCODES relationships")

    def load_diseases(self, df: pd.DataFrame):
        """
        Load disease entities into the Neo4j database.

        Creates Disease nodes with epidemiological and clinical information
        including disease classification, population prevalence, and severity metrics.

        Args:
            df: DataFrame containing disease data with columns:
                - disease_id: Unique disease identifier
                - disease_name: Human-readable disease name
                - category: Disease classification (e.g., "metabolic", "neurological")
                - prevalence: Population prevalence rate
                - severity: Disease severity level

        Node Properties Created:
            Each Disease node includes clinical metadata essential for
            epidemiological analysis and treatment prioritization.
        """
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    CREATE (d:Disease {
                        disease_id: $disease_id,
                        disease_name: $disease_name,
                        category: $category,
                        prevalence: $prevalence,
                        severity: $severity
                    })
                    """,
                    disease_id=row["disease_id"],
                    disease_name=row["disease_name"],
                    category=row["category"],
                    prevalence=row["prevalence"],
                    severity=row["severity"],
                )
            logger.info(f"Loaded {len(df)} diseases")

    def load_drugs(self, df: pd.DataFrame):
        """
        Load drug entities into the Neo4j database.

        Creates Drug nodes with pharmaceutical information including drug
        classification, regulatory approval status, and mechanism of action.

        Args:
            df: DataFrame containing drug data with columns:
                - drug_id: Unique drug identifier
                - drug_name: Human-readable drug name
                - type: Drug classification (e.g., "small_molecule", "biologic")
                - approval_status: Regulatory approval status
                - mechanism: Mechanism of action description

        Node Properties Created:
            Each Drug node includes pharmaceutical metadata essential for
            drug discovery research and clinical decision-making.
        """
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    CREATE (dr:Drug {
                        drug_id: $drug_id,
                        drug_name: $drug_name,
                        type: $type,
                        approval_status: $approval_status,
                        mechanism: $mechanism
                    })
                    """,
                    drug_id=row["drug_id"],
                    drug_name=row["drug_name"],
                    type=row["type"],
                    approval_status=row["approval_status"],
                    mechanism=row["mechanism"],
                )
            logger.info(f"Loaded {len(df)} drugs")

    def load_protein_disease_associations(self, df: pd.DataFrame):
        """
        Load protein-disease association relationships.

        Creates ASSOCIATED_WITH relationships between proteins and diseases,
        representing various types of protein involvement in disease processes
        including causal relationships, biomarker associations, and therapeutic targets.

        Args:
            df: DataFrame containing association data with columns:
                - protein_id: Reference to existing protein
                - disease_id: Reference to existing disease
                - association_type: Type of association (e.g., "causal", "biomarker")
                - confidence: Confidence level of association

        Relationship Properties:
            - association_type: Describes how protein relates to disease
            - confidence: Scientific confidence in the association

        Note:
            Requires both proteins and diseases to be loaded first.
        """
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MATCH (p:Protein {protein_id: $protein_id})
                    MATCH (d:Disease {disease_id: $disease_id})
                    CREATE (p)-[:ASSOCIATED_WITH {
                        association_type: $association_type,
                        confidence: $confidence
                    }]->(d)
                    """,
                    protein_id=row["protein_id"],
                    disease_id=row["disease_id"],
                    association_type=row["association_type"],
                    confidence=row["confidence"],
                )
            logger.info(f"Loaded {len(df)} protein-disease associations")

    def load_drug_disease_treatments(self, df: pd.DataFrame):
        """
        Load drug-disease treatment relationships.

        Creates TREATS relationships between drugs and diseases, representing
        therapeutic interventions with clinical efficacy data and development stage information.

        Args:
            df: DataFrame containing treatment data with columns:
                - drug_id: Reference to existing drug
                - disease_id: Reference to existing disease
                - efficacy: Treatment efficacy level (e.g., "high", "medium", "low")
                - stage: Development stage (e.g., "approved", "phase_III", "experimental")

        Relationship Properties:
            - efficacy: Clinical effectiveness of the treatment
            - stage: Regulatory approval or clinical trial stage

        Note:
            Requires both drugs and diseases to be loaded first.
        """
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MATCH (dr:Drug {drug_id: $drug_id})
                    MATCH (d:Disease {disease_id: $disease_id})
                    CREATE (dr)-[:TREATS {
                        efficacy: $efficacy,
                        stage: $stage
                    }]->(d)
                    """,
                    drug_id=row["drug_id"],
                    disease_id=row["disease_id"],
                    efficacy=row["efficacy"],
                    stage=row["stage"],
                )
            logger.info(f"Loaded {len(df)} drug-disease treatments")

    def load_drug_protein_targets(self, df: pd.DataFrame):
        """
        Load drug-protein target relationships.

        Creates TARGETS relationships between drugs and proteins, representing
        molecular interactions including binding affinity and interaction mechanisms.

        Args:
            df: DataFrame containing target data with columns:
                - drug_id: Reference to existing drug
                - protein_id: Reference to existing protein
                - interaction_type: Type of interaction (e.g., "inhibitor", "agonist")
                - affinity: Binding affinity strength

        Relationship Properties:
            - interaction_type: Mechanism of drug-protein interaction
            - affinity: Strength of molecular binding

        Note:
            Requires both drugs and proteins to be loaded first.
        """
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MATCH (dr:Drug {drug_id: $drug_id})
                    MATCH (p:Protein {protein_id: $protein_id})
                    CREATE (dr)-[:TARGETS {
                        interaction_type: $interaction_type,
                        affinity: $affinity
                    }]->(p)
                    """,
                    drug_id=row["drug_id"],
                    protein_id=row["protein_id"],
                    interaction_type=row["interaction_type"],
                    affinity=row["affinity"],
                )
            logger.info(f"Loaded {len(df)} drug-protein targets")

    def create_gene_disease_links(self):
        """
        Create derived LINKED_TO relationships between genes and diseases.

        This method computes indirect gene-disease associations by following
        the biological pathway: Gene → Protein → Disease. When a gene encodes
        a protein that is associated with a disease, this creates a derived
        LINKED_TO relationship directly from gene to disease.

        Biological Rationale:
            If Gene A encodes Protein B, and Protein B is associated with Disease C,
            then Gene A is indirectly linked to Disease C through its protein product.
            This derived relationship enables direct gene-disease queries.

        Query Pattern:
            MATCH (gene)-[:ENCODES]->(protein)-[:ASSOCIATED_WITH]->(disease)
            CREATE (gene)-[:LINKED_TO]->(disease)

        Note:
            Only creates new relationships where none exist to avoid duplicates.
            Should be called after all entities and direct relationships are loaded.
        """
        with self.driver.session() as session:
            session.run(
                """
                MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)
                WHERE NOT EXISTS((g)-[:LINKED_TO]->(d))
                CREATE (g)-[:LINKED_TO]->(d)
                """
            )
            result = session.run(
                "MATCH ()-[r:LINKED_TO]->() RETURN count(r) as count"
            ).single()
            logger.info(f"Created {result['count']} gene-disease links")


def main():
    """
    Main entry point for loading biomedical knowledge graph data into Neo4j.

    This function orchestrates the complete data loading process:
    1. Establishes database connection using environment variables
    2. Clears existing data for fresh loading
    3. Creates database constraints for performance
    4. Loads all entity types (genes, proteins, diseases, drugs)
    5. Establishes all relationship types
    6. Computes derived relationships
    7. Handles errors gracefully with proper cleanup

    Environment Variables Required:
        NEO4J_PASSWORD: Database password (required)
        NEO4J_URI: Database URI (optional, defaults to bolt://localhost:7687)
        NEO4J_USER: Database username (optional, defaults to neo4j)

    Data Loading Order:
        The loading follows dependency order to ensure referential integrity:
        1. Entities: Genes → Proteins → Diseases → Drugs
        2. Direct relationships: Gene-Protein, Protein-Disease, Drug-Disease, Drug-Protein
        3. Derived relationships: Gene-Disease links

    Raises:
        ValueError: If required environment variables are missing
        Exception: If database connection or data loading fails
    """
    # Get database credentials from environment
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD")

    if not password:
        raise ValueError("NEO4J_PASSWORD environment variable not set")

    # Initialize data loader
    loader = Neo4jDataLoader(uri, user, password)

    try:
        # Phase 1: Database preparation
        logger.info("Starting database preparation...")
        loader.clear_database()
        loader.create_constraints()

        # Phase 2: Load entity data from CSV files
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        logger.info("Loading entity data...")

        # Load primary entities in dependency order
        genes_df = pd.read_csv(os.path.join(data_dir, "genes.csv"))
        loader.load_genes(genes_df)

        proteins_df = pd.read_csv(os.path.join(data_dir, "proteins.csv"))
        loader.load_proteins(proteins_df)  # Also creates gene-protein relationships

        diseases_df = pd.read_csv(os.path.join(data_dir, "diseases.csv"))
        loader.load_diseases(diseases_df)

        drugs_df = pd.read_csv(os.path.join(data_dir, "drugs.csv"))
        loader.load_drugs(drugs_df)

        # Phase 3: Load relationship data
        logger.info("Loading relationship data...")

        protein_disease_df = pd.read_csv(
            os.path.join(data_dir, "protein_disease_associations.csv")
        )
        loader.load_protein_disease_associations(protein_disease_df)

        drug_disease_df = pd.read_csv(
            os.path.join(data_dir, "drug_disease_treatments.csv")
        )
        loader.load_drug_disease_treatments(drug_disease_df)

        drug_protein_df = pd.read_csv(
            os.path.join(data_dir, "drug_protein_targets.csv")
        )
        loader.load_drug_protein_targets(drug_protein_df)

        # Phase 4: Compute derived relationships
        logger.info("Computing derived relationships...")
        loader.create_gene_disease_links()

        logger.info("Data loading completed successfully!")

    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise
    finally:
        # Ensure database connection is properly closed
        loader.close()


if __name__ == "__main__":
    main()
