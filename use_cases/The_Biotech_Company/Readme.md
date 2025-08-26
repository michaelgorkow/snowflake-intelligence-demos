# The Biotech Company - Clinical Trial Analytics Dataset

![BIOTECH](resources/biotech.png)

## Overview

This dataset demonstrates a realistic pharmaceutical clinical trial data model designed to showcase Snowflake's text-to-SQL agent capabilities for biotech and pharmaceutical organizations. The dataset contains synthetic but realistic data representing clinical trials, patient demographics, drug information, trial sites, and comprehensive trial results.

The data follows a **star schema** design optimized for analytical queries, making it perfect for demonstrating how AI agents can help pharmaceutical professionals extract insights from complex clinical trial data using natural language queries.

## Dataset Structure

The dataset consists of **5 interconnected tables** following a star schema pattern:
- **4 Dimension Tables**: Patient demographics, drug information, trial sites, and trial metadata
- **1 Fact Table**: Detailed trial results connecting all dimensions

## Data Model

The biotech dataset follows a **star schema** design with `FACT_TRIAL_RESULTS` as the central fact table connected to four dimension tables:

```
                      ┌──────────────────────────────┐
                      │        DIM_PATIENTS          │
                      │                              │
                      │ • PATIENT_ID (PK)            │
                      │ • AGE                        │
                      │ • GENDER                     │
                      │ • ETHNICITY                  │
                      │ • BMI                        │
                      │ • COUNTRY                    │
                      │ • ENROLLMENT_DATE            │
                      └──────────────┬───────────────┘
                                     │
                                     │
         ┌─────────────────────────┐ │ ┌─────────────────────────┐
         │       DIM_DRUGS         │ │ │       DIM_SITES         │
         │                         │ │ │                         │
         │ • DRUG_ID (PK)          │ │ │ • SITE_ID (PK)          │
         │ • DRUG_NAME             │ │ │ • SITE_NAME             │
         │ • CATEGORY              │ │ │ • CITY                  │
         │ • MECHANISM             │ │ │ • COUNTRY               │
         │ • INDICATION            │ │ │ • SITE_TYPE             │
         │ • DOSAGE_FORM           │ │ │ • INVESTIGATOR_COUNT    │
         │ • DEVELOPMENT_COST_USD  │ │ │ • CERTIFICATION_LEVEL   │
         └─────────────┬───────────┘ │ └─────────────┬───────────┘
                       │             │               │
                       │             │               │
                       └─────────────┼───────────────┘
                                     │
                    ┌────────────────▼─────────────────┐
                    │        FACT_TRIAL_RESULTS        │
                    │                                  │
                    │ • RESULT_ID                      │
                    │ • TRIAL_ID (FK)                  │
                    │ • PATIENT_ID (FK)                │
                    │ • DRUG_ID (FK)                   │
                    │ • SITE_ID (FK)                   │
                    │ • TREATMENT_ARM                  │
                    │ • BASELINE_SCORE                 │
                    │ • ENDPOINT_SCORE                 │
                    │ • IMPROVEMENT                    │
                    │ • ADVERSE_EVENTS                 │
                    │ • SERIOUS_ADVERSE_EVENTS         │
                    │ • TREATMENT_DURATION_DAYS        │
                    │ • COMPLIANCE_RATE                │
                    │ • OUTCOME                        │
                    │ • VISIT_DATE                     │
                    └─────────────────┬────────────────┘
                                      │
                                      │
                    ┌─────────────────▼────────────────┐
                    │        DIM_TRIALS                │
                    │                                  │
                    │ • TRIAL_ID (PK)                  │
                    │ • TRIAL_NAME                     │
                    │ • PHASE                          │
                    │ • STATUS                         │
                    │ • PRIMARY_ENDPOINT               │
                    │ • START_DATE                     │
                    │ • END_DATE                       │
                    │ • PLANNED_ENROLLMENT             │
                    │ • SPONSOR                        │
                    └──────────────────────────────────┘
```

### Key Relationships

| Relationship | Description |
|--------------|-------------|
| **TRIAL_PATIENTS** | `FACT_TRIAL_RESULTS.PATIENT_ID` → `DIM_PATIENTS.PATIENT_ID` |
| **TRIAL_DRUGS** | `FACT_TRIAL_RESULTS.DRUG_ID` → `DIM_DRUGS.DRUG_ID` |
| **TRIAL_SITES** | `FACT_TRIAL_RESULTS.SITE_ID` → `DIM_SITES.SITE_ID` |
| **TRIAL_STUDIES** | `FACT_TRIAL_RESULTS.TRIAL_ID` → `DIM_TRIALS.TRIAL_ID` |

### Data Flow

```
Patient Demographics + Drug Information + Site Details + Trial Metadata
                                ↓
                      FACT_TRIAL_RESULTS
                                ↓
           Clinical Outcomes + Safety Data + Efficacy Measures
```

This star schema design enables:
- **Fast analytical queries** across multiple dimensions
- **Simplified joins** for complex business questions
- **Scalable data architecture** for growing clinical trial datasets
- **Optimized performance** for text-to-SQL AI agents

