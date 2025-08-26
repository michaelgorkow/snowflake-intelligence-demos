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

## 📋 Dataset Statistics

- **Patients**: 1,000 de-identified patient records
- **Drugs**: 20 pharmaceutical compounds across 5 therapeutic areas
- **Sites**: 50 clinical trial sites worldwide
- **Trials**: 15 clinical trials across 3 phases
- **Results**: 1,621 individual patient outcome records

# Example Use Cases for different Personas

This section demonstrates how different stakeholders in a biotech organization can leverage the text-to-SQL agent to extract actionable insights from clinical trial data. Each persona represents a typical role with specific analytical needs and decision-making requirements.

## 🧑‍⚕️ Persona 1: Clinical Trial Manager - Sarah Chen

**Role & Responsibilities:**
Sarah manages multiple clinical trials across different therapeutic areas. She's responsible for trial operations, site performance monitoring, patient enrollment tracking, and ensuring studies stay on timeline and budget.

**Key Insights Needed:**
- Site performance and selection optimization
- Patient enrollment efficiency and demographics
- Trial timeline and milestone tracking
- Resource allocation and capacity planning

**Complex Analysis Examples:**

### 1. **Comprehensive Site Performance Investigation**
**Initial Question:** *"Which clinical sites are underperforming across multiple metrics, and what should be our action plan?"*

**Follow-up Analysis:**
- *"For sites with high adverse event rates, what's the relationship between investigator count, certification level, and patient safety outcomes?"*
- *"Among underperforming sites, which therapeutic areas show the biggest gaps in patient compliance and treatment success?"*
- *"What's the cost-effectiveness of Level 3 certified sites versus lower levels when factoring in enrollment rates, compliance, and outcomes?"*

**Required Data:**
- **FACT_TRIAL_RESULTS**: Adverse events, compliance rates, treatment outcomes, visit dates
- **DIM_SITES**: Site certification levels, investigator counts, site types, geographic locations
- **DIM_DRUGS**: Development costs for cost-effectiveness analysis
- **DIM_TRIALS**: Trial phases and status for context
- **DIM_PATIENTS**: Demographics for stratification analysis

### 2. **Strategic Enrollment Optimization Across Therapeutic Areas**
**Initial Question:** *"Our oncology and cardiology programs are struggling with enrollment. What demographic and operational factors should we prioritize to improve recruitment efficiency?"*

**Follow-up Analysis:**
- *"In countries where we have multiple sites, which site characteristics predict faster enrollment and better retention?"*
- *"For our target demographics (age 50-70, specific ethnicities), which geographic regions show the highest treatment success rates?"*
- *"What's the optimal mix of Hospital vs Research Institute vs Private Clinic sites for different therapeutic areas based on enrollment velocity and patient outcomes?"*

**Required Data:**
- **DIM_PATIENTS**: Age, gender, ethnicity, country, enrollment dates for demographic analysis
- **DIM_SITES**: Site types, countries, investigator counts for operational optimization
- **FACT_TRIAL_RESULTS**: Treatment outcomes, compliance rates, treatment duration for retention analysis
- **DIM_DRUGS**: Drug categories (Oncology, Cardiology) and development costs
- **DIM_TRIALS**: Planned vs actual enrollment, trial phases, start/end dates

---

## 🔬 Persona 2: Drug Development Scientist - Dr. Michael Rodriguez

**Role & Responsibilities:**
Dr. Rodriguez leads drug development programs and is responsible for evaluating drug efficacy, optimizing dosing strategies, understanding mechanism of action performance, and making go/no-go decisions for advancing compounds through development phases.

**Key Insights Needed:**
- Drug efficacy and safety profiles
- Mechanism of action performance comparison
- Dose-response relationships
- Biomarker and endpoint analysis

**Complex Analysis Examples:**

### 1. **Mechanism-Indication Optimization for Portfolio Prioritization**
**Initial Question:** *"Which drug mechanism and indication combinations show the strongest risk-adjusted potential for our Phase III advancement decisions?"*

**Follow-up Analysis:**
- *"For Gene Therapy mechanisms showing promise, how do patient demographics and baseline characteristics affect treatment response across different indications?"*
- *"Among our diabetes indication drugs, what's the relationship between drug mechanism (Small Molecule vs Monoclonal Antibody vs Protein), treatment duration, and sustained efficacy?"*
- *"Which high-development-cost drugs (>$300M) are justified by their efficacy profiles, and which should be reconsidered?"*

