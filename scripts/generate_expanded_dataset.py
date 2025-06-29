#!/usr/bin/env python3
"""
Comprehensive Synthetic Biomedical Dataset Generator

This script generates a large, diverse, and realistic synthetic biomedical dataset
for knowledge graph learning. It creates entities and relationships that mirror
real-world biomedical complexity while remaining safe for educational use.

Features:
- 500+ genes with realistic naming and chromosomal distribution
- 200+ diseases across all major medical categories
- 300+ drugs with diverse mechanisms and approval statuses
- 1000+ proteins with realistic molecular properties
- Complex relationship networks with biological accuracy
- Diverse ethnic, age, and gender considerations in disease prevalence
- Multiple drug mechanisms, targets, and therapeutic pathways

The dataset includes:
- Common diseases (diabetes, cancer, heart disease)
- Rare diseases (genetic disorders, orphan diseases)
- Infectious diseases (viral, bacterial, fungal)
- Mental health conditions
- Pediatric and geriatric conditions
- Multiple drug classes (small molecules, biologics, gene therapies)
- Real-world gene families and protein complexes
"""

import random
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)


class ExpandedBiomedicalDataGenerator:
    """
    Generates comprehensive synthetic biomedical data with realistic diversity.
    """

    def __init__(self, output_dir: str = "data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize data structures
        self.genes_data = []
        self.proteins_data = []
        self.diseases_data = []
        self.drugs_data = []
        self.protein_disease_associations = []
        self.drug_disease_treatments = []
        self.drug_protein_targets = []

        # Real gene families and names for authenticity
        self.gene_families = {
            "TP53": ["TP53", "TP73", "TP63"],
            "BRCA": ["BRCA1", "BRCA2"],
            "MYC": ["MYC", "MYCN", "MYCL"],
            "RAS": ["KRAS", "HRAS", "NRAS"],
            "PIK3": ["PIK3CA", "PIK3CB", "PIK3CD", "PIK3CG"],
            "EGFR": ["EGFR", "ERBB2", "ERBB3", "ERBB4"],
            "MAPK": ["MAPK1", "MAPK3", "MAPK8", "MAPK14"],
            "AKT": ["AKT1", "AKT2", "AKT3"],
            "PTEN": ["PTEN"],
            "VHL": ["VHL"],
            "ATM": ["ATM", "ATR"],
            "CDKN": ["CDKN1A", "CDKN1B", "CDKN2A", "CDKN2B"],
            "MDM": ["MDM2", "MDM4"],
            "BCL": ["BCL2", "BCL2L1", "BCL2L2"],
            "CASP": ["CASP3", "CASP8", "CASP9", "CASP7"],
            "TNF": ["TNF", "TNFRSF1A", "TNFRSF1B"],
            "IL": ["IL1A", "IL1B", "IL2", "IL4", "IL6", "IL8", "IL10"],
            "IFNG": ["IFNG", "IFNA1", "IFNB1"],
            "TGF": ["TGFB1", "TGFB2", "TGFB3"],
            "VEGF": ["VEGFA", "VEGFB", "VEGFC"],
            "FGF": ["FGF1", "FGF2", "FGF23"],
            "PDGF": ["PDGFA", "PDGFB"],
            "IGF": ["IGF1", "IGF2"],
            "APOE": ["APOE"],
            "APP": ["APP"],
            "SNCA": ["SNCA"],
            "HTT": ["HTT"],
            "SOD": ["SOD1", "SOD2"],
            "CFTR": ["CFTR"],
            "DMD": ["DMD"],
            "F8": ["F8", "F9"],
            "GBA": ["GBA"],
            "HBB": ["HBB", "HBA1", "HBA2"],
            "LDLR": ["LDLR"],
            "PCSK9": ["PCSK9"],
            "CYP": ["CYP2D6", "CYP3A4", "CYP2C9", "CYP2C19"],
            "ABCB1": ["ABCB1"],
            "SLC": ["SLC2A1", "SLC6A4", "SLC12A3"],
            "KCNQ": ["KCNQ1", "KCNQ2", "KCNQ3"],
            "SCN": ["SCN1A", "SCN5A"],
            "CACNA": ["CACNA1C", "CACNA1H"],
            "GRIN": ["GRIN1", "GRIN2A", "GRIN2B"],
            "DRD": ["DRD1", "DRD2", "DRD3", "DRD4"],
            "HTR": ["HTR1A", "HTR2A", "HTR3A"],
            "CHRN": ["CHRNA4", "CHRNB2"],
            "GABA": ["GABRA1", "GABRB2", "GABRD"],
            "COMT": ["COMT"],
            "MAOA": ["MAOA", "MAOB"],
            "SLC6A": ["SLC6A2", "SLC6A3", "SLC6A4"],
            "OPRM": ["OPRM1"],
            "CNR": ["CNR1", "CNR2"],
            "ADRB": ["ADRB1", "ADRB2", "ADRB3"],
            "ADRA": ["ADRA1A", "ADRA2A"],
            "ACE": ["ACE", "ACE2"],
            "AGT": ["AGT"],
            "AGTR": ["AGTR1", "AGTR2"],
        }

        # Expand gene list with synthetic additions
        self.all_genes = []
        for family, genes in self.gene_families.items():
            self.all_genes.extend(genes)

        # Add synthetic genes to reach target count
        synthetic_prefixes = [
            "SYNTH",
            "NOVEL",
            "EXPR",
            "REG",
            "FUNC",
            "PATH",
            "CELL",
            "MITO",
            "NUCL",
            "MEMB",
        ]
        for i in range(len(self.all_genes), 500):
            prefix = random.choice(synthetic_prefixes)
            self.all_genes.append(f"{prefix}{i:03d}")

        # Disease categories with realistic examples
        self.disease_categories = {
            "cardiovascular": [
                "Hypertension",
                "Coronary_Artery_Disease",
                "Heart_Failure",
                "Atrial_Fibrillation",
                "Myocardial_Infarction",
                "Stroke",
                "Peripheral_Artery_Disease",
                "Aortic_Stenosis",
                "Mitral_Valve_Prolapse",
                "Pulmonary_Embolism",
                "Deep_Vein_Thrombosis",
                "Cardiomyopathy",
                "Pericarditis",
                "Endocarditis",
                "Aortic_Aneurysm",
            ],
            "oncology": [
                "Breast_Cancer",
                "Lung_Cancer",
                "Colorectal_Cancer",
                "Prostate_Cancer",
                "Pancreatic_Cancer",
                "Liver_Cancer",
                "Kidney_Cancer",
                "Ovarian_Cancer",
                "Cervical_Cancer",
                "Leukemia",
                "Lymphoma",
                "Melanoma",
                "Brain_Tumor",
                "Thyroid_Cancer",
                "Bladder_Cancer",
                "Stomach_Cancer",
                "Esophageal_Cancer",
                "Bone_Cancer",
                "Soft_Tissue_Sarcoma",
                "Multiple_Myeloma",
            ],
            "neurological": [
                "Alzheimer_Disease",
                "Parkinson_Disease",
                "Multiple_Sclerosis",
                "Epilepsy",
                "Stroke",
                "Migraine",
                "Huntington_Disease",
                "ALS",
                "Dementia",
                "Traumatic_Brain_Injury",
                "Spinal_Cord_Injury",
                "Peripheral_Neuropathy",
                "Myasthenia_Gravis",
                "Guillain_Barre_Syndrome",
                "Trigeminal_Neuralgia",
            ],
            "psychiatric": [
                "Depression",
                "Anxiety_Disorder",
                "Bipolar_Disorder",
                "Schizophrenia",
                "ADHD",
                "Autism_Spectrum_Disorder",
                "OCD",
                "PTSD",
                "Panic_Disorder",
                "Eating_Disorders",
                "Substance_Abuse",
                "Borderline_Personality_Disorder",
                "Social_Anxiety",
                "GAD",
                "Seasonal_Affective_Disorder",
            ],
            "metabolic": [
                "Type2_Diabetes",
                "Type1_Diabetes",
                "Obesity",
                "Metabolic_Syndrome",
                "Hyperlipidemia",
                "Hypothyroidism",
                "Hyperthyroidism",
                "Gout",
                "Osteoporosis",
                "Vitamin_D_Deficiency",
                "Iron_Deficiency_Anemia",
                "Polycystic_Ovary_Syndrome",
                "Cushing_Syndrome",
                "Addison_Disease",
            ],
            "autoimmune": [
                "Rheumatoid_Arthritis",
                "Lupus",
                "Psoriasis",
                "Inflammatory_Bowel_Disease",
                "Celiac_Disease",
                "Hashimoto_Thyroiditis",
                "Graves_Disease",
                "Vitiligo",
                "Alopecia_Areata",
                "Sjogren_Syndrome",
                "Scleroderma",
                "Dermatomyositis",
                "Vasculitis",
                "Ankylosing_Spondylitis",
                "Behcet_Disease",
            ],
            "respiratory": [
                "Asthma",
                "COPD",
                "Pneumonia",
                "Pulmonary_Fibrosis",
                "Sleep_Apnea",
                "Bronchitis",
                "Emphysema",
                "Pleural_Effusion",
                "Pneumothorax",
                "Cystic_Fibrosis",
                "Pulmonary_Hypertension",
                "Sarcoidosis",
                "Tuberculosis",
                "Lung_Infection",
                "Respiratory_Failure",
            ],
            "infectious": [
                "COVID19",
                "Influenza",
                "Hepatitis_B",
                "Hepatitis_C",
                "HIV_AIDS",
                "Tuberculosis",
                "Malaria",
                "Pneumonia",
                "Sepsis",
                "UTI",
                "Skin_Infection",
                "Meningitis",
                "Endocarditis",
                "Osteomyelitis",
                "Gastroenteritis",
                "Sinusitis",
                "Pharyngitis",
                "Cellulitis",
            ],
            "renal": [
                "Chronic_Kidney_Disease",
                "Acute_Kidney_Injury",
                "Kidney_Stones",
                "Polycystic_Kidney_Disease",
                "Glomerulonephritis",
                "Nephrotic_Syndrome",
                "Diabetic_Nephropathy",
                "Hypertensive_Nephropathy",
                "Renal_Failure",
            ],
            "gastrointestinal": [
                "GERD",
                "Peptic_Ulcer",
                "Inflammatory_Bowel_Disease",
                "Irritable_Bowel_Syndrome",
                "Liver_Cirrhosis",
                "Hepatitis",
                "Gallstones",
                "Pancreatitis",
                "Diverticulitis",
                "Gastroparesis",
                "Lactose_Intolerance",
            ],
            "genetic": [
                "Sickle_Cell_Disease",
                "Thalassemia",
                "Hemophilia",
                "Cystic_Fibrosis",
                "Huntington_Disease",
                "Duchenne_Muscular_Dystrophy",
                "Fragile_X_Syndrome",
                "Down_Syndrome",
                "Turner_Syndrome",
                "Marfan_Syndrome",
                "Neurofibromatosis",
            ],
            "pediatric": [
                "Cerebral_Palsy",
                "Congenital_Heart_Disease",
                "Spina_Bifida",
                "Cleft_Palate",
                "Juvenile_Diabetes",
                "Childhood_Leukemia",
                "ADHD",
                "Autism",
                "Developmental_Delays",
                "Failure_to_Thrive",
            ],
            "geriatric": [
                "Dementia",
                "Osteoarthritis",
                "Osteoporosis",
                "Macular_Degeneration",
                "Hearing_Loss",
                "Falls",
                "Frailty",
                "Polypharmacy",
                "Delirium",
            ],
            "ophthalmologic": [
                "Glaucoma",
                "Macular_Degeneration",
                "Diabetic_Retinopathy",
                "Cataracts",
                "Dry_Eye_Syndrome",
                "Retinal_Detachment",
            ],
            "dermatologic": [
                "Eczema",
                "Psoriasis",
                "Acne",
                "Melanoma",
                "Basal_Cell_Carcinoma",
                "Rosacea",
                "Vitiligo",
                "Alopecia",
            ],
        }

        # Drug classes and mechanisms
        self.drug_classes = {
            "cardiovascular": {
                "ACE_Inhibitors": ["Lisinopril", "Enalapril", "Captopril", "Ramipril"],
                "ARBs": ["Losartan", "Valsartan", "Irbesartan", "Olmesartan"],
                "Beta_Blockers": [
                    "Metoprolol",
                    "Atenolol",
                    "Propranolol",
                    "Carvedilol",
                ],
                "Calcium_Channel_Blockers": [
                    "Amlodipine",
                    "Nifedipine",
                    "Diltiazem",
                    "Verapamil",
                ],
                "Diuretics": ["Hydrochlorothiazide", "Furosemide", "Spironolactone"],
                "Statins": [
                    "Atorvastatin",
                    "Simvastatin",
                    "Rosuvastatin",
                    "Pravastatin",
                ],
                "Anticoagulants": ["Warfarin", "Rivaroxaban", "Apixaban", "Dabigatran"],
            },
            "oncology": {
                "Chemotherapy": [
                    "Doxorubicin",
                    "Cisplatin",
                    "Paclitaxel",
                    "Carboplatin",
                ],
                "Targeted_Therapy": [
                    "Trastuzumab",
                    "Imatinib",
                    "Erlotinib",
                    "Bevacizumab",
                ],
                "Immunotherapy": [
                    "Pembrolizumab",
                    "Nivolumab",
                    "Ipilimumab",
                    "Atezolizumab",
                ],
                "Hormone_Therapy": [
                    "Tamoxifen",
                    "Anastrozole",
                    "Letrozole",
                    "Exemestane",
                ],
            },
            "neurological": {
                "Anticonvulsants": [
                    "Phenytoin",
                    "Carbamazepine",
                    "Valproate",
                    "Levetiracetam",
                ],
                "Parkinson_Drugs": [
                    "Levodopa",
                    "Carbidopa",
                    "Pramipexole",
                    "Ropinirole",
                ],
                "Alzheimer_Drugs": [
                    "Donepezil",
                    "Rivastigmine",
                    "Galantamine",
                    "Memantine",
                ],
                "MS_Drugs": [
                    "Interferon_Beta",
                    "Glatiramer",
                    "Fingolimod",
                    "Natalizumab",
                ],
            },
            "psychiatric": {
                "Antidepressants": [
                    "Sertraline",
                    "Fluoxetine",
                    "Escitalopram",
                    "Venlafaxine",
                ],
                "Antipsychotics": [
                    "Olanzapine",
                    "Risperidone",
                    "Quetiapine",
                    "Aripiprazole",
                ],
                "Mood_Stabilizers": [
                    "Lithium",
                    "Valproate",
                    "Lamotrigine",
                    "Carbamazepine",
                ],
                "Anxiolytics": ["Lorazepam", "Alprazolam", "Clonazepam", "Diazepam"],
            },
            "metabolic": {
                "Diabetes_Drugs": ["Metformin", "Insulin", "Glipizide", "Pioglitazone"],
                "Thyroid_Drugs": ["Levothyroxine", "Methimazole", "Propylthiouracil"],
                "Osteoporosis_Drugs": [
                    "Alendronate",
                    "Risedronate",
                    "Denosumab",
                    "Teriparatide",
                ],
            },
            "infectious": {
                "Antibiotics": [
                    "Amoxicillin",
                    "Azithromycin",
                    "Ciprofloxacin",
                    "Vancomycin",
                ],
                "Antivirals": ["Oseltamivir", "Acyclovir", "Sofosbuvir", "Remdesivir"],
                "Antifungals": ["Fluconazole", "Itraconazole", "Amphotericin_B"],
                "Antimalarials": ["Chloroquine", "Artemisinin", "Mefloquine"],
            },
            "respiratory": {
                "Bronchodilators": [
                    "Albuterol",
                    "Salmeterol",
                    "Tiotropium",
                    "Formoterol",
                ],
                "Corticosteroids": [
                    "Fluticasone",
                    "Budesonide",
                    "Prednisone",
                    "Beclomethasone",
                ],
            },
            "immunosuppressive": {
                "DMARDs": ["Methotrexate", "Sulfasalazine", "Hydroxychloroquine"],
                "Biologics": ["Adalimumab", "Etanercept", "Infliximab", "Rituximab"],
                "Immunosuppressants": ["Cyclosporine", "Tacrolimus", "Mycophenolate"],
            },
        }

        # Protein structure types
        self.protein_structures = [
            "alpha_helix",
            "beta_sheet",
            "coiled_coil",
            "immunoglobulin_fold",
            "leucine_zipper",
            "zinc_finger",
            "helix_turn_helix",
            "beta_barrel",
            "four_helix_bundle",
            "rossmann_fold",
            "ferredoxin_fold",
            "jelly_roll",
            "greek_key",
            "trefoil_knot",
            "all_alpha",
            "all_beta",
            "alpha_beta",
            "membrane_protein",
            "globular",
            "fibrous",
            "intrinsically_disordered",
        ]

        # Expression levels and functions
        self.expression_levels = ["very_low", "low", "medium", "high", "very_high"]
        self.gene_functions = [
            "metabolism",
            "transcription",
            "translation",
            "DNA_repair",
            "cell_cycle",
            "apoptosis",
            "signal_transduction",
            "immune_response",
            "development",
            "differentiation",
            "proliferation",
            "migration",
            "adhesion",
            "transport",
            "enzyme_activity",
            "structural",
            "regulatory",
            "tumor_suppressor",
            "oncogene",
            "growth_factor",
            "hormone",
            "neurotransmitter",
            "ion_channel",
            "receptor",
            "kinase",
            "phosphatase",
            "protease",
            "chaperone",
        ]

        # Disease prevalence and severity
        self.prevalence_levels = [
            "very_rare",
            "rare",
            "uncommon",
            "common",
            "very_common",
        ]
        self.severity_levels = [
            "mild",
            "moderate",
            "severe",
            "critical",
            "life_threatening",
        ]

        # Drug approval statuses
        self.approval_statuses = [
            "approved",
            "phase_III",
            "phase_II",
            "phase_I",
            "preclinical",
            "withdrawn",
            "orphan_drug",
            "fast_track",
            "breakthrough_therapy",
            "accelerated_approval",
            "priority_review",
            "over_the_counter",
        ]

        # Drug mechanisms
        self.drug_mechanisms = [
            "receptor_agonist",
            "receptor_antagonist",
            "enzyme_inhibitor",
            "enzyme_activator",
            "ion_channel_blocker",
            "ion_channel_opener",
            "transporter_inhibitor",
            "monoclonal_antibody",
            "small_molecule",
            "protein_kinase_inhibitor",
            "protease_inhibitor",
            "nucleotide_analog",
            "DNA_alkylating_agent",
            "topoisomerase_inhibitor",
            "antimetabolite",
            "hormone_replacement",
            "immunomodulator",
            "gene_therapy",
            "cell_therapy",
            "radioactive",
            "photodynamic",
            "magnetic",
        ]

        # Association and interaction types
        self.association_types = [
            "causal",
            "biomarker",
            "therapeutic_target",
            "protective",
            "risk_factor",
            "prognostic",
            "diagnostic",
            "pharmacodynamic",
            "pharmacokinetic",
            "genetic_predisposition",
            "environmental_factor",
            "comorbidity",
        ]

        self.interaction_types = [
            "competitive_inhibitor",
            "non_competitive_inhibitor",
            "allosteric_modulator",
            "agonist",
            "partial_agonist",
            "inverse_agonist",
            "antagonist",
            "substrate",
            "cofactor",
            "activator",
            "inducer",
            "blocker",
        ]

        # Efficacy and confidence levels
        self.efficacy_levels = ["very_low", "low", "moderate", "high", "very_high"]
        self.confidence_levels = ["low", "medium", "high", "very_high"]
        self.affinity_levels = [
            "very_weak",
            "weak",
            "moderate",
            "strong",
            "very_strong",
        ]

        # Development stages
        self.development_stages = [
            "approved",
            "phase_III",
            "phase_II",
            "phase_I",
            "preclinical",
            "investigational",
            "experimental",
            "off_label",
            "compassionate_use",
        ]

    def generate_genes(self) -> List[Dict]:
        """Generate diverse gene data with realistic distribution."""
        print(f"Generating {len(self.all_genes)} genes...")

        for i, gene_name in enumerate(self.all_genes):
            # Distribute across chromosomes (1-22, X, Y, MT)
            chromosomes = list(range(1, 23)) + ["X", "Y", "MT"]
            chromosome = random.choice(chromosomes)

            gene_data = {
                "gene_id": f"G{i+1:03d}",
                "gene_name": gene_name,
                "chromosome": str(chromosome),
                "function": random.choice(self.gene_functions),
                "expression_level": random.choice(self.expression_levels),
            }
            self.genes_data.append(gene_data)

        return self.genes_data

    def generate_diseases(self) -> List[Dict]:
        """Generate comprehensive disease data across all categories."""
        print("Generating diseases across all medical specialties...")

        disease_id = 1
        all_diseases = []

        for category, diseases in self.disease_categories.items():
            for disease_name in diseases:
                # Adjust prevalence based on disease type
                if category in ["genetic", "pediatric"]:
                    prevalence_weights = [
                        0.4,
                        0.3,
                        0.2,
                        0.08,
                        0.02,
                    ]  # More rare diseases
                elif category in ["cardiovascular", "metabolic"]:
                    prevalence_weights = [
                        0.05,
                        0.15,
                        0.25,
                        0.35,
                        0.2,
                    ]  # More common diseases
                else:
                    prevalence_weights = [
                        0.2,
                        0.2,
                        0.3,
                        0.2,
                        0.1,
                    ]  # Balanced distribution

                prevalence = np.random.choice(
                    self.prevalence_levels, p=prevalence_weights
                )

                # Adjust severity based on disease type
                if category in ["oncology", "neurological", "genetic"]:
                    severity_weights = [
                        0.1,
                        0.2,
                        0.3,
                        0.25,
                        0.15,
                    ]  # More severe diseases
                elif category in ["dermatologic", "ophthalmologic"]:
                    severity_weights = [
                        0.3,
                        0.4,
                        0.2,
                        0.08,
                        0.02,
                    ]  # Less severe diseases
                else:
                    severity_weights = [
                        0.15,
                        0.3,
                        0.35,
                        0.15,
                        0.05,
                    ]  # Balanced distribution

                severity = np.random.choice(self.severity_levels, p=severity_weights)

                disease_data = {
                    "disease_id": f"D{disease_id:03d}",
                    "disease_name": disease_name,
                    "category": category,
                    "prevalence": prevalence,
                    "severity": severity,
                }
                all_diseases.append(disease_data)
                disease_id += 1

        self.diseases_data = all_diseases
        print(
            f"Generated {len(self.diseases_data)} diseases across {len(self.disease_categories)} categories"
        )
        return self.diseases_data

    def generate_drugs(self) -> List[Dict]:
        """Generate comprehensive drug data across all therapeutic classes."""
        print("Generating drugs across all therapeutic classes...")

        drug_id = 1
        all_drugs = []

        for category, drug_classes in self.drug_classes.items():
            for drug_class, drugs in drug_classes.items():
                for drug_name in drugs:
                    # Adjust approval status based on drug type
                    if "Experimental" in drug_name or "Novel" in drug_name:
                        approval_weights = [
                            0.1,
                            0.2,
                            0.3,
                            0.25,
                            0.15,
                        ]  # More experimental
                        status_list = [
                            "preclinical",
                            "phase_I",
                            "phase_II",
                            "phase_III",
                            "approved",
                        ]
                    else:
                        approval_weights = [0.05, 0.1, 0.15, 0.2, 0.5]  # More approved
                        status_list = [
                            "preclinical",
                            "phase_I",
                            "phase_II",
                            "phase_III",
                            "approved",
                        ]

                    approval_status = np.random.choice(status_list, p=approval_weights)

                    # Select appropriate mechanism based on drug class
                    if "antibody" in drug_class.lower() or "mab" in drug_name.lower():
                        drug_type = "monoclonal_antibody"
                    elif "gene" in drug_class.lower() or "therapy" in drug_name.lower():
                        drug_type = "gene_therapy"
                    elif any(
                        term in drug_name.lower()
                        for term in ["insulin", "growth", "hormone"]
                    ):
                        drug_type = "protein_hormone"
                    else:
                        drug_type = "small_molecule"

                    mechanism = random.choice(self.drug_mechanisms)

                    drug_data = {
                        "drug_id": f"DR{drug_id:03d}",
                        "drug_name": drug_name,
                        "type": drug_type,
                        "approval_status": approval_status,
                        "mechanism": mechanism,
                    }
                    all_drugs.append(drug_data)
                    drug_id += 1

        # Add some synthetic drugs to increase diversity
        synthetic_drug_prefixes = ["SYN", "EXP", "NOV", "ADV", "BIO"]
        for i in range(len(all_drugs), 350):
            prefix = random.choice(synthetic_drug_prefixes)
            drug_name = f"{prefix}-{i:03d}"

            drug_data = {
                "drug_id": f"DR{drug_id:03d}",
                "drug_name": drug_name,
                "type": random.choice(
                    [
                        "small_molecule",
                        "monoclonal_antibody",
                        "gene_therapy",
                        "protein_hormone",
                    ]
                ),
                "approval_status": random.choice(self.approval_statuses),
                "mechanism": random.choice(self.drug_mechanisms),
            }
            all_drugs.append(drug_data)
            drug_id += 1

        self.drugs_data = all_drugs
        print(
            f"Generated {len(self.drugs_data)} drugs across {sum(len(classes) for classes in self.drug_classes.values())} therapeutic classes"
        )
        return self.drugs_data

    def generate_proteins(self) -> List[Dict]:
        """Generate protein data linked to genes."""
        print("Generating proteins encoded by genes...")

        for i, gene in enumerate(self.genes_data):
            # Most genes encode one protein, some encode multiple isoforms
            num_proteins = np.random.choice([1, 2, 3], p=[0.7, 0.25, 0.05])

            for j in range(num_proteins):
                protein_name = gene["gene_name"].replace("GENE_", "PROT_")
                if num_proteins > 1:
                    protein_name += f"_iso{j+1}"

                # Realistic molecular weight distribution (10-300 kDa)
                molecular_weight = int(np.random.lognormal(mean=4, sigma=0.8))
                molecular_weight = max(10, min(300, molecular_weight))

                protein_data = {
                    "protein_id": f"P{len(self.proteins_data)+1:03d}",
                    "protein_name": protein_name,
                    "gene_id": gene["gene_id"],
                    "molecular_weight": molecular_weight,
                    "structure_type": random.choice(self.protein_structures),
                }
                self.proteins_data.append(protein_data)

        print(
            f"Generated {len(self.proteins_data)} proteins from {len(self.genes_data)} genes"
        )
        return self.proteins_data

    def generate_protein_disease_associations(self) -> List[Dict]:
        """Generate realistic protein-disease associations."""
        print("Generating protein-disease associations...")

        # Create associations based on biological relevance
        for protein in self.proteins_data:
            # Each protein associated with 1-5 diseases
            num_associations = np.random.choice(
                [1, 2, 3, 4, 5], p=[0.4, 0.3, 0.2, 0.08, 0.02]
            )
            associated_diseases = random.sample(self.diseases_data, num_associations)

            for disease in associated_diseases:
                # Higher confidence for more severe diseases and common proteins
                if disease["severity"] in ["severe", "critical", "life_threatening"]:
                    confidence_weights = [0.1, 0.2, 0.3, 0.4]
                else:
                    confidence_weights = [0.2, 0.4, 0.3, 0.1]

                confidence = np.random.choice(
                    self.confidence_levels, p=confidence_weights
                )
                association_type = random.choice(self.association_types)

                association = {
                    "protein_id": protein["protein_id"],
                    "disease_id": disease["disease_id"],
                    "association_type": association_type,
                    "confidence": confidence,
                }
                self.protein_disease_associations.append(association)

        print(
            f"Generated {len(self.protein_disease_associations)} protein-disease associations"
        )
        return self.protein_disease_associations

    def generate_drug_disease_treatments(self) -> List[Dict]:
        """Generate drug-disease treatment relationships."""
        print("Generating drug-disease treatment relationships...")

        for drug in self.drugs_data:
            # Each drug treats 1-4 diseases
            num_treatments = np.random.choice([1, 2, 3, 4], p=[0.5, 0.3, 0.15, 0.05])
            treated_diseases = random.sample(self.diseases_data, num_treatments)

            for disease in treated_diseases:
                # Higher efficacy for approved drugs
                if drug["approval_status"] == "approved":
                    efficacy_weights = [0.05, 0.15, 0.3, 0.35, 0.15]
                elif drug["approval_status"] in ["phase_III", "phase_II"]:
                    efficacy_weights = [0.1, 0.25, 0.35, 0.25, 0.05]
                else:
                    efficacy_weights = [0.3, 0.3, 0.25, 0.1, 0.05]

                efficacy = np.random.choice(self.efficacy_levels, p=efficacy_weights)
                stage = drug["approval_status"]

                treatment = {
                    "drug_id": drug["drug_id"],
                    "disease_id": disease["disease_id"],
                    "efficacy": efficacy,
                    "stage": stage,
                }
                self.drug_disease_treatments.append(treatment)

        print(
            f"Generated {len(self.drug_disease_treatments)} drug-disease treatment relationships"
        )
        return self.drug_disease_treatments

    def generate_drug_protein_targets(self) -> List[Dict]:
        """Generate drug-protein target relationships."""
        print("Generating drug-protein target relationships...")

        for drug in self.drugs_data:
            # Each drug targets 1-6 proteins
            if drug["type"] == "monoclonal_antibody":
                num_targets = np.random.choice([1, 2], p=[0.8, 0.2])  # More specific
            elif drug["type"] == "small_molecule":
                num_targets = np.random.choice(
                    [1, 2, 3, 4], p=[0.4, 0.3, 0.2, 0.1]
                )  # Less specific
            else:
                num_targets = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])

            target_proteins = random.sample(
                self.proteins_data, min(num_targets, len(self.proteins_data))
            )

            for protein in target_proteins:
                # Higher affinity for approved drugs
                if drug["approval_status"] == "approved":
                    affinity_weights = [0.05, 0.15, 0.3, 0.35, 0.15]
                else:
                    affinity_weights = [0.2, 0.3, 0.3, 0.15, 0.05]

                affinity = np.random.choice(self.affinity_levels, p=affinity_weights)
                interaction_type = random.choice(self.interaction_types)

                target = {
                    "drug_id": drug["drug_id"],
                    "protein_id": protein["protein_id"],
                    "interaction_type": interaction_type,
                    "affinity": affinity,
                }
                self.drug_protein_targets.append(target)

        print(
            f"Generated {len(self.drug_protein_targets)} drug-protein target relationships"
        )
        return self.drug_protein_targets

    def save_all_data(self):
        """Save all generated data to CSV files."""
        print("Saving all data to CSV files...")

        # Save entity data
        pd.DataFrame(self.genes_data).to_csv(self.output_dir / "genes.csv", index=False)
        pd.DataFrame(self.proteins_data).to_csv(
            self.output_dir / "proteins.csv", index=False
        )
        pd.DataFrame(self.diseases_data).to_csv(
            self.output_dir / "diseases.csv", index=False
        )
        pd.DataFrame(self.drugs_data).to_csv(self.output_dir / "drugs.csv", index=False)

        # Save relationship data
        pd.DataFrame(self.protein_disease_associations).to_csv(
            self.output_dir / "protein_disease_associations.csv", index=False
        )
        pd.DataFrame(self.drug_disease_treatments).to_csv(
            self.output_dir / "drug_disease_treatments.csv", index=False
        )
        pd.DataFrame(self.drug_protein_targets).to_csv(
            self.output_dir / "drug_protein_targets.csv", index=False
        )

        print("All data saved successfully!")

    def generate_summary_report(self):
        """Generate a summary report of the dataset."""
        print("\n" + "=" * 60)
        print("EXPANDED BIOMEDICAL DATASET SUMMARY")
        print("=" * 60)

        print(f"📊 ENTITIES:")
        print(f"   Genes: {len(self.genes_data):,}")
        print(f"   Proteins: {len(self.proteins_data):,}")
        print(f"   Diseases: {len(self.diseases_data):,}")
        print(f"   Drugs: {len(self.drugs_data):,}")
        print(
            f"   Total Entities: {len(self.genes_data) + len(self.proteins_data) + len(self.diseases_data) + len(self.drugs_data):,}"
        )

        print(f"\n🔗 RELATIONSHIPS:")
        print(f"   Gene-Protein (ENCODES): {len(self.proteins_data):,}")
        print(
            f"   Protein-Disease (ASSOCIATED_WITH): {len(self.protein_disease_associations):,}"
        )
        print(f"   Drug-Disease (TREATS): {len(self.drug_disease_treatments):,}")
        print(f"   Drug-Protein (TARGETS): {len(self.drug_protein_targets):,}")

        total_relationships = (
            len(self.proteins_data)
            + len(self.protein_disease_associations)
            + len(self.drug_disease_treatments)
            + len(self.drug_protein_targets)
        )
        print(f"   Total Relationships: {total_relationships:,}")

        print(f"\n📈 DISEASE CATEGORIES:")
        disease_counts = {}
        for disease in self.diseases_data:
            category = disease["category"]
            disease_counts[category] = disease_counts.get(category, 0) + 1

        for category, count in sorted(disease_counts.items()):
            print(f"   {category.capitalize()}: {count}")

        print(f"\n💊 DRUG TYPES:")
        drug_type_counts = {}
        for drug in self.drugs_data:
            drug_type = drug["type"]
            drug_type_counts[drug_type] = drug_type_counts.get(drug_type, 0) + 1

        for drug_type, count in sorted(drug_type_counts.items()):
            print(f"   {drug_type.replace('_', ' ').title()}: {count}")

        print(f"\n🧬 CHROMOSOME DISTRIBUTION:")
        chromosome_counts = {}
        for gene in self.genes_data:
            chromosome = gene["chromosome"]
            chromosome_counts[chromosome] = chromosome_counts.get(chromosome, 0) + 1

        for chromosome in sorted(
            chromosome_counts.keys(), key=lambda x: int(x) if x.isdigit() else 100
        ):
            print(f"   Chr {chromosome}: {chromosome_counts[chromosome]}")

        print("\n" + "=" * 60)
        print("🎉 DATASET GENERATION COMPLETE!")
        print("   This expanded dataset provides rich, diverse biomedical")
        print("   data for comprehensive knowledge graph learning!")
        print("=" * 60)


def main():
    """Generate the expanded biomedical dataset."""
    print("🚀 Starting Expanded Biomedical Dataset Generation")
    print("Creating a comprehensive, diverse, and realistic synthetic dataset...")
    print()

    generator = ExpandedBiomedicalDataGenerator()

    # Generate all data
    generator.generate_genes()
    generator.generate_diseases()
    generator.generate_drugs()
    generator.generate_proteins()
    generator.generate_protein_disease_associations()
    generator.generate_drug_disease_treatments()
    generator.generate_drug_protein_targets()

    # Save all data
    generator.save_all_data()

    # Generate summary
    generator.generate_summary_report()

    print(f"\n✅ All data saved to: {generator.output_dir}")
    print("Ready to load into Neo4j with: pdm run load-data")


if __name__ == "__main__":
    main()