### 📊 Table Schemas

#### **DIM_PATIENTS** - Patient Demographics
Contains de-identified patient information for clinical trial participants.

| Column | Type | Description |
|--------|------|-------------|
| `PATIENT_ID` | String | Unique patient identifier (PAT_0001, PAT_0002, ...) |
| `AGE` | Integer | Patient age (18-85 years) |
| `GENDER` | String | Patient gender (Male, Female) |
| `ETHNICITY` | String | Patient ethnicity (Caucasian, Hispanic, African American, Asian, Other) |
| `BMI` | Float | Body Mass Index (18.5-40.0) |
| `COUNTRY` | String | Patient's country of residence |
| `ENROLLMENT_DATE` | Date | Date when patient enrolled in trials |

**Sample Data:**
```
PATIENT_ID  AGE  GENDER  ETHNICITY        BMI   COUNTRY        ENROLLMENT_DATE
PAT_0001    32   Male    African American 23.8  Czech Republic 2025-05-10
PAT_0002    35   Male    Other           20.4  Swaziland      2023-11-21
```

#### **DIM_DRUGS** - Drug Information Catalog
Master catalog of pharmaceutical compounds in development and testing.

| Column | Type | Description |
|--------|------|-------------|
| `DRUG_ID` | String | Unique drug identifier (DRG_001, DRG_002, ...) |
| `DRUG_NAME` | String | Commercial drug name (AlphaCure, BetaHeal, etc.) |
| `CATEGORY` | String | Therapeutic area (Oncology, Cardiology, Neurology, Immunology, Endocrinology) |
| `MECHANISM` | String | Drug mechanism type (Small Molecule, Monoclonal Antibody, Protein, Gene Therapy) |
| `INDICATION` | String | Target medical condition (Cancer, Heart Disease, Alzheimer's, Diabetes, Arthritis) |
| `DOSAGE_FORM` | String | Administration method (Tablet, Injection, Capsule, IV Infusion) |
| `DEVELOPMENT_COST_USD` | Integer | Total development cost in USD ($50M - $500M) |

**Sample Data:**
```
DRUG_ID  DRUG_NAME   CATEGORY   MECHANISM            INDICATION  DOSAGE_FORM  DEVELOPMENT_COST_USD
DRG_001  AlphaCure   Neurology  Monoclonal Antibody  Diabetes    Injection    136,411,714
DRG_002  BetaHeal    Cardiology Monoclonal Antibody  Arthritis   Capsule      154,328,094
```

#### **DIM_SITES** - Clinical Trial Sites
Information about clinical research facilities conducting trials.

| Column | Type | Description |
|--------|------|-------------|
| `SITE_ID` | String | Unique site identifier (SITE_001, SITE_002, ...) |
| `SITE_NAME` | String | Clinical site name (e.g., "New York Medical Center") |
| `CITY` | String | Site location city |
| `COUNTRY` | String | Site location country |
| `SITE_TYPE` | String | Facility type (Hospital, Research Institute, Private Clinic) |
| `INVESTIGATOR_COUNT` | Integer | Number of investigators at site (5-25) |
| `CERTIFICATION_LEVEL` | String | Site certification (Level 1, Level 2, Level 3) |

#### **DIM_TRIALS** - Clinical Trial Metadata
Information about clinical trials including phases, timelines, and study design.

| Column | Type | Description |
|--------|------|-------------|
| `TRIAL_ID` | String | Unique trial identifier (TRL_001, TRL_002, ...) |
| `TRIAL_NAME` | String | Study name (e.g., "Clinical Study 1") |
| `PHASE` | String | Clinical trial phase (Phase I, Phase II, Phase III) |
| `STATUS` | String | Current trial status (Completed, Ongoing, Terminated, Suspended) |
| `PRIMARY_ENDPOINT` | String | Main study objective (Safety, Efficacy, Dosage, Biomarker Response) |
| `START_DATE` | Date | Trial start date |
| `END_DATE` | Date | Trial completion date |
| `PLANNED_ENROLLMENT` | Integer | Target patient enrollment (50-500) |
| `SPONSOR` | String | Trial sponsor organization |

#### **FACT_TRIAL_RESULTS** - Clinical Trial Results (Fact Table)
Comprehensive trial results connecting patients, drugs, sites, and trials with outcome measures.

| Column | Type | Description |
|--------|------|-------------|
| `RESULT_ID` | String | Unique result record identifier |
| `TRIAL_ID` | String | Foreign key to DIM_TRIALS |
| `PATIENT_ID` | String | Foreign key to DIM_PATIENTS |
| `DRUG_ID` | String | Foreign key to DIM_DRUGS |
| `SITE_ID` | String | Foreign key to DIM_SITES |
| `TREATMENT_ARM` | String | Study arm assignment (Treatment, Placebo, Control) |
| `BASELINE_SCORE` | Integer | Patient's pre-treatment score (20-80) |
| `ENDPOINT_SCORE` | Integer | Patient's post-treatment score |
| `IMPROVEMENT` | Integer | Score improvement (endpoint - baseline) |
| `ADVERSE_EVENTS` | Integer | Number of adverse events reported (0-5) |
| `SERIOUS_ADVERSE_EVENTS` | Integer | Number of serious adverse events (0-2) |
| `TREATMENT_DURATION_DAYS` | Integer | Length of treatment in days (30-365) |
| `COMPLIANCE_RATE` | Float | Patient treatment compliance (0.7-1.0) |
| `OUTCOME` | String | Overall treatment outcome (Success, Failure, Partial Response, No Response) |
| `VISIT_DATE` | Date | Date of outcome assessment |

## 🤖 Text-to-SQL Agent Capabilities

This dataset is designed to demonstrate how AI agents can translate natural language questions into SQL queries for pharmaceutical analytics. Here are the types of questions the agent can answer:

### 🎯 Clinical Trial Performance Analysis

**Example Questions:**
- *"What is the average improvement score for each drug category?"*
- *"Which Phase III trials had the highest success rates?"*
- *"Show me the completion rates by trial phase and therapeutic area"*
- *"What percentage of patients showed improvement scores above 20?"*

**Sample Query Generated:**
```sql
SELECT 
    d.CATEGORY,
    AVG(f.IMPROVEMENT) as avg_improvement,
    COUNT(*) as total_patients
FROM FACT_TRIAL_RESULTS f
JOIN DIM_DRUGS d ON f.DRUG_ID = d.DRUG_ID
GROUP BY d.CATEGORY
ORDER BY avg_improvement DESC;
```

### 🏥 Site Performance & Geographic Analysis

**Example Questions:**
- *"Which clinical sites reported the most adverse events?"*
- *"What is the patient enrollment by country and site type?"*
- *"Show me compliance rates by site certification level"*
- *"Which countries have the highest treatment success rates?"*

### 💊 Drug Development Insights

**Example Questions:**
- *"Compare success rates between monoclonal antibodies and small molecules"*
- *"Which drugs had the best safety profile (fewest adverse events)?"*
- *"What's the correlation between development cost and trial success rate?"*
- *"Show me efficacy by indication and dosage form"*

### 👥 Patient Demographics & Outcomes

**Example Questions:**
- *"How do treatment outcomes vary by patient age groups?"*
- *"What's the success rate breakdown by gender and ethnicity?"*
- *"Which BMI ranges show the best treatment response?"*
- *"Show patient compliance patterns by demographic factors"*

### ⚠️ Safety Signal Detection

**Example Questions:**
- *"Identify patients with multiple serious adverse events"*
- *"Which drug-site combinations have elevated safety concerns?"*
- *"Show adverse event patterns by treatment duration"*
- *"Compare safety profiles across different trial phases"*

### 📈 Regulatory & Business Intelligence

**Example Questions:**
- *"What's the average time from trial start to completion by phase?"*
- *"Which sponsors have the highest trial success rates?"*
- *"Show enrollment efficiency by site and therapeutic area"*
- *"Calculate cost per successful patient outcome by drug"*

### 🔍 Complex Multi-Dimensional Analysis

**Example Questions:**
- *"For oncology drugs in Phase II trials, show success rates by site type and patient age group"*
- *"Compare treatment arm performance for diabetes drugs across different BMI categories"*
- *"Which combination of factors (age, gender, BMI) predict the best treatment outcomes?"*

## 📋 Dataset Statistics

- **Patients**: 1,000 de-identified patient records
- **Drugs**: 20 pharmaceutical compounds across 5 therapeutic areas
- **Sites**: 50 clinical trial sites worldwide
- **Trials**: 15 clinical trials across 3 phases
- **Results**: 1,621 individual patient outcome records

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy faker
```

### Generate Fresh Data
```python
from data_generator import generate_biotech_dataset

# Generate new dataset
datasets = generate_biotech_dataset(
    num_patients=1000,
    num_drugs=20,
    num_sites=50,
    num_trials=15,
    output_dir='data/'
)
```

### Load into Snowflake
The generated CSV files can be directly loaded into Snowflake tables using standard data loading procedures. The star schema design ensures optimal query performance for analytical workloads.

## 🎯 Use Cases for Pharmaceutical Organizations

This dataset demonstrates how Snowflake's AI agents can help pharmaceutical companies:

1. **Accelerate Clinical Decision Making** - Natural language queries for rapid trial insights
2. **Enhance Safety Monitoring** - Quick identification of safety signals and adverse event patterns
3. **Optimize Site Selection** - Data-driven decisions for future trial site selection
4. **Improve Patient Stratification** - Identify optimal patient populations for specific treatments
5. **Support Regulatory Submissions** - Generate evidence packages with comprehensive analytics
6. **Enable Competitive Intelligence** - Benchmark performance against industry standards

## 📝 Notes

- All patient data is synthetic and de-identified
- Data follows realistic pharmaceutical industry patterns
- Schema designed for optimal analytical query performance
- Compatible with Snowflake Cortex AI and text-to-SQL agents
- Extensible design allows for additional data dimensions

---

*This dataset is part of the Snowflake Intelligence Demos showcasing AI-powered analytics for the pharmaceutical industry.*