**Required Data:**
- **DIM_DRUGS**: Drug mechanisms, therapeutic categories, indications, development costs
- **FACT_TRIAL_RESULTS**: Baseline/endpoint scores, improvement scores, treatment duration, outcomes
- **DIM_PATIENTS**: Age, BMI, demographics for subgroup efficacy analysis
- **DIM_TRIALS**: Trial phases for progression analysis
- **DIM_SITES**: Geographic distribution for global efficacy patterns

### 2. **Safety-Efficacy Profile Deep Dive for Regulatory Strategy**
**Initial Question:** *"Our monoclonal antibody portfolio is approaching Phase III. What's the comprehensive safety-efficacy profile across patient subpopulations that will strengthen our regulatory submissions?"*

**Follow-up Analysis:**
- *"For patients with high BMI (>30) and age >65, how do adverse event rates correlate with treatment compliance and efficacy outcomes across our monoclonal antibody drugs?"*
- *"Which monoclonal antibodies show differential response patterns by ethnicity, and what are the implications for global registration strategies?"*
- *"Among treatment arms vs controls, what's the therapeutic window analysis showing optimal efficacy with acceptable safety margins?"*

**Required Data:**
- **DIM_DRUGS**: Drug mechanisms (filter for Monoclonal Antibodies), therapeutic categories
- **FACT_TRIAL_RESULTS**: Adverse events, serious adverse events, compliance rates, improvement scores, treatment arms
- **DIM_PATIENTS**: Age, BMI, ethnicity, gender for subpopulation analysis
- **DIM_TRIALS**: Trial phases, primary endpoints for regulatory context
- **DIM_SITES**: Countries for global regulatory strategy

---

## 📋 Persona 3: Regulatory Affairs Manager - Jennifer Wu

**Role & Responsibilities:**
Jennifer ensures clinical trials comply with regulatory requirements, manages safety reporting obligations, prepares regulatory submissions, and monitors safety signals across the development portfolio.

**Key Insights Needed:**
- Safety signal detection and analysis
- Regulatory compliance monitoring
- Adverse event trending and reporting
- Patient safety profiles by demographics

**Complex Analysis Examples:**

### 1. **Multi-Dimensional Safety Signal Investigation**
**Initial Question:** *"We've received queries from regulators about potential safety signals in our neurology portfolio. What's the comprehensive safety profile analysis we need for our response?"*

**Follow-up Analysis:**
- *"For our Gene Therapy neurology drugs, what's the relationship between treatment duration, patient age/BMI, and serious adverse event patterns across different countries?"*
- *"Among patients who experienced serious adverse events, what demographic and baseline characteristics predict higher risk, and how does this vary by investigational site certification level?"*
- *"What's the comparative safety analysis between our Alzheimer's indication drugs and diabetes indication drugs within the neurology therapeutic area?"*

