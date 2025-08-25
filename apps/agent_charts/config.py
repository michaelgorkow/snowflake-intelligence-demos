"""
Configuration module for the Agent Charts application.
Centralizes database table names, connection parameters, and app settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_CONFIG = {
    "chart_table": "AI_DEVELOPMENT.PUBLIC.AGENT_GENERATED_CHARTS",
    "favorites_table": "AI_DEVELOPMENT.PUBLIC.AGENT_GENERATED_CHARTS_FAVORITES",
    "chart_search_service": "chart_search_service"
}

def get_connection_params():
    """
    Load Snowflake connection parameters from environment variables.
    
    Required environment variables:
    - SNOWFLAKE_ACCOUNT
    - SNOWFLAKE_USER
    - SNOWFLAKE_PASSWORD
    - SNOWFLAKE_ROLE
    - SNOWFLAKE_WAREHOUSE
    - SNOWFLAKE_DATABASE
    - SNOWFLAKE_SCHEMA
    
    Returns:
        dict: Connection parameters for Snowflake
    """
    return {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    }

# UI Configuration
UI_CONFIG = {
    "page_title": "Agent Generated Charts",
    "layout": "wide",
    "charts_per_page": 20,
    "search_limit": 10
}

# Chart styling configuration
CHART_STYLES = {
    "metadata_card": {
        "background": "#1D84B5",
        "color": "white",
        "border_radius": "8px",
        "padding": "8px 6px",
        "box_shadow": "0 2px 4px rgba(29, 132, 181, 0.2)"
    },
    "question_card": {
        "background": "rgba(83, 162, 190, 0.1)",
        "border_left": "4px solid #176087",
        "border_radius": "5px",
        "padding": "15px"
    }
} 