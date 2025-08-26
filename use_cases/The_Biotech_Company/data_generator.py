import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

def generate_biotech_dataset(num_patients=1000, num_drugs=20, num_sites=50, num_trials=15, output_dir='data/'):
    """
    Generate a simple biotech clinical trial dataset with 5 tables following a star schema.
    
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
    
    print("Generating biotech clinical trial dataset...")
    
    # ====== DIMENSION TABLES ======
    
    # 1. DIM_PATIENTS - Patient Demographics
    print("Creating DIM_PATIENTS table...")
    patients_data = []
    for i in range(1, num_patients + 1):
        age = random.randint(18, 85)
        gender = random.choice(['Male', 'Female'])
        
        patients_data.append({
            'PATIENT_ID': f'PAT_{i:04d}',
            'AGE': age,
            'GENDER': gender,
            'ETHNICITY': random.choice(['Caucasian', 'Hispanic', 'African American', 'Asian', 'Other']),
            'BMI': round(random.uniform(18.5, 40.0), 1),
            'COUNTRY': fake.country(),
            'ENROLLMENT_DATE': fake.date_between(start_date='-2y', end_date='today')
        })
    
    dim_patients = pd.DataFrame(patients_data)
    
    # 2. DIM_DRUGS - Drug Information
    print("Creating DIM_DRUGS table...")
    drug_categories = ['Oncology', 'Cardiology', 'Neurology', 'Immunology', 'Endocrinology']
    drug_names = [
        'AlphaCure', 'BetaHeal', 'GammaTreat', 'DeltaRx', 'EpsilonMed',
        'ZetaTherapy', 'EtaCure', 'ThetaHeal', 'IotaRx', 'KappaMed',
        'LambdaTreat', 'MuTherapy', 'NuCure', 'XiHeal', 'OmicronRx',
        'PiMed', 'RhoTreat', 'SigmaTherapy', 'TauCure', 'UpsilonHeal'
    ]
    
    drugs_data = []
    for i in range(1, num_drugs + 1):
        drugs_data.append({
            'DRUG_ID': f'DRG_{i:03d}',
            'DRUG_NAME': drug_names[i-1],
            'CATEGORY': random.choice(drug_categories),
            'MECHANISM': random.choice(['Small Molecule', 'Monoclonal Antibody', 'Protein', 'Gene Therapy']),
            'INDICATION': random.choice(['Cancer', 'Heart Disease', 'Alzheimer\'s', 'Diabetes', 'Arthritis']),
            'DOSAGE_FORM': random.choice(['Tablet', 'Injection', 'Capsule', 'IV Infusion']),
            'DEVELOPMENT_COST_USD': random.randint(50000000, 500000000)
        })
    
    dim_drugs = pd.DataFrame(drugs_data)
    
    # 3. DIM_SITES - Clinical Trial Sites
    print("Creating DIM_SITES table...")
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 
              'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
              'London', 'Paris', 'Berlin', 'Madrid', 'Rome', 'Amsterdam', 'Stockholm',
              'Toronto', 'Vancouver', 'Montreal', 'Sydney', 'Melbourne', 'Tokyo']
    
    sites_data = []
    for i in range(1, num_sites + 1):
        city = random.choice(cities)
        sites_data.append({
            'SITE_ID': f'SITE_{i:03d}',
            'SITE_NAME': f'{city} Medical Center',
            'CITY': city,
            'COUNTRY': 'USA' if city in cities[:12] else random.choice(['UK', 'France', 'Germany', 'Spain', 'Italy', 'Netherlands', 'Sweden', 'Canada', 'Australia', 'Japan']),
            'SITE_TYPE': random.choice(['Hospital', 'Research Institute', 'Private Clinic']),
            'INVESTIGATOR_COUNT': random.randint(5, 25),
            'CERTIFICATION_LEVEL': random.choice(['Level 1', 'Level 2', 'Level 3'])
        })
    
    dim_sites = pd.DataFrame(sites_data)
    
    # 4. DIM_TRIALS - Clinical Trial Information
    print("Creating DIM_TRIALS table...")
    trials_data = []
    for i in range(1, num_trials + 1):
        start_date = fake.date_between(start_date='-3y', end_date='-1y')
        end_date = start_date + timedelta(days=random.randint(180, 720))
        
        trials_data.append({
            'TRIAL_ID': f'TRL_{i:03d}',
            'TRIAL_NAME': f'Clinical Study {i}',
            'PHASE': random.choice(['Phase I', 'Phase II', 'Phase III']),
            'STATUS': random.choice(['Completed', 'Ongoing', 'Terminated', 'Suspended']),
            'PRIMARY_ENDPOINT': random.choice(['Safety', 'Efficacy', 'Dosage', 'Biomarker Response']),
            'START_DATE': start_date,
            'END_DATE': end_date,
            'PLANNED_ENROLLMENT': random.randint(50, 500),
            'SPONSOR': random.choice(['BioTech Corp', 'Pharma Global', 'Research Institute', 'Medical University'])
        })
    
    dim_trials = pd.DataFrame(trials_data)
    
    # ====== FACT TABLE ======
    
    # 5. FACT_TRIAL_RESULTS - Clinical Trial Results
    print("Creating FACT_TRIAL_RESULTS table...")
    results_data = []
    
    # Generate results for each combination (some patients may be in multiple trials)
    for trial in dim_trials['TRIAL_ID']:
        # Each trial has a subset of patients
        trial_patients = random.sample(list(dim_patients['PATIENT_ID']), 
                                     random.randint(30, min(200, num_patients)))
        
        for patient_id in trial_patients:
            # Assign random drug and site for this trial
            drug_id = random.choice(dim_drugs['DRUG_ID'])
            site_id = random.choice(dim_sites['SITE_ID'])
            
            # Generate realistic trial results
            baseline_score = random.randint(20, 80)
            treatment_score = baseline_score + random.randint(-30, 50)
            
            results_data.append({
                'RESULT_ID': f'RES_{len(results_data) + 1:06d}',
                'TRIAL_ID': trial,
                'PATIENT_ID': patient_id,
                'DRUG_ID': drug_id,
                'SITE_ID': site_id,
                'TREATMENT_ARM': random.choice(['Treatment', 'Placebo', 'Control']),
                'BASELINE_SCORE': baseline_score,
                'ENDPOINT_SCORE': treatment_score,
                'IMPROVEMENT': treatment_score - baseline_score,
                'ADVERSE_EVENTS': random.randint(0, 5),
                'SERIOUS_ADVERSE_EVENTS': random.randint(0, 2),
                'TREATMENT_DURATION_DAYS': random.randint(30, 365),
                'COMPLIANCE_RATE': round(random.uniform(0.7, 1.0), 2),
                'OUTCOME': random.choice(['Success', 'Failure', 'Partial Response', 'No Response']),
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
    
    # ====== PRINT SUMMARY ======
    
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
    
    print(f"\nSAMPLE QUERIES FOR TEXT-TO-SQL AGENT:")
    print(f"  • 'Show me the average improvement score by drug category'")
    print(f"  • 'Which sites had the most adverse events?'")
    print(f"  • 'What is the success rate for Phase III trials?'")
    print(f"  • 'Show patient demographics for successful treatments'")
    print(f"  • 'Which drugs had the highest compliance rates?'")
    
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
