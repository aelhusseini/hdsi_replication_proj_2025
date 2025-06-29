#!/usr/bin/env python3
"""
Simplified Data Loader for Learning Purposes

This is a streamlined version of the data loader focused on learning.
It demonstrates the core concepts without production complexity.

Learning Objectives:
- Understand how to populate a graph database
- See the biomedical knowledge graph schema in action
- Learn basic Neo4j operations and constraints
- Experience the data flow from CSV to graph

Usage:
    python scripts/simple_load_data.py
"""

import os

import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()


class SimpleBiomedicalLoader:
    """
    Learning data loader for biomedical knowledge graphs.

    This simplified version focuses on core concepts:
    1. Connect to Neo4j
    2. Create basic constraints
    3. Load entities (nodes)
    4. Create relationships (edges)
    5. Derive new relationships

    Perfect for understanding graph database operations!
    """

    def __init__(self):
        # Get database connection info
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD")

        if not password:
            raise ValueError("Please set NEO4J_PASSWORD in your .env file")

        # Connect to Neo4j
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("✅ Connected to Neo4j!")

    def close(self):
        """Close the database connection."""
        self.driver.close()
        print("🔒 Database connection closed")

    def clear_database(self):
        """Remove all existing data - start fresh for learning."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("🧹 Cleared existing data")

    def create_constraints(self):
        """
        Create unique constraints for our main entities.
        This ensures no duplicate IDs and improves query performance.
        """
        constraints = [
            (
                "CREATE CONSTRAINT IF NOT EXISTS FOR (g:Gene) "
                "REQUIRE g.gene_id IS UNIQUE"
            ),
            (
                "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Protein) "
                "REQUIRE p.protein_id IS UNIQUE"
            ),
            (
                "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) "
                "REQUIRE d.disease_id IS UNIQUE"
            ),
            (
                "CREATE CONSTRAINT IF NOT EXISTS FOR (dr:Drug) "
                "REQUIRE dr.drug_id IS UNIQUE"
            ),
        ]

        with self.driver.session() as session:
            for constraint in constraints:
                if isinstance(constraint, tuple):
                    # Join the tuple parts into a single string
                    constraint_str = "".join(constraint)
                    session.run(constraint_str)
                else:
                    session.run(constraint)
        print("🔧 Created database constraints")

    def load_genes(self, genes_df):
        """Load gene entities into the graph."""
        print(f"📍 Loading {len(genes_df)} genes...")

        with self.driver.session() as session:
            for _, gene in genes_df.iterrows():
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
                    **gene.to_dict(),
                )
        print("✅ Genes loaded!")

    def load_proteins(self, proteins_df):
        """Load proteins and link them to genes."""
        print(f"🧪 Loading {len(proteins_df)} proteins...")

        with self.driver.session() as session:
            for _, protein in proteins_df.iterrows():
                # Create the protein node
                session.run(
                    """
                    CREATE (p:Protein {
                        protein_id: $protein_id,
                        protein_name: $protein_name,
                        molecular_weight: $molecular_weight,
                        structure_type: $structure_type
                    })
                """,
                    **protein.to_dict(),
                )

                # Link it to its gene with ENCODES relationship
                session.run(
                    """
                    MATCH (g:Gene {gene_id: $gene_id})
                    MATCH (p:Protein {protein_id: $protein_id})
                    CREATE (g)-[:ENCODES]->(p)
                """,
                    gene_id=protein["gene_id"],
                    protein_id=protein["protein_id"],
                )

        print("✅ Proteins loaded and linked to genes!")

    def load_diseases(self, diseases_df):
        """Load disease entities."""
        print(f"🏥 Loading {len(diseases_df)} diseases...")

        with self.driver.session() as session:
            for _, disease in diseases_df.iterrows():
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
                    **disease.to_dict(),
                )
        print("✅ Diseases loaded!")

    def load_drugs(self, drugs_df):
        """Load drug entities."""
        print(f"💊 Loading {len(drugs_df)} drugs...")

        with self.driver.session() as session:
            for _, drug in drugs_df.iterrows():
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
                    **drug.to_dict(),
                )
        print("✅ Drugs loaded!")

    def create_protein_disease_links(self, associations_df):
        """Create ASSOCIATED_WITH relationships between proteins and diseases."""
        print(f"🔗 Creating {len(associations_df)} protein-disease associations...")

        with self.driver.session() as session:
            for _, assoc in associations_df.iterrows():
                session.run(
                    """
                    MATCH (p:Protein {protein_id: $protein_id})
                    MATCH (d:Disease {disease_id: $disease_id})
                    CREATE (p)-[:ASSOCIATED_WITH {
                        association_type: $association_type,
                        confidence: $confidence
                    }]->(d)
                """,
                    **assoc.to_dict(),
                )
        print("✅ Protein-disease associations created!")

    def create_drug_treatment_links(self, treatments_df):
        """Create TREATS relationships between drugs and diseases."""
        print(f"💉 Creating {len(treatments_df)} drug treatment relationships...")

        with self.driver.session() as session:
            for _, treatment in treatments_df.iterrows():
                session.run(
                    """
                    MATCH (dr:Drug {drug_id: $drug_id})
                    MATCH (d:Disease {disease_id: $disease_id})
                    CREATE (dr)-[:TREATS {
                        efficacy: $efficacy,
                        stage: $stage
                    }]->(d)
                """,
                    **treatment.to_dict(),
                )
        print("✅ Drug treatment relationships created!")

    def create_drug_target_links(self, targets_df):
        """Create TARGETS relationships between drugs and proteins."""
        print(f"🎯 Creating {len(targets_df)} drug-protein target relationships...")

        with self.driver.session() as session:
            for _, target in targets_df.iterrows():
                session.run(
                    """
                    MATCH (dr:Drug {drug_id: $drug_id})
                    MATCH (p:Protein {protein_id: $protein_id})
                    CREATE (dr)-[:TARGETS {
                        interaction_type: $interaction_type,
                        affinity: $affinity
                    }]->(p)
                """,
                    **target.to_dict(),
                )
        print("✅ Drug-protein target relationships created!")

    def create_gene_disease_links(self):
        """
        Create derived LINKED_TO relationships between genes and diseases.

        This is a great example of graph thinking:
        If Gene A encodes Protein B, and Protein B is associated with Disease C,
        then Gene A is linked to Disease C!
        """
        print("🧬 Creating derived gene-disease links...")

        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (g:Gene)-[:ENCODES]->(p:Protein)-[:ASSOCIATED_WITH]->(d:Disease)
                WHERE NOT EXISTS((g)-[:LINKED_TO]->(d))
                CREATE (g)-[:LINKED_TO]->(d)
                RETURN count(*) as links_created
            """
            )

            links_created = result.single()["links_created"]
            print(f"✅ Created {links_created} gene-disease links!")

    def print_summary(self):
        """Print a summary of what we loaded - great for learning!"""
        print("\n" + "=" * 50)
        print("📊 KNOWLEDGE GRAPH SUMMARY")
        print("=" * 50)

        with self.driver.session() as session:
            # Count nodes
            gene_count = session.run(
                "MATCH (g:Gene) RETURN count(g) as count"
            ).single()["count"]
            protein_count = session.run(
                "MATCH (p:Protein) RETURN count(p) as count"
            ).single()["count"]
            disease_count = session.run(
                "MATCH (d:Disease) RETURN count(d) as count"
            ).single()["count"]
            drug_count = session.run(
                "MATCH (dr:Drug) RETURN count(dr) as count"
            ).single()["count"]

            print(f"🧬 Genes: {gene_count}")
            print(f"🧪 Proteins: {protein_count}")
            print(f"🏥 Diseases: {disease_count}")
            print(f"💊 Drugs: {drug_count}")

            # Count relationships
            encodes_count = session.run(
                "MATCH ()-[r:ENCODES]->() RETURN count(r) as count"
            ).single()["count"]
            linked_count = session.run(
                "MATCH ()-[r:LINKED_TO]->() RETURN count(r) as count"
            ).single()["count"]
            assoc_count = session.run(
                "MATCH ()-[r:ASSOCIATED_WITH]->() RETURN count(r) as count"
            ).single()["count"]
            treats_count = session.run(
                "MATCH ()-[r:TREATS]->() RETURN count(r) as count"
            ).single()["count"]
            targets_count = session.run(
                "MATCH ()-[r:TARGETS]->() RETURN count(r) as count"
            ).single()["count"]

            print("\n🔗 Relationships:")
            print(f"   ENCODES: {encodes_count}")
            print(f"   LINKED_TO: {linked_count}")
            print(f"   ASSOCIATED_WITH: {assoc_count}")
            print(f"   TREATS: {treats_count}")
            print(f"   TARGETS: {targets_count}")

        print("=" * 50)
        print("🎉 Knowledge graph is ready for learning!")


