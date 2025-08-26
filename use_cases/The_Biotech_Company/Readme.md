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

# 📊 Discovery Stories: How Key Insights Were Uncovered

This section demonstrates how different stakeholders in a biotech organization would naturally discover the key insights in the dataset through progressive questioning. Each story shows the realistic analytical journey from initial curiosity to actionable findings.

## 🏥 The Clinical Operations Discovery: "Why Are Our Costs Spiraling?"

**Sarah Chen, Clinical Trial Manager**, starts her Monday morning reviewing the quarterly budget variance report. The numbers don't add up.

**Initial Question:** *"Which of our clinical sites are driving the highest operational costs?"*

The data reveals Level 3 certified sites are consuming 40% more budget than originally planned. But before raising concerns with finance...

**Follow-up Question:** *"Are these Level 3 sites delivering better outcomes to justify the costs?"*

The analysis shows Level 3 sites consistently deliver 20% better patient outcomes and 10% higher compliance rates compared to Level 1 sites.

**Deep Dive Question:** *"What exactly makes Level 3 sites more expensive?"*

The investigation reveals Level 3 sites employ 15-25 investigators compared to 5-12 at Level 1 sites, explaining the cost differential.

**Strategic Question:** *"For which types of trials do Level 3 sites justify their premium?"*

**The Discovery:** Level 3 sites excel at Phase III trials and high-stakes studies where outcome quality is paramount, making their premium costs justifiable for critical milestones.

**Follow-up Investigation:** *"Are there geographic patterns in site performance we should know about?"*

Sarah discovers that Northern European sites (Netherlands, Sweden) show exceptional enrollment efficiency (90-95%) while Japanese sites struggle with enrollment (70%) but deliver superior safety profiles.

**Action Plan:** Prioritize Level 3 sites for Phase III trials and use Northern European sites for challenging enrollments.

---

## 🔬 The Drug Development Revelation: "Why Aren't All Our Mechanisms Working?"

**Dr. Michael Rodriguez, Drug Development Scientist**, is preparing for the monthly portfolio review when he notices concerning patterns in the latest Phase II readouts.

**Initial Question:** *"Which drug mechanisms are showing the strongest efficacy signals across our portfolio?"*

Gene Therapy emerges as the top performer, but with puzzling variability in results across different trial sites.

**Curiosity Question:** *"Why is Gene Therapy showing such high variability in patient responses?"*

Digging deeper into the demographics, Dr. Rodriguez discovers Asian populations respond 40% better to Gene Therapy than African American populations.

**Investment Question:** *"Are our high-cost Gene Therapy programs ($300-500M) justified by their efficacy profiles?"*

The analysis confirms that successful Gene Therapy programs easily justify their development costs, with projected returns of 200-300%.

**Red Flag Question:** *"Which of our expensive drugs are underperforming and why?"*

**The Shocking Discovery:** Three specific compounds (GammaTreat, IotaRx, LambdaTreat) are underperforming despite investments exceeding $350M each - representing $1.2B in potentially misallocated capital.

**Mechanism Deep-Dive:** *"How do our Monoclonal Antibodies perform across different patient populations?"*

The investigation reveals elderly obese patients (>65 years, BMI >30) show 20% reduced efficacy, while Asian and Hispanic populations demonstrate 20% better response rates.

**Action Plan:** Focus Gene Therapy development on Asian markets first and develop demographic-specific dosing strategies for monoclonal antibodies.

---

## ⚠️ The Regulatory Wake-Up Call: "Why Is the FDA Asking About Our Neurology Portfolio?"

**Jennifer Wu, Regulatory Affairs Manager**, receives an unexpected call from the FDA requesting additional safety data on the company's neurology programs.

**Urgent Question:** *"What safety signals exist in our neurology portfolio that caught regulatory attention?"*

The analysis reveals Gene Therapy neurology drugs show 2-3x higher adverse event rates compared to other therapeutic areas.

**Risk Assessment Question:** *"Which patient populations are at highest risk for serious adverse events?"*

Jennifer discovers a clear pattern: Age >65, BMI >30, and treatment duration >180 days significantly increase serious adverse events.

**Site Investigation:** *"Is there a relationship between investigational sites and safety outcomes?"*

