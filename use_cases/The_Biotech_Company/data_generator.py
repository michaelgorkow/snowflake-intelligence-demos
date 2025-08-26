import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

def generate_biotech_dataset(num_patients=1000, num_drugs=20, num_sites=50, num_trials=15, output_dir='data/'):
    """
    Generate a biotech clinical trial dataset with realistic patterns for persona-based analysis.
    
    Args:
        num_patients (int): Number of patients to generate
        num_drugs (int): Number of drugs to generate
        num_sites (int): Number of clinical trial sites to generate
        num_trials (int): Number of clinical trials to generate
        output_dir (str): Directory to save the generated data files
    
    Returns:
        dict: Dictionary containing all generated dataframes
    """
    
    fake = Faker()
    random.seed(42)  # For reproducible results
    np.random.seed(42)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating biotech clinical trial dataset with realistic patterns...")
    
    # ====== DIMENSION TABLES ======
    
    # 1. DIM_PATIENTS - Patient Demographics
    print("Creating DIM_PATIENTS table...")
    patients_data = []
    
    # Define demographic patterns that will affect outcomes
    countries_with_patterns = {
        'USA': {'weight': 0.3, 'enrollment_efficiency': 0.8},
        'Germany': {'weight': 0.15, 'enrollment_efficiency': 0.9},
        'UK': {'weight': 0.12, 'enrollment_efficiency': 0.85},
        'Canada': {'weight': 0.1, 'enrollment_efficiency': 0.82},
        'Japan': {'weight': 0.08, 'enrollment_efficiency': 0.7},
        'France': {'weight': 0.08, 'enrollment_efficiency': 0.78},
        'Australia': {'weight': 0.05, 'enrollment_efficiency': 0.88},
        'Netherlands': {'weight': 0.04, 'enrollment_efficiency': 0.92},
        'Sweden': {'weight': 0.03, 'enrollment_efficiency': 0.95},
        'Spain': {'weight': 0.05, 'enrollment_efficiency': 0.75}
    }
    
    countries = list(countries_with_patterns.keys())
    country_weights = [countries_with_patterns[c]['weight'] for c in countries]
    
    ethnicities_with_response = {
        'Caucasian': {'weight': 0.5, 'gene_therapy_response': 0.8, 'mab_response': 0.75},
        'Asian': {'weight': 0.2, 'gene_therapy_response': 0.9, 'mab_response': 0.85},
        'African American': {'weight': 0.15, 'gene_therapy_response': 0.65, 'mab_response': 0.7},
        'Hispanic': {'weight': 0.12, 'gene_therapy_response': 0.7, 'mab_response': 0.8},
        'Other': {'weight': 0.03, 'gene_therapy_response': 0.75, 'mab_response': 0.78}
    }
    
    ethnicities = list(ethnicities_with_response.keys())
    ethnicity_weights = [ethnicities_with_response[e]['weight'] for e in ethnicities]
    
    for i in range(1, num_patients + 1):
        # Age distribution with more patients in target demographics
        age = int(np.random.normal(55, 15))
        age = max(18, min(85, age))  # Clamp to realistic range
        
        gender = random.choice(['Male', 'Female'])
        country = np.random.choice(countries, p=country_weights)
        ethnicity = np.random.choice(ethnicities, p=ethnicity_weights)
        
        # BMI patterns that will affect outcomes
        if age > 60:
            bmi = max(18.5, min(40.0, np.random.normal(28, 5)))
        else:
            bmi = max(18.5, min(40.0, np.random.normal(25, 4)))
        
        patients_data.append({
            'PATIENT_ID': f'PAT_{i:04d}',
            'AGE': age,
            'GENDER': gender,
            'ETHNICITY': ethnicity,
            'BMI': round(bmi, 1),
            'COUNTRY': country,
            'ENROLLMENT_DATE': fake.date_between(start_date='-2y', end_date='today')
        })
    
    dim_patients = pd.DataFrame(patients_data)
    
    # 2. DIM_DRUGS - Drug Information with strategic patterns
    print("Creating DIM_DRUGS table...")
    drug_categories = ['Oncology', 'Cardiology', 'Neurology', 'Immunology', 'Endocrinology']
    drug_names = [
        'AlphaCure', 'BetaHeal', 'GammaTreat', 'DeltaRx', 'EpsilonMed',
        'ZetaTherapy', 'EtaCure', 'ThetaHeal', 'IotaRx', 'KappaMed',
        'LambdaTreat', 'MuTherapy', 'NuCure', 'XiHeal', 'OmicronRx',
        'PiMed', 'RhoTreat', 'SigmaTherapy', 'TauCure', 'UpsilonHeal'
    ]
    
    # Define strategic drug portfolio with realistic cost-efficacy patterns
    drug_mechanisms = ['Small Molecule', 'Monoclonal Antibody', 'Protein', 'Gene Therapy']
    indications = ['Cancer', 'Heart Disease', 'Alzheimer\'s', 'Diabetes', 'Arthritis']
    
    drugs_data = []
    for i in range(1, num_drugs + 1):
        category = random.choice(drug_categories)
        mechanism = random.choice(drug_mechanisms)
        indication = random.choice(indications)
        
        # Cost patterns: Gene Therapy and Monoclonal Antibodies are more expensive
        if mechanism == 'Gene Therapy':
            base_cost = random.randint(300000000, 500000000)
        elif mechanism == 'Monoclonal Antibody':
            base_cost = random.randint(200000000, 400000000)
        elif mechanism == 'Protein':
            base_cost = random.randint(150000000, 350000000)
        else:  # Small Molecule
            base_cost = random.randint(50000000, 250000000)
        
        # Some high-cost drugs will underperform (for business analysis)
        if i in [3, 7, 12]:  # Specific drugs that will be poor ROI
            base_cost = random.randint(350000000, 500000000)
        
        drugs_data.append({
            'DRUG_ID': f'DRG_{i:03d}',
            'DRUG_NAME': drug_names[i-1],
            'CATEGORY': category,
            'MECHANISM': mechanism,
            'INDICATION': indication,
            'DOSAGE_FORM': random.choice(['Tablet', 'Injection', 'Capsule', 'IV Infusion']),
            'DEVELOPMENT_COST_USD': base_cost
        })
    
    dim_drugs = pd.DataFrame(drugs_data)
    
    # 3. DIM_SITES - Clinical Trial Sites with performance patterns
    print("Creating DIM_SITES table...")
    
    # Site performance will correlate with certification level and investigator count
    site_countries = {
        'USA': 15, 'Germany': 8, 'UK': 6, 'Canada': 4, 'Japan': 3,
        'France': 4, 'Australia': 3, 'Netherlands': 2, 'Sweden': 2, 'Spain': 3
    }
    
    sites_data = []
    site_id = 1
    
    for country, count in site_countries.items():
        for i in range(count):
            # Higher certification levels have more investigators and better outcomes
            cert_level = random.choice(['Level 1', 'Level 2', 'Level 3'])
            
            if cert_level == 'Level 3':
                investigator_count = random.randint(15, 25)
                site_type = random.choice(['Hospital', 'Research Institute'])  # Better sites
            elif cert_level == 'Level 2':
                investigator_count = random.randint(10, 18)
                site_type = random.choice(['Hospital', 'Research Institute', 'Private Clinic'])
            else:  # Level 1
                investigator_count = random.randint(5, 12)
                site_type = random.choice(['Private Clinic', 'Hospital'])
            
            city = fake.city()
            sites_data.append({
                'SITE_ID': f'SITE_{site_id:03d}',
                'SITE_NAME': f'{city} Medical Center',
                'CITY': city,
                'COUNTRY': country,
                'SITE_TYPE': site_type,
                'INVESTIGATOR_COUNT': investigator_count,
                'CERTIFICATION_LEVEL': cert_level
            })
            site_id += 1
    
    dim_sites = pd.DataFrame(sites_data)
    
    # 4. DIM_TRIALS - Clinical Trial Information
    print("Creating DIM_TRIALS table...")
    trials_data = []
    
    # Ensure we have trials for the key therapeutic areas mentioned in personas
    key_categories = ['Oncology', 'Cardiology', 'Neurology']
    
    for i in range(1, num_trials + 1):
        start_date = fake.date_between(start_date='-3y', end_date='-1y')
        end_date = start_date + timedelta(days=random.randint(180, 720))
        
        # Phase III trials for some drugs approaching submission
        if i <= 5:
            phase = 'Phase III'
        elif i <= 10:
            phase = 'Phase II'
        else:
            phase = 'Phase I'
        
        trials_data.append({
            'TRIAL_ID': f'TRL_{i:03d}',
            'TRIAL_NAME': f'Clinical Study {i}',
            'PHASE': phase,
            'STATUS': random.choice(['Completed', 'Ongoing', 'Terminated', 'Suspended']) if phase != 'Phase III' else 'Completed',
            'PRIMARY_ENDPOINT': random.choice(['Safety', 'Efficacy', 'Dosage', 'Biomarker Response']),
            'START_DATE': start_date,
            'END_DATE': end_date,
            'PLANNED_ENROLLMENT': random.randint(50, 500),
            'SPONSOR': random.choice(['BioTech Corp', 'Pharma Global', 'Research Institute', 'Medical University'])
        })
    
    dim_trials = pd.DataFrame(trials_data)
    
    # ====== FACT TABLE WITH REALISTIC PATTERNS ======
    
    # 5. FACT_TRIAL_RESULTS - Clinical Trial Results with persona-relevant patterns
    print("Creating FACT_TRIAL_RESULTS table with realistic outcome patterns...")
    results_data = []
    
    for trial_idx, trial in enumerate(dim_trials['TRIAL_ID']):
        # Each trial has a subset of patients
        trial_patients = random.sample(list(dim_patients['PATIENT_ID']), 
                                     random.randint(30, min(200, num_patients)))
        
        for patient_id in trial_patients:
            # Get patient characteristics for outcome modeling
            patient = dim_patients[dim_patients['PATIENT_ID'] == patient_id].iloc[0]
            
            # Assign drug and site for this trial
            drug_id = random.choice(dim_drugs['DRUG_ID'])
            drug = dim_drugs[dim_drugs['DRUG_ID'] == drug_id].iloc[0]
            
            site_id = random.choice(dim_sites['SITE_ID'])
            site = dim_sites[dim_sites['SITE_ID'] == site_id].iloc[0]
            
            # === OUTCOME MODELING WITH REALISTIC PATTERNS ===
            
            # Base outcomes
            baseline_score = random.randint(20, 80)
            treatment_arm = random.choice(['Treatment', 'Placebo', 'Control'])
            
            # Initialize improvement based on treatment arm
            if treatment_arm == 'Treatment':
                base_improvement = random.randint(-10, 40)
            elif treatment_arm == 'Placebo':
                base_improvement = random.randint(-15, 10)
            else:  # Control
                base_improvement = random.randint(-20, 5)
            
            # === DRUG MECHANISM EFFECTS ===
            mechanism_modifier = 1.0
            
            if drug['MECHANISM'] == 'Gene Therapy':
                # Gene therapy shows promise but high variability
                if patient['ETHNICITY'] == 'Asian':
                    mechanism_modifier = 1.4  # Better response in Asian populations
                elif patient['ETHNICITY'] == 'African American':
                    mechanism_modifier = 0.7  # Poorer response
                else:
                    mechanism_modifier = 1.1
                
                # High variability for gene therapy
                mechanism_modifier *= random.uniform(0.5, 1.8)
                
            elif drug['MECHANISM'] == 'Monoclonal Antibody':
                # Age and BMI effects for monoclonal antibodies
                if patient['AGE'] > 65 and patient['BMI'] > 30:
                    mechanism_modifier = 0.8  # Poorer response in elderly obese
                elif patient['ETHNICITY'] in ['Asian', 'Hispanic']:
                    mechanism_modifier = 1.2  # Better ethnic response
                else:
                    mechanism_modifier = 1.0
                    
            elif drug['MECHANISM'] == 'Small Molecule':
                # Age effects
                if patient['AGE'] > 70:
                    mechanism_modifier = 0.9
                else:
                    mechanism_modifier = 1.1
                    
            else:  # Protein
                mechanism_modifier = 1.0
            
            # === SITE PERFORMANCE EFFECTS ===
            site_modifier = 1.0
            
            if site['CERTIFICATION_LEVEL'] == 'Level 3':
                site_modifier = 1.2  # Better outcomes at Level 3 sites
            elif site['CERTIFICATION_LEVEL'] == 'Level 2':
                site_modifier = 1.1
            else:  # Level 1
                site_modifier = 0.9  # Poorer outcomes at Level 1 sites
            
            # Investigator count effect
            if site['INVESTIGATOR_COUNT'] > 20:
                site_modifier *= 1.1
            elif site['INVESTIGATOR_COUNT'] < 10:
                site_modifier *= 0.9
            
            # === THERAPEUTIC AREA EFFECTS ===
            category_modifier = 1.0
            
            if drug['CATEGORY'] == 'Oncology':
                # Oncology struggles with enrollment and outcomes
                category_modifier = 0.85
            elif drug['CATEGORY'] == 'Cardiology':
                # Cardiology also has challenges
                category_modifier = 0.9
            elif drug['CATEGORY'] == 'Neurology':
                # Neurology has mixed results
                category_modifier = random.uniform(0.7, 1.3)
            
            # === CALCULATE FINAL OUTCOMES ===
            
            final_improvement = int(base_improvement * mechanism_modifier * site_modifier * category_modifier)
            endpoint_score = baseline_score + final_improvement
            
            # === ADVERSE EVENTS MODELING ===
            
            base_ae = random.randint(0, 3)
            base_sae = 0
            
            # Neurology drugs have more safety signals
            if drug['CATEGORY'] == 'Neurology' and drug['MECHANISM'] == 'Gene Therapy':
                base_ae += random.randint(1, 3)
                if patient['AGE'] > 65 or patient['BMI'] > 30:
                    base_ae += 1
                    base_sae = random.randint(0, 2)
            
            # High BMI and age increase adverse events
            if patient['BMI'] > 30:
                base_ae += 1
            if patient['AGE'] > 70:
                base_ae += 1
                if random.random() < 0.3:
                    base_sae += 1
            
            # Site certification affects safety
            if site['CERTIFICATION_LEVEL'] == 'Level 1':
                base_ae += random.randint(0, 2)
                if random.random() < 0.2:
                    base_sae += 1
            
            adverse_events = min(5, base_ae)
            serious_adverse_events = min(2, base_sae)
            
            # === COMPLIANCE AND DURATION ===
            
            treatment_duration = random.randint(30, 365)
            
            # Compliance affected by adverse events and site quality
            base_compliance = random.uniform(0.7, 1.0)
            
            if adverse_events > 3:
                base_compliance *= 0.85
            if site['CERTIFICATION_LEVEL'] == 'Level 3':
                base_compliance = min(1.0, base_compliance * 1.1)
            
            compliance_rate = round(base_compliance, 2)
            
            # === OUTCOME CLASSIFICATION ===
            
            if final_improvement > 20:
                outcome = 'Success'
            elif final_improvement > 10:
                outcome = 'Partial Response'
            elif final_improvement > 0:
                outcome = random.choice(['Partial Response', 'No Response'])
            else:
                outcome = 'Failure'
            
            # Poor performers for business analysis
            if drug_id in ['DRG_003', 'DRG_007', 'DRG_012']:
                if random.random() < 0.6:  # 60% chance of poor outcome
                    outcome = random.choice(['Failure', 'No Response'])
                    final_improvement = random.randint(-20, 5)
                    endpoint_score = baseline_score + final_improvement
            
            results_data.append({
                'RESULT_ID': f'RES_{len(results_data) + 1:06d}',
                'TRIAL_ID': trial,
                'PATIENT_ID': patient_id,
                'DRUG_ID': drug_id,
                'SITE_ID': site_id,
                'TREATMENT_ARM': treatment_arm,
                'BASELINE_SCORE': baseline_score,
                'ENDPOINT_SCORE': endpoint_score,
                'IMPROVEMENT': final_improvement,
                'ADVERSE_EVENTS': adverse_events,
                'SERIOUS_ADVERSE_EVENTS': serious_adverse_events,
                'TREATMENT_DURATION_DAYS': treatment_duration,
                'COMPLIANCE_RATE': compliance_rate,
                'OUTCOME': outcome,
                'VISIT_DATE': fake.date_between(start_date='-2y', end_date='today')
            })
    
    fact_trial_results = pd.DataFrame(results_data)
    
    # ====== SAVE DATA ======
    
    datasets = {
        'DIM_PATIENTS': dim_patients,
        'DIM_DRUGS': dim_drugs,
        'DIM_SITES': dim_sites,
        'DIM_TRIALS': dim_trials,
        'FACT_TRIAL_RESULTS': fact_trial_results
    }
    
    print(f"\nSaving datasets to {output_dir}...")
    for table_name, df in datasets.items():
        filename = f"{table_name.lower()}.csv"
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"  ✓ {table_name}: {len(df)} records saved to {filename}")
    
    # ====== PRINT SUMMARY WITH INSIGHTS ======
    
    print("\n" + "="*60)
    print("BIOTECH CLINICAL TRIAL DATASET SUMMARY")
    print("="*60)
    
    print(f"\nDIMENSION TABLES:")
    print(f"  • DIM_PATIENTS: {len(dim_patients)} patients with demographics")
    print(f"  • DIM_DRUGS: {len(dim_drugs)} drugs across {len(drug_categories)} categories")
    print(f"  • DIM_SITES: {len(dim_sites)} clinical trial sites worldwide")
    print(f"  • DIM_TRIALS: {len(dim_trials)} clinical trials in various phases")
    
    print(f"\nFACT TABLE:")
    print(f"  • FACT_TRIAL_RESULTS: {len(fact_trial_results)} trial result records")
    
    print(f"\nKEY PATTERNS BUILT INTO THE DATA:")
    print(f"  🏥 SITE PERFORMANCE: Level 3 certified sites show better outcomes")
    print(f"  💊 DRUG MECHANISMS: Gene Therapy shows promise with ethnic variations")
    print(f"  🧬 DEMOGRAPHICS: Age, BMI, and ethnicity affect treatment response")
    print(f"  ⚠️  SAFETY SIGNALS: Neurology drugs show concerning adverse event patterns")
    print(f"  💰 ROI ANALYSIS: High-cost drugs mostly justified, but some poor performers")
    print(f"  🌍 GEOGRAPHIC: Asian markets show strong potential for Gene Therapy")
    
    print(f"\nSAMPLE PERSONA QUERIES:")
    print(f"  👩‍⚕️ Clinical Manager: 'Which Level 3 sites have best ROI vs cost?'")
    print(f"  🔬 Drug Scientist: 'How do monoclonal antibodies perform by ethnicity?'")
    print(f"  📋 Regulatory: 'What safety signals exist in neurology portfolio?'")
    print(f"  💼 Business Dev: 'Which high-cost drugs justify their development costs?'")
    
    print(f"\nAll files saved to: {os.path.abspath(output_dir)}")
    print("="*60)
    
    return datasets

# Example usage
if __name__ == "__main__":
    # Generate the dataset
    data = generate_biotech_dataset(
        num_patients=1000,
        num_drugs=20,
        num_sites=50,
        num_trials=15,
        output_dir='data/'
    )
    
    # Display sample data from each table
    print("\nSAMPLE DATA PREVIEW:")
    print("-" * 40)
    
    for table_name, df in data.items():
        print(f"\n{table_name} (first 3 rows):")
        print(df.head(3).to_string(index=False))