def main():
    """
    Main function that loads all the biomedical data.
    This shows the complete flow from CSV files to graph database!
    """
    print("🚀 Starting Simple Biomedical Knowledge Graph Loader")
    print("This learning version focuses on core concepts!")
    print()

    # Initialize the loader
    loader = SimpleBiomedicalLoader()

    try:
        # Step 1: Prepare the database
        print("📋 Step 1: Database Preparation")
        loader.clear_database()
        loader.create_constraints()
        print()

        # Step 2: Load entity data
        print("📋 Step 2: Loading Entities (Nodes)")
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

        # Load all the CSV files
        genes_df = pd.read_csv(os.path.join(data_dir, "genes.csv"))
        proteins_df = pd.read_csv(os.path.join(data_dir, "proteins.csv"))
        diseases_df = pd.read_csv(os.path.join(data_dir, "diseases.csv"))
        drugs_df = pd.read_csv(os.path.join(data_dir, "drugs.csv"))

        # Load entities in order (genes first, then proteins that depend on genes)
        loader.load_genes(genes_df)
        loader.load_proteins(proteins_df)  # Also creates gene→protein links
        loader.load_diseases(diseases_df)
        loader.load_drugs(drugs_df)
        print()

        # Step 3: Create relationships
        print("📋 Step 3: Creating Relationships (Edges)")

        # Load relationship data
        protein_disease_df = pd.read_csv(
            os.path.join(data_dir, "protein_disease_associations.csv")
        )
        drug_disease_df = pd.read_csv(
            os.path.join(data_dir, "drug_disease_treatments.csv")
        )
        drug_protein_df = pd.read_csv(
            os.path.join(data_dir, "drug_protein_targets.csv")
        )

        # Create all the relationships
        loader.create_protein_disease_links(protein_disease_df)
        loader.create_drug_treatment_links(drug_disease_df)
        loader.create_drug_target_links(drug_protein_df)
        print()

        # Step 4: Derive new knowledge
        print("📋 Step 4: Computing Derived Relationships")
        loader.create_gene_disease_links()
        print()

        # Step 5: Show what we built
        loader.print_summary()

        print("\n🎓 Ready for learning! Try these commands:")
        print("   pdm run app  # Start the interactive app")
        print(
            "   jupyter notebook tutorial_langgraph_knowledge_graphs.ipynb  # "
            "Open tutorial"
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        raise
    finally:
        loader.close()


if __name__ == "__main__":
    main()