**The Critical Finding:** Site certification level strongly correlates with safety outcomes - Level 1 sites show 40% more adverse events than Level 3 sites.

**Demographic Analysis:** *"Are there broader demographic risk patterns we need to address?"*

The investigation reveals:
- Age >70 increases adverse event risk by 50% across all drug categories
- High BMI (>30) correlates with both efficacy reduction and safety concerns
- Treatment duration >180 days in high-risk populations requires special labeling considerations

**Compliance Question:** *"How do patient compliance rates affect safety profiles for long-term treatments?"*

For patients with treatment duration >180 days, safety profiles significantly differ between high-compliance (>90%) and lower-compliance cohorts.

**Action Plan:** Implement enhanced safety monitoring for neurology Gene Therapy programs and develop risk-based dosing guidelines.

---

## 🌍 The Global Strategy Breakthrough: "Where Should We Expand Next?"

**David Kim, Business Development Executive**, is reviewing potential market expansion opportunities for the upcoming board presentation.

**Market Opportunity Question:** *"Which geographic markets show the strongest potential for our Gene Therapy portfolio?"*

The data reveals Asian markets present exceptional opportunity with 90% superior response rates for Gene Therapy mechanisms.

**Operational Feasibility Question:** *"Can we actually execute successful trials in Asian markets?"*

Analysis shows strong enrollment efficiency in developed Asian markets, with Japan at 70% efficiency (projected 85% with optimization).

**Strategic Location Question:** *"Which regions should serve as our centers of excellence for future expansion?"*

**The Strategic Discovery:** Nordic countries (Sweden, Netherlands) consistently outperform in both enrollment and outcomes, while German sites offer optimal balance of volume, quality, and cost-effectiveness.

**ROI Calculation:** *"What are the projected returns for different mechanism-market combinations?"*

The analysis reveals:
- Gene Therapy + Asian markets = highest risk-adjusted returns (200-300% development cost recovery)
- Monoclonal Antibody + Global diverse populations = steady, predictable returns (150-200% cost recovery)

**Partnership Evaluation:** *"Which programs have the strongest value proposition for out-licensing?"*

Jennifer discovers that successful Phase II cardiology and endocrinology programs show strong out-licensing potential, especially when highlighting demographic differentiation and ethnic response variations.

**Action Plan:** Prioritize Asian market entry strategy for Gene Therapy portfolio and establish Nordic centers of excellence for challenging study populations.

---

## 💰 The Portfolio Optimization Crisis: "Are We Investing in the Right Programs?"

During the quarterly investment committee meeting, **David Kim** faces tough questions about capital allocation efficiency.

**Investment Reality Check:** *"Which of our high-cost programs are delivering expected returns?"*

The shocking revelation: While drugs costing >$300M show mixed justification overall, 70% deliver expected returns, but three specific underperformers represent massive capital misallocation.

**Strategic Reallocation Question:** *"How should we reallocate resources from underperformers to high-potential combinations?"*

**The Business Intelligence Breakthrough:** The data shows clear winners and losers:
- **Winners:** Gene Therapy + Asian markets with 200-300% cost recovery potential
- **Steady Performers:** Monoclonal Antibody + Global diverse populations with 150-200% returns
- **Losers:** Three high-cost underperformers consuming $1.2B in capital

**Licensing Strategy Question:** *"Which programs should we out-license versus continue internal development?"*

The analysis reveals demographic differentiation (especially ethnic response variations) creates premium licensing value in targeted geographic markets.

**Action Plan:** Reallocate resources from underperformers to high-potential mechanism-market combinations and develop licensing packages highlighting demographic advantages.

These discovery stories demonstrate how natural analytical curiosity, combined with progressive questioning, leads to actionable insights that drive strategic decision-making across clinical operations, drug development, regulatory affairs, and business development functions.

# 📊 Key Findings Summary

The generated dataset contains realistic patterns and correlations that enable discovery of actionable insights for each persona. Below are the key findings built into the data:

## 🏥 Site Performance & Operations

**Level 3 Certified Sites Excel But At Premium Cost:**
- Level 3 certified sites consistently deliver 20% better patient outcomes and 10% higher compliance rates
- However, operational costs are significantly higher due to 15-25 investigators vs 5-12 at Level 1 sites
- Hospital and Research Institute sites outperform Private Clinics across all therapeutic areas
- **Action Item:** Level 3 sites justify premium costs for Phase III trials and high-stakes studies