**Required Data:**
- **DIM_DRUGS**: Drug categories (filter Neurology), mechanisms, indications (Alzheimer's, Diabetes)
- **FACT_TRIAL_RESULTS**: Adverse events, serious adverse events, treatment duration, baseline scores, compliance rates
- **DIM_PATIENTS**: Age, BMI, gender, ethnicity, countries for demographic risk profiling
- **DIM_SITES**: Site certification levels, countries for institutional risk factors
- **DIM_TRIALS**: Trial phases, primary endpoints, sponsors for regulatory context

### 2. **Regulatory Submission Safety Dossier Preparation**
**Initial Question:** *"For our lead Phase III drug approaching FDA submission, what's the comprehensive patient exposure and safety database that demonstrates acceptable benefit-risk profile?"*

**Follow-up Analysis:**
- *"What's the exposure-adjusted adverse event rate analysis showing safety margins across different treatment arms and patient subpopulations?"*
- *"For patients with treatment duration >180 days, how do safety profiles compare between high-compliance (>90%) and lower-compliance cohorts?"*
- *"Which demographic subgroups show differential safety patterns that require special labeling considerations or post-market surveillance?"*

**Required Data:**
- **FACT_TRIAL_RESULTS**: Treatment duration (exposure calculation), adverse events, serious adverse events, compliance rates, treatment arms, outcomes
- **DIM_PATIENTS**: Complete demographic profile for subgroup safety analysis
- **DIM_TRIALS**: Phase III trials, primary endpoints, completion status
- **DIM_DRUGS**: Development costs and mechanisms for benefit-risk contextualization
- **DIM_SITES**: Geographic distribution for global safety profile

---

## 💼 Persona 4: Business Development Executive - David Kim

**Role & Responsibilities:**
David evaluates the commercial potential of the drug pipeline, makes investment decisions, manages R&D portfolio priorities, and provides strategic guidance on which programs to advance, partner, or discontinue.

**Key Insights Needed:**
- Portfolio ROI and investment analysis
- Pipeline risk assessment
- Market opportunity evaluation
- Partnership and licensing opportunities

**Complex Analysis Examples:**

### 1. **Strategic Portfolio Optimization and Investment Prioritization**
**Initial Question:** *"Given our current burn rate and upcoming funding round, which combination of therapeutic areas and drug mechanisms offers the optimal risk-adjusted returns for our next 18-month investment cycle?"*

**Follow-up Analysis:**
- *"For drugs with development costs >$200M, what's the probability-weighted return analysis based on current Phase II/III success rates, patient population sizes, and time-to-market projections?"*
- *"Among our Gene Therapy and Monoclonal Antibody portfolios, which indication-mechanism combinations show the strongest competitive differentiation based on efficacy improvement scores and safety profiles?"*
- *"What's the geographic market potential analysis for our successful Phase III programs, considering enrollment patterns, regulatory approval timelines, and regional safety profiles?"*

**Required Data:**
- **DIM_DRUGS**: Development costs, therapeutic categories, mechanisms, indications for portfolio analysis
- **FACT_TRIAL_RESULTS**: Success rates, improvement scores, patient counts for efficacy assessment
- **DIM_TRIALS**: Trial phases, status, planned enrollment, start/end dates for timeline analysis
- **DIM_PATIENTS**: Geographic distribution, demographics for market sizing
- **DIM_SITES**: Countries, site types for global market entry strategy

### 2. **Partnership and Licensing Opportunity Evaluation**
**Initial Question:** *"Our board wants to evaluate potential out-licensing opportunities for non-core assets. Which programs in our portfolio have the strongest value proposition for pharmaceutical partners?"*

**Follow-up Analysis:**
- *"For our completed Phase II trials in Cardiology and Endocrinology, what's the licensing valuation framework based on patient exposure data, safety margins, and efficacy benchmarks?"*
- *"Which of our drugs show differentiated performance in specific demographic subgroups (age, ethnicity, BMI) that could command premium licensing terms in targeted geographic markets?"*
- *"Among our high-development-cost programs, which ones show sufficient clinical de-risking to warrant co-development partnerships vs full out-licensing?"*

**Required Data:**
- **DIM_DRUGS**: Development costs, therapeutic categories (Cardiology, Endocrinology), mechanisms for valuation
- **FACT_TRIAL_RESULTS**: Treatment outcomes, adverse events, improvement scores, compliance rates for clinical de-risking
- **DIM_PATIENTS**: Age, ethnicity, BMI for demographic differentiation analysis
- **DIM_TRIALS**: Phase II completion status, trial sponsors for partnership benchmarking
- **DIM_SITES**: Geographic coverage and certification levels for global partnership appeal

---

## 🎯 Cross-Functional Insights

**Multi-Persona Complex Analysis:**
These advanced scenarios demonstrate how the same rich dataset supports sophisticated decision-making across different organizational functions:

### **Integrated Portfolio Risk Assessment**
*"Our Phase III oncology drug GammaTreat is approaching regulatory submission, but we're seeing mixed signals. What's the comprehensive risk-benefit analysis across operational, clinical, regulatory, and commercial dimensions?"*

**Multi-Dimensional Analysis Requires:**
- **Clinical Trial Manager**: Site performance optimization, enrollment efficiency, operational risk factors
- **Drug Development Scientist**: Mechanism-specific efficacy patterns, safety-efficacy correlations, dose-response relationships
- **Regulatory Affairs Manager**: Safety database adequacy, subpopulation risk profiles, exposure-adjusted event rates
- **Business Development Executive**: ROI projections, competitive positioning, licensing valuation scenarios

**Required Data Integration:**
- **FACT_TRIAL_RESULTS**: Complete efficacy, safety, compliance, and outcome data across all dimensions
- **DIM_DRUGS**: Development costs, mechanism, indication for commercial and clinical context
- **DIM_PATIENTS**: Full demographic profiles for subgroup analysis and market segmentation
- **DIM_SITES**: Geographic and operational metrics for global strategy
- **DIM_TRIALS**: Phase progression, timelines, and regulatory milestones

### **Strategic Geographic Expansion Decision**
*"We're considering expanding our diabetes drug program into Asian markets. What's the integrated analysis framework for operational feasibility, clinical differentiation, regulatory strategy, and commercial opportunity?"*

**Cross-Functional Requirements:**
- Geographic site performance and certification analysis
- Ethnicity-specific efficacy and safety profiles
- Regulatory precedent analysis in target markets
- Cost-effectiveness and market potential evaluation

This sophisticated analytical approach enables evidence-based strategic decision making across the entire clinical development organization, leveraging the full depth of clinical trial data for competitive advantage.
