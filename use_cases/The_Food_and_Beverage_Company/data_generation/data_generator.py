import json
import pandas as pd
import numpy as np
import random
import scipy
from datetime import datetime
from scipy.stats import truncnorm
from faker import Faker
from datetime import date
import swifter
from snowflake.snowpark import functions as F
from transformers import pipeline
from transformers.pipelines.pt_utils import KeyDataset
from datasets import Dataset
import json
from pathlib import Path
import shutil
import uuid


# Set random seed for reproducible results
np.random.seed(42)
random.seed(42)
Faker.seed(0)
fake = Faker()

class DataGenerator():
    def __init__(self, session, config_path = 'data_generation/'):
        self.config_path = config_path
        self.session = session
        return

    def load_configuration(self):
        # tables
        self.product_categories = json.load(open(f'{ self.config_path}/01_tables/configuration/product_categories.json'))
        self.product_subcategories = json.load(open(f'{ self.config_path}/01_tables/configuration/product_subcategories.json'))
        self.product_prices = json.load(open(f'{ self.config_path}/01_tables/configuration/product_prices.json'))
        self.products = json.load(open(f'{ self.config_path}/01_tables/configuration/products.json'))
        self.events = json.load(open(f'{ self.config_path}/01_tables/configuration/events.json'))
        self.platforms = json.load(open(f'{ self.config_path}/01_tables/configuration/platforms.json'))
        self.personas = json.load(open(f'{ self.config_path}/01_tables/configuration/personas.json'))
        self.persona_products = json.load(open(f'{ self.config_path}/01_tables/configuration/persona_products.json'))
        self.suppliers = json.load(open(f'{ self.config_path}/01_tables/configuration/suppliers.json'))
        self.supplier_products = json.load(open(f'{ self.config_path}/01_tables/configuration/supplier_products.json'))

        # audio
        self.customer_reviews = json.load(open(f'{ self.config_path}/04_audio/configuration/event_reviews.json'))

    def generate_dim_suppliers(self):
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(self.suppliers, orient='index')
        
        # Add supplier name as a column
        df['SUPPLIER_NAME'] = df.index
        df = df.reset_index(drop=True)
        
        # Reorder columns
        df = df[['SUPPLIER_ID', 'SUPPLIER_NAME', 'COUNTRY', 'CITY', 'STREET', 'CONTACT_PERSON']]
        return df
    
    def generate_dim_date(self, start_date, end_date):
        start_date = '2000-01-01'
        end_date = '2030-12-31'
        day_difference = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
        future_days = day_difference.days+1
        self.session.sql(f"""
        CREATE OR REPLACE TABLE DIM_DATES AS
        WITH DATE_RANGE AS (
            SELECT '{start_date}'::DATE+x AS DATE
            FROM (
              SELECT row_number() over(order by 0) x 
              FROM TABLE(generator(rowcount => {future_days}))
            )
        )
        SELECT
            TO_NUMBER(TO_CHAR(DATE::DATE, 'YYYYMMDD')) AS DATE_KEY,
            DATE,
            DATE_PART('YEAR',DATE) AS YEAR,
            DATE_PART('MONTH',DATE) AS MONTH,
            DATE_PART('DAYOFYEAR',DATE) AS DAY_OF_YEAR,
            DATE_PART('WEEKOFYEAR',DATE) AS WEEK_OF_YEAR,
            DATE_PART('QUARTER',DATE) AS QUARTER,
            DAYNAME(DATE) AS DAY_NAME,
            MONTHNAME(DATE) AS MONTH_NAME,
            DATE_TRUNC('W', DATE) AS DATE_TRUNCATED_TO_WEEK, 
            DATE_TRUNC('MM', DATE) AS DATE_TRUNCATED_TO_MONTH
        FROM DATE_RANGE;
        """).collect()

    def generate_revenue_categories(self, start_date, end_date):
        # Convert string dates to datetime objects
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # Create date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')

        all_data = []
        for category, params in self.product_categories.items():
            category_data = []
            
            for i, date in enumerate(date_range):
                # Base revenue with growth trend
                base = params['base_revenue'] * (1 + params['growth_rate'] * i) / 100
                
                # Seasonal component (sinusoidal)
                day_of_year = date.timetuple().tm_yday
                seasonal_factor = 1 + params['seasonality_amplitude'] * np.sin(2 * np.pi * day_of_year / 365.25)
                
                # Adjust seasonal factor based on category characteristics
                if not params['summer_boost']:
                    # Invert the seasonal pattern for categories that perform worse in summer
                    seasonal_factor = 2 - seasonal_factor
                
                # Weekend effect
                weekend_factor = params['weekend_factor'] if date.weekday() >= 5 else 1.0
                
                # Holiday effects (simplified - major holidays boost)
                holiday_factor = 1.0
                if (date.month == 12 and date.day in [24, 25, 31]) or \
                   (date.month == 1 and date.day == 1) or \
                   (date.month == 11 and date.day >= 22 and date.day <= 28):  # Thanksgiving week
                    if category == 'Confectionery':
                        holiday_factor = 1.8
                    elif category == 'Food Products':
                        holiday_factor = 1.4
                    elif category == 'Beverages':
                        holiday_factor = 1.3
                    else:
                        holiday_factor = 1.1
                
                # Valentine's Day boost for Confectionery
                if category == 'Confectionery' and date.month == 2 and date.day == 14:
                    holiday_factor = 2.2
                
                # Back-to-school effect for Health Nutrition and Pet Care
                if category in ['Health & Nutrition', 'Pet Care'] and date.month == 9 and date.day <= 15:
                    holiday_factor = 1.2
                
                # Random daily variation (normal distribution)
                random_factor = np.random.normal(1.0, 0.1)
                random_factor = max(0.7, min(1.3, random_factor))  # Clamp to reasonable range
                
                # Occasional promotional events (5% chance of 20-40% boost)
                promo_factor = 1.0
                if random.random() < 0.05:
                    promo_factor = random.uniform(1.2, 1.4)
                
                # Calculate final revenue
                revenue = base * seasonal_factor * weekend_factor * holiday_factor * random_factor * promo_factor
                
                # Round to nearest dollar
                revenue = round(revenue, 2)
                
                category_data.append({
                    'DATE': date,
                    'PRODUCT_CATEGORY': category,
                    'PRODUCT_CATEGORY_REVENUE': revenue
                })
            
            all_data.extend(category_data)
        
        # Create DataFrame
        df = pd.DataFrame(all_data)
        
        # Sort by date and category for better organization
        df = df.sort_values(['DATE', 'PRODUCT_CATEGORY']).reset_index(drop=True)
        return df
    
    def generate_revenue_subcategories(self, df):
        # Define realistic revenue split percentages for each category
        category_splits = self.product_subcategories
        
        # Create list to store results
        result_rows = []
        
        # Process each row in the input dataframe
        for _, row in df.iterrows():
            date = row['DATE']
            category = row['PRODUCT_CATEGORY']
            total_revenue = row['PRODUCT_CATEGORY_REVENUE']
            
            # Check if category exists in our splits
            if category in category_splits:
                subcategory_splits = category_splits[category]
                
                # Add some realistic variation (±5%) to the base percentages
                # This makes the splits look more realistic over time
                np.random.seed(hash(str(date) + category) % 2**32)  # Consistent randomness per date/category
                
                adjusted_splits = {}
                total_adjusted = 0
                
                # Apply random variation to each split
                for subcat, base_pct in subcategory_splits.items():
                    # Add random variation between -5% to +5% of the base percentage
                    variation = np.random.uniform(-0.05, 0.05)
                    adjusted_pct = max(0.01, base_pct + variation)  # Ensure minimum 1%
                    adjusted_splits[subcat] = adjusted_pct
                    total_adjusted += adjusted_pct
                
                # Normalize to ensure splits sum to 1.0
                for subcat in adjusted_splits:
                    adjusted_splits[subcat] = adjusted_splits[subcat] / total_adjusted
                
                # Calculate revenue for each subcategory
                for subcategory, percentage in adjusted_splits.items():
                    subcategory_revenue = total_revenue * percentage
                    
                    result_rows.append({
                        'DATE': date,
                        'PRODUCT_CATEGORY': category,
                        'SUB_CATEGORY': subcategory,
                        'SUB_CATEGORY_REVENUE': round(subcategory_revenue, 2)
                    })
            else:
                # If category not found, create a warning entry
                result_rows.append({
                    'DATE': date,
                    'PRODUCT_CATEGORY': category,
                    'SUB_CATEGORY': 'Unknown',
                    'SUB_CATEGORY_REVENUE': total_revenue
                })
        
        # Create result dataframe
        result_df = pd.DataFrame(result_rows)
        
        # Sort by date and category for better readability
        result_df = result_df.sort_values(['DATE', 'PRODUCT_CATEGORY', 'SUB_CATEGORY']).reset_index(drop=True)
        return result_df


    def generate_facts_revenue_products(self, df):
        """
        Split subcategory revenue across individual products with realistic pricing and quantities.
        
        Parameters:
        df (pd.DataFrame): DataFrame with columns ['DATE', 'PRODUCT_CATEGORY', 'SUB_CATEGORY', 'SUB_CATEGORY_REVENUE']
        
        Returns:
        pd.DataFrame: DataFrame with product-level breakdown
        """
        
        # Product definitions with tier information
        products_data = self.products
        
        # Price ranges by category and tier (unit price, cogs)
        price_ranges = self.product_prices
        
        # Revenue split percentages by tier (Premium, Standard, Budget)
        revenue_splits = {
            'Premium': 0.35,  # Premium products get 35% of revenue
            'Standard': 0.45, # Standard products get 45% of revenue  
            'Budget': 0.20    # Budget products get 20% of revenue
        }
        
        result_rows = []
        
        for _, row in df.iterrows():
            date = row['DATE']
            category = row['PRODUCT_CATEGORY']
            subcategory = row['SUB_CATEGORY']
            total_revenue = row['SUB_CATEGORY_REVENUE']
            
            if category in products_data and subcategory in products_data[category]:
                subcategory_products = products_data[category][subcategory]
                price_info = price_ranges[category][subcategory]
                
                # Calculate revenue per tier
                for tier in ['Premium', 'Standard', 'Budget']:
                    products_in_tier = subcategory_products[tier]
                    if not products_in_tier:  # Skip if no products in tier
                        continue
                        
                    tier_revenue = total_revenue * revenue_splits[tier]
                    revenue_per_product = tier_revenue / len(products_in_tier)
                    
                    # Get price and COGS for this tier
                    unit_price, unit_cogs = price_info[tier]
                    if unit_price == 0:  # Skip if no price set
                        continue
                    
                    # Add some variation to prices within tier (±10%)
                    for i, product in enumerate(products_in_tier):
                        price_variation = 1#1 + (np.random.random() - 0.5) * 0.2  # ±10% variation
                        product_unit_price = round(unit_price * price_variation, 2)
                        product_unit_cogs = round(unit_cogs * price_variation, 2)
                        
                        # Calculate quantity sold
                        quantity = max(1, int(revenue_per_product / product_unit_price))
                        actual_revenue = round(quantity * product_unit_price, 2)
                        
                        result_rows.append({
                            'DATE': date,
                            'CATEGORY_HIER_1_NAME': category,
                            'CATEGORY_HIER_2_NAME': subcategory,
                            'PRODUCT_NAME': product,
                            'PRODUCT_TIER': tier,
                            'PRODUCT_UNIT_PRICE': product_unit_price,
                            'PRODUCT_UNIT_COGS': product_unit_cogs,
                            'QUANTITY': quantity,
                            'PRODUCT_REVENUE': actual_revenue
                        })
        
        # Create result dataframe
        result_df = pd.DataFrame(result_rows)
        return result_df

    def generate_dim_product_hierarchy(self, df):
        # Create a dictionary to store unique category mappings
        category_dict = {}
        subcategory_dict = {}
        
        # Get unique categories and assign HIER numbers
        unique_categories = df['CATEGORY_HIER_1_NAME'].unique()
        for i, category in enumerate(unique_categories, 1):
            category_dict[category] = f'HIER_{i}'
        
        # Create the category hierarchy column
        df['CATEGORY_HIER_1_ID'] = df['CATEGORY_HIER_1_NAME'].map(category_dict)
        
        # Create subcategory hierarchy
        for category in unique_categories:
            # Get subcategories for each category
            mask = df['CATEGORY_HIER_1_NAME'] == category
            subcategories = df.loc[mask, 'CATEGORY_HIER_2_NAME'].unique()
            
            # Create subcategory mappings
            for j, subcategory in enumerate(subcategories, 1):
                main_hier = category_dict[category]
                subcategory_dict[category + '_' + subcategory] = f'{main_hier}_{j}'
        
        # Create the subcategory hierarchy column
        df['CATEGORY_HIER_2_ID'] = df.apply(
            lambda x: subcategory_dict[x['CATEGORY_HIER_1_NAME'] + '_' + x['CATEGORY_HIER_2_NAME']], 
            axis=1
        )
        df = df[['CATEGORY_HIER_1_ID','CATEGORY_HIER_1_NAME','CATEGORY_HIER_2_ID','CATEGORY_HIER_2_NAME']]
        return df

    def generate_dim_products(self, facts_product_revenue_df, dim_product_hierarchy_df):
        dim_products_df = facts_product_revenue_df[['CATEGORY_HIER_1_NAME','CATEGORY_HIER_2_NAME','PRODUCT_NAME','PRODUCT_TIER','PRODUCT_UNIT_PRICE','PRODUCT_UNIT_COGS']].drop_duplicates()
        dim_products_df['PRODUCT_ID'] = [f'PID_{i:08d}' for i in range(len(dim_products_df))]
        dim_products_df = dim_products_df.merge(dim_product_hierarchy_df, on=['CATEGORY_HIER_1_NAME','CATEGORY_HIER_2_NAME'])
        dim_products_df = dim_products_df[['PRODUCT_ID','CATEGORY_HIER_1_ID','CATEGORY_HIER_2_ID','PRODUCT_NAME','PRODUCT_TIER','PRODUCT_UNIT_PRICE','PRODUCT_UNIT_COGS']]
        return dim_products_df

    def _get_age(self, min_age, mean_age, max_age, std_dev, size=1):    
        # Validate inputs
        if min_age >= max_age:
            raise ValueError("min_age must be less than max_age")
        if mean_age <= min_age or mean_age >= max_age:
            raise ValueError("mean_age must be between min_age and max_age")
        if std_dev <= 0:
            raise ValueError("std_dev must be positive")
        
        # Calculate the bounds for truncated normal distribution
        # These are in terms of standard deviations from the mean
        a = (min_age - mean_age) / std_dev  # Lower bound
        b = (max_age - mean_age) / std_dev  # Upper bound
        
        # Generate the truncated normal distribution
        ages = truncnorm.rvs(a, b, loc=mean_age, scale=std_dev, size=size)
        
        # Round to nearest integer (ages are typically whole numbers)
        ages = np.round(ages).astype(int)[0]
        
        return ages
    
    def generate_dim_customers(self):
        customers = []
        customer_id = 1
        for persona_group in self.personas.keys():
            persona_specs = self.personas[persona_group]
            for i in range(persona_specs['num_customers']):
                age = self._get_age(min_age=persona_specs['ages']['min'], mean_age=persona_specs['ages']['mean'], max_age=persona_specs['ages']['max'], std_dev=persona_specs['ages']['stddev'], size=1)
                #age = np.random.choice(persona_specs['ages']['ages'],p=np.array(persona_specs['ages']['probabilities']) / np.sum(persona_specs['ages']['probabilities']))    #persona_specs['ages']['probabilities'])
                birthday = fake.date_between(start_date=date(2025-int(age), 1, 1), end_date=date(2025-int(age), 12, 31))
                country = np.random.choice(persona_specs['countries']['countries'],p=persona_specs['countries']['probabilities'])
                gender = np.random.choice(persona_specs['gender']['genders'],p=persona_specs['gender']['probabilities'])
                if gender == 'Male':
                    first_name = fake.first_name_male()
                if gender == 'Female':
                    first_name = fake.first_name_female()
                last_name = fake.last_name()
                full_name = f'{first_name} {last_name}'
                row = {
                    'CUSTOMER_ID':f'CID_{customer_id:05d}',
                    'PERSONA_GROUP':persona_group,
                    'NAME':full_name,
                    'GENDER':gender,
                    'BIRTHDATE':birthday,
                    'COUNTRY':country,
                    
                }
                customers.append(row)
                customer_id += 1
        customers_df = pd.DataFrame(customers)
        # also create a dict for later retrieval
        self.persona_customer_mappings = {}
        for persona in self.personas.keys():
            self.persona_customer_mappings[persona] = customers_df[customers_df['PERSONA_GROUP'] == persona]['CUSTOMER_ID'].unique()
        customers_df = customers_df.drop('PERSONA_GROUP', axis=1)
        return customers_df

    def generate_transactions(self, df):
        
        def create_transactions(row):
            """Function that creates multiple records per row"""
            records = []
            date = row['DATE']
            product_name = row['PRODUCT_NAME']
            quantity = row['QUANTITY']
            _persona_names = self.persona_products[product_name]['persona_names']
            _probabilities = self.persona_products[product_name]['probabilities']
            
            while quantity >= 0:
                persona_name = np.random.choice(_persona_names, p=_probabilities)
                customer_id = np.random.choice(self.persona_customer_mappings[persona_name])
                row_quantity = np.random.choice([1,2,3,4,5],p=[0.4,0.3,0.15,0.1,0.05])
                _platforms = self.personas[persona_name]['platform_preference']['platforms']
                _platform_probabilities = self.personas[persona_name]['platform_preference']['probabilities']
                platform_name = np.random.choice(_platforms, p=_platform_probabilities)
                platform_id = self.platforms[platform_name]
                #session_duration = np.clip(np.random.normal(120, 3, 1).astype('int'), 60, 180)[0]
                row = {
                    'DATE_KEY':date,
                    'CUSTOMER_ID':customer_id,
                    'PRODUCT_NAME':product_name,
                    'QUANTITY':row_quantity,
                    'PLATFORM_ID':platform_id,
                    'PLATFORM_NAME':platform_name,
                }
                quantity -= row_quantity
                records.append(row)
            
            return records
        #users = {}
        # Apply function and explode the results
        fact_transactions_df = df.swifter.apply(create_transactions, axis=1)
        # Flatten the list of lists and create new DataFrame
        fact_transactions_df = [record for record_list in fact_transactions_df for record in record_list]
        fact_transactions_df = pd.DataFrame(fact_transactions_df)
        fact_transactions_df['SESSION_DURATION'] = np.clip(np.random.normal(120, 3, len(fact_transactions_df)).astype('int'), 60, 180) 
        return fact_transactions_df

    def generate_fact_supplier_deliveries2(self):
        
        def add_supplier(row):
            supplier_name = np.random.choice(self.supplier_products[row['PRODUCT_NAME']]['suppliers'],p=self.supplier_products[row['PRODUCT_NAME']]['probabilities'])
            return self.suppliers[supplier_name]['SUPPLIER_ID']
            
        df = (
            self.fact_transactions
                .join(self.dim_products, on=['PRODUCT_ID'])
                .join(self.dim_dates, on=['DATE_KEY'])
                .select(['DATE','PRODUCT_NAME','PRODUCT_ID','QUANTITY'])
                .with_column('WEEK', F.date_trunc('W','DATE'))
                .group_by(['PRODUCT_NAME','PRODUCT_ID','WEEK'])
                .agg(F.sum('QUANTITY').as_('WEEKLY_QUANTITY'))
                .order_by(F.col('WEEKLY_QUANTITY').asc())
        )
            
        df = df.to_pandas()
        df['WEEK'] = df['WEEK'] - pd.Timedelta(days=1)
        df['SUPPLIER_ID'] = df.apply(add_supplier, axis=1)
        df['SUPPLIER_QUANTITY'] = df['WEEKLY_QUANTITY'] #(np.ceil(df['WEEKLY_QUANTITY'] / 10) * 10).astype(int)
        df['DATE_KEY'] = pd.to_datetime(df['WEEK']).dt.strftime('%Y%m%d').astype(int)
        df = df.drop(['WEEK','WEEKLY_QUANTITY','PRODUCT_NAME'], axis=1)
        return df


    def generate_fact_supplier_deliveries(self):
        
        def add_supplier(row):
            supplier_name = np.random.choice(self.supplier_products[row['PRODUCT_NAME']]['suppliers'],p=self.supplier_products[row['PRODUCT_NAME']]['probabilities'])
            return self.suppliers[supplier_name]['SUPPLIER_ID']

        def create_variable_date_buckets(df, min_bucket_size=2, max_bucket_size=4):
            """
            Create DATEBUCKET with variable bucket sizes between min and max.
            """
            df_result = df.copy()
            df_result = df_result.sort_values('DATE').reset_index(drop=True)
            
            # Get unique dates
            unique_dates = sorted(df_result['DATE'].unique())
            
            # Create bucket assignments
            bucket_assignments = {}
            i = 0
            
            while i < len(unique_dates):
                bucket_start = unique_dates[i]
                
                # Determine bucket size
                remaining_dates = len(unique_dates) - i
                if remaining_dates < min_bucket_size:
                    bucket_size = remaining_dates
                else:
                    bucket_size = min(max_bucket_size, 
                                    np.random.randint(min_bucket_size, 
                                                    min(max_bucket_size + 1, remaining_dates + 1)))
                
                # Assign dates to this bucket
                for j in range(bucket_size):
                    if i + j < len(unique_dates):
                        bucket_assignments[unique_dates[i + j]] = bucket_start
                
                i += bucket_size
            
            # Apply bucket assignments
            df_result['DATEBUCKET'] = df_result['DATE'].map(bucket_assignments)
            
            return df_result
            
        df = (
            self.fact_transactions
                .join(self.dim_products, on=['PRODUCT_ID'])
                .join(self.dim_dates, on=['DATE_KEY'])
                .select(['DATE','PRODUCT_NAME','PRODUCT_ID','QUANTITY'])
                .group_by(['DATE','PRODUCT_NAME','PRODUCT_ID'])
                .agg(F.sum('QUANTITY').as_('QUANTITY_DELIVERED'))
                #.filter(F.col('PRODUCT_NAME') == 'Aged Balsamic Reduction')
                .to_pandas()
        )

        df = create_variable_date_buckets(df, min_bucket_size=2, max_bucket_size=4)
        
        df = df.groupby(['DATEBUCKET', 'PRODUCT_NAME', 'PRODUCT_ID'], as_index=False).agg({
            'QUANTITY_DELIVERED': 'sum'
        }).rename(columns={'DATEBUCKET': 'DATE'})
            
        df['DATE'] = df['DATE'] - pd.Timedelta(days=1)
        df['SUPPLIER_ID'] = df.apply(add_supplier, axis=1)
        df['DATE_KEY'] = pd.to_datetime(df['DATE']).dt.strftime('%Y%m%d').astype(int)
        df = df[['DATE_KEY','PRODUCT_ID','SUPPLIER_ID','QUANTITY_DELIVERED']]
        return df
        


    def apply_events_to_revenue(self, df):
        for event in self.events.keys():
            event_data = self.events[event]
            revenue_multiplier = event_data['revenue_multiplier']
            products = event_data['products']
            start_date = event_data['start_date']
            end_date = event_data['end_date']
        
            # adjust revenue data
            mask = (df['DATE'] >= start_date) & (df['DATE'] <= end_date) & (df['PRODUCT_NAME'].isin(products))
            #df.loc[mask, 'PRODUCT_REVENUE'] = df.loc[mask, 'PRODUCT_REVENUE'] * revenue_multiplier
            df['QUANTITY'] = df['QUANTITY'].astype(float)
            df.loc[mask, 'QUANTITY'] = df.loc[mask, 'QUANTITY'] * revenue_multiplier
        df['QUANTITY'] = df['QUANTITY'].astype(int)
        return df


    def apply_events_to_transactions(self, df):
        for event in self.events.keys():
            event_data = self.events[event]
            products = event_data['products']
            start_date = event_data['start_date']
            end_date = event_data['end_date']
            platform_options = event_data['platforms']['options']
            platform_probabilities = np.array(event_data['platforms']['probabilities']) / np.sum(event_data['platforms']['probabilities'])
            session_lengths = event_data['sessions']
        
            # adjust platforms
            mask = (df['DATE_KEY'] >= start_date) & (df['DATE_KEY'] <= end_date) & (df['PRODUCT_NAME'].isin(products))
            num_rows = len(df.loc[mask, 'PLATFORM_NAME'])
            new_platform_names = np.random.choice(platform_options, size = num_rows, p=platform_probabilities)
            new_platforms = [self.platforms[pname] for pname in new_platform_names]
            df.loc[mask, 'PLATFORM_ID'] = new_platforms
            new_session_lengths = np.clip(np.random.normal(session_lengths['mean'], 3, num_rows).astype('int'), session_lengths['min'], session_lengths['max'])
            df.loc[mask, 'SESSION_DURATION'] = new_session_lengths
        return df

    def generate_audio_data(self):
        # Create folder if it does not exist or remove files inside folder if any
        path = Path("/tmp/voice_reviews")
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
        else:
            path.mkdir(parents=True, exist_ok=True)

        # Create a dataset
        dataset = {'filename':[],'text':[]}
        for review in self.customer_reviews['reviews']:
            filename = f"{review['DATE']}_CUSTOMER-REVIEW_{uuid.uuid4()}.wav"
            #dataset[filename] = review['REVIEW_TEXT']
            dataset['text'].append(review['REVIEW_TEXT'])
            dataset['filename'].append(filename)
        dataset = Dataset.from_dict(dataset)
        
        # Load model
        tts_pipe = pipeline("text-to-speech", model="facebook/mms-tts-eng")
        
        # Run model - using zip to iterate through both audio results and filenames
        total_reviews = len(self.customer_reviews['reviews'])
        i = 0
        for speech_result, filename in zip(tts_pipe(KeyDataset(dataset, "text")), dataset['filename']):
            print(f'[Unstructured Data] Generating recording {i}/{total_reviews} ...', end='\r', flush=True)
            scipy.io.wavfile.write(
                f"/tmp/voice_reviews/{filename}", 
                rate=speech_result['sampling_rate'], 
                data=speech_result['audio'].T
            )
            i += 1
        print('')
        print('[Unstructured Data] Uploading recordings to stage ...')
        self.session.file.put(
            '/tmp/voice_reviews/*', 
            stage_location='@AUDIO/CUSTOMER_REVIEWS/', 
            auto_compress=False,
            overwrite=True
        )
        
        self.session.sql('ALTER STAGE AUDIO REFRESH').collect()


    def alter_tables(self, session):
        session.sql('''ALTER TABLE DIM_DATES ADD PRIMARY KEY (DATE_KEY);''').collect()
        session.sql('''ALTER TABLE DIM_PRODUCT_HIERARCHY ADD PRIMARY KEY (CATEGORY_HIER_1_ID, CATEGORY_HIER_2_ID);''').collect()
        session.sql('''ALTER TABLE DIM_PRODUCTS ADD PRIMARY KEY (PRODUCT_ID);''').collect()
        session.sql('''ALTER TABLE DIM_PLATFORMS ADD PRIMARY KEY (PLATFORM_ID);''').collect()
        session.sql('''ALTER TABLE DIM_CUSTOMERS ADD PRIMARY KEY (CUSTOMER_ID);''').collect()
        session.sql('''ALTER TABLE DIM_SUPPLIERS ADD PRIMARY KEY (SUPPLIER_ID);''').collect()
        session.sql('''ALTER TABLE FACT_TRANSACTIONS ADD FOREIGN KEY (CUSTOMER_ID) REFERENCES DIM_CUSTOMERS (CUSTOMER_ID)''').collect()
        session.sql('''ALTER TABLE FACT_TRANSACTIONS ADD FOREIGN KEY (PRODUCT_ID) REFERENCES DIM_PRODUCTS (PRODUCT_ID)''').collect()
        session.sql('''ALTER TABLE FACT_TRANSACTIONS ADD FOREIGN KEY (PLATFORM_ID) REFERENCES DIM_PLATFORMS (PLATFORM_ID)''').collect()
        session.sql('''ALTER TABLE FACT_TRANSACTIONS ADD FOREIGN KEY (DATE_KEY) REFERENCES DIM_DATES (DATE_KEY)''').collect()
        session.sql('''ALTER TABLE FACT_SUPPLIER_DELIVERIES ADD FOREIGN KEY (DATE_KEY) REFERENCES DIM_DATES (DATE_KEY)''').collect()

    def generate_data(self, start_date, end_date):
        print('[Unstructured Data] Generating data ...')
        # Generate audio data
        self.generate_audio_data()
        print('[Unstructured Data] Done!')

        print('[Structured Data] Generating data ...')
        self.session.read.parquet(path='@__DATA/__CUSTOMER_REVIEWS.parquet').write.save_as_table('__CUSTOMER_REVIEWS', mode='overwrite')
        self.session.read.parquet(path='@__DATA/__SENTIMENTS_CUSTOMER_REVIEWS.parquet').write.save_as_table('__SENTIMENTS_CUSTOMER_REVIEWS', mode='overwrite')
        self.session.read.parquet(path='@__DATA/__SENTIMENTS_PRODUCTS_CUSTOMER_REVIEWS.parquet').write.save_as_table('__SENTIMENTS_PRODUCTS_CUSTOMER_REVIEWS', mode='overwrite')
        self.generate_dim_date(start_date,end_date)
        dim_suppliers = self.generate_dim_suppliers()
        
        self.dim_dates = self.session.table('DIM_DATES')
        product_category_revenue_df = self.generate_revenue_categories(start_date, end_date)
        product_subcategory_revenue_df = self.generate_revenue_subcategories(product_category_revenue_df)
        facts_product_revenue_df = self.generate_facts_revenue_products(product_subcategory_revenue_df)
        facts_product_revenue_df = self.apply_events_to_revenue(facts_product_revenue_df)
        
        dim_product_hierarchy_df = self.generate_dim_product_hierarchy(facts_product_revenue_df[['CATEGORY_HIER_1_NAME','CATEGORY_HIER_2_NAME']].drop_duplicates())
        dim_products_df = self.generate_dim_products(facts_product_revenue_df, dim_product_hierarchy_df)
        dim_customers_df = self.generate_dim_customers()
        dim_platforms_df = pd.DataFrame([(self.platforms[key], key) for key in self.platforms.keys()], columns=['PLATFORM_ID','PLATFORM_NAME'])
        
        fact_transactions_df = self.generate_transactions(facts_product_revenue_df)
        fact_transactions_df = self.apply_events_to_transactions(fact_transactions_df)
        fact_transactions_df = fact_transactions_df.merge(dim_products_df[['PRODUCT_ID','PRODUCT_NAME']], on=['PRODUCT_NAME'])
        fact_transactions_df = fact_transactions_df[['DATE_KEY','CUSTOMER_ID','PRODUCT_ID','PLATFORM_ID','QUANTITY','SESSION_DURATION']]
        fact_transactions_df['DATE_KEY'] = pd.to_datetime(fact_transactions_df['DATE_KEY']).dt.strftime('%Y%m%d').astype(int)

        # Write data to Snowflake
        dim_product_hierarchy_df.index = pd.RangeIndex(start=0, stop=len(dim_product_hierarchy_df.index), step=1)
        self.dim_product_hierarchy = self.session.write_pandas(dim_product_hierarchy_df,table_name='DIM_PRODUCT_HIERARCHY', overwrite=True, auto_create_table=True, use_logical_type=True, parallel=50)
        self.dim_products = self.session.write_pandas(dim_products_df,table_name='DIM_PRODUCTS', overwrite=True, auto_create_table=True, use_logical_type=True, parallel=50)
        self.dim_platforms = self.session.write_pandas(dim_platforms_df,table_name='DIM_PLATFORMS', overwrite=True, auto_create_table=True, use_logical_type=True, parallel=50)
        self.dim_customers = self.session.write_pandas(dim_customers_df,table_name='DIM_CUSTOMERS', overwrite=True, auto_create_table=True, use_logical_type=True, parallel=50)
        self.dim_suppliers = self.session.write_pandas(dim_suppliers,table_name='DIM_SUPPLIERS', overwrite=True, auto_create_table=True, use_logical_type=True, parallel=50)
        self.fact_transactions = self.session.write_pandas(fact_transactions_df,table_name='FACT_TRANSACTIONS', overwrite=True, auto_create_table=True, use_logical_type=True, parallel=50)
        self.dim_dates = self.session.table('DIM_DATES')
        self.customer_reviews = self.session.table('__CUSTOMER_REVIEWS')

        fact_supplier_deliveries = self.generate_fact_supplier_deliveries()
        self.fact_supplier_deliveries = self.session.write_pandas(fact_supplier_deliveries,table_name='FACT_SUPPLIER_DELIVERIES', overwrite=True, auto_create_table=True, use_logical_type=True, parallel=50)
        
        # Alter tables to add primary keys and foreign keys
        self.alter_tables(self.session)

        # View creation
        with open(f'data_generation/02_views/stock_levels.sql', 'r') as f :
            self.session.sql(f.read()).collect()
        self.fact_daily_stock_levels = self.session.table('FACT_DAILY_STOCK_LEVELS')
        print('[Structured Data] Done!')
        return