**Geographic Performance Variations:**
- Northern European sites (Netherlands, Sweden) show exceptional enrollment efficiency (90-95%)
- Japanese sites struggle with enrollment (70% efficiency) but deliver superior safety profiles
- USA dominates volume (30% of patients) but shows mixed performance outcomes
- **Action Item:** Prioritize Northern European sites for challenging enrollments

## 💊 Drug Mechanism Effectiveness

**Gene Therapy Shows Revolutionary Potential With Ethnic Variations:**
- Asian populations respond 40% better to Gene Therapy than African American populations
- High variability (50-180% response range) creates both opportunities and risks
- Development costs ($300-500M) are justified for successful Gene Therapy programs
- **Action Item:** Focus Gene Therapy development on Asian markets first

**Monoclonal Antibodies Display Demographic-Specific Performance:**
- Elderly obese patients (>65 years, BMI >30) show 20% reduced efficacy
- Asian and Hispanic populations demonstrate 20% better response rates
- Strong safety profiles make them ideal for global registration strategies
- **Action Item:** Develop demographic-specific dosing strategies for monoclonal antibodies

**High-Cost Drug Portfolio Analysis:**
- Drugs costing >$300M show mixed justification: 70% deliver expected returns
- Three specific compounds (GammaTreat, IotaRx, LambdaTreat) underperform despite high investment
- Small molecules remain most cost-effective for broad market applications
- **Action Item:** Reassess high-cost underperformers for partnership or discontinuation

## ⚠️ Safety Signal Discoveries

**Neurology Portfolio Requires Regulatory Attention:**
- Gene Therapy neurology drugs show 2-3x higher adverse event rates
- Risk factors: Age >65, BMI >30, and treatment duration >180 days significantly increase serious adverse events
- Site certification level strongly correlates with safety outcomes (Level 1 sites show 40% more adverse events)
- **Action Item:** Implement enhanced safety monitoring for neurology Gene Therapy programs

**Demographic Risk Profiling:**
- Age >70 increases adverse event risk by 50% across all drug categories
- High BMI (>30) correlates with both efficacy reduction and safety concerns
- Treatment duration >180 days in high-risk populations requires special labeling considerations
- **Action Item:** Develop risk-based dosing guidelines and enhanced monitoring protocols

## 🌍 Geographic Market Opportunities

**Asian Markets Present Exceptional Gene Therapy Opportunity:**
- 90% superior response rates in Asian populations for Gene Therapy mechanisms
- Strong enrollment efficiency in developed Asian markets (Japan: 70%, projected 85% with optimization)
- Regulatory pathway advantages due to positive safety/efficacy profiles
- **Action Item:** Prioritize Asian market entry strategy for Gene Therapy portfolio

**European Excellence Centers:**
- Nordic countries (Sweden, Netherlands) consistently outperform in enrollment and outcomes
- German sites offer optimal balance of volume, quality, and cost-effectiveness
- UK provides strong regulatory precedent for global submissions
- **Action Item:** Establish Nordic centers of excellence for challenging study populations

## 💰 Business Intelligence & ROI

**Portfolio Optimization Insights:**
- Gene Therapy + Asian markets = highest risk-adjusted returns (200-300% development cost recovery projected)
- Monoclonal Antibody + Global diverse populations = steady, predictable returns (150-200% cost recovery)
- Three high-cost underperformers represent $1.2B in potentially misallocated capital
- **Action Item:** Reallocate resources from underperformers to high-potential mechanism-market combinations

**Partnership & Licensing Opportunities:**
- Successful Phase II cardiology and endocrinology programs show strong out-licensing potential
- Demographic differentiation (especially ethnic response variations) creates premium licensing value
- Geographic market data supports targeted partnership strategies in high-performance regions
- **Action Item:** Develop licensing packages highlighting demographic advantages and geographic performance data

These findings demonstrate the dataset's ability to support sophisticated, multi-dimensional analysis that drives strategic decision-making across clinical operations, drug development, regulatory affairs, and business development functions.
