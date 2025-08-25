"""
Session management module for the Agent Charts application.
Handles Snowflake session creation, connection management, and data initialization.
"""

import streamlit as st
import pandas as pd
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import functions as F
from snowflake.core import Root

from config import DATABASE_CONFIG, get_connection_params


class SessionManager:
    """Manages Snowflake session and application state."""
    
    def __init__(self):
        self.session = self._get_session()
        self.root = Root(self.session)
        self._initialize_session_state()
    
    def _get_session(self) -> Session:
        """
        Get or create a Snowflake session.
        
        Returns:
            Session: Active Snowflake session
        """
        try:
            # Try to get active session first (for production)
            return get_active_session()
        except Exception:
            # Fallback to local connection (for development)
            return Session.builder.configs(get_connection_params()).create()
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state with required data."""
        if 'charts' not in st.session_state:
            st.session_state['charts'] = self._load_charts()
        
        if 'favorite_charts' not in st.session_state:
            st.session_state['favorite_charts'] = self._load_favorites()
        
        if 'my_charts' not in st.session_state:
            st.session_state['my_charts'] = self._load_my_charts()
        
        if 'current_user' not in st.session_state:
            st.session_state['current_user'] = self._get_current_user()
    
    def _load_charts(self) -> pd.DataFrame:
        """Load all charts from the database."""
        try:
            return (self.session.table(DATABASE_CONFIG["chart_table"])
                   .order_by('CREATION_TIMESTAMP')
                   .to_pandas())
        except Exception as e:
            st.error(f"Failed to load charts: {str(e)}")
            return pd.DataFrame()
    
    def _load_favorites(self) -> pd.DataFrame:
        """Load all favorite charts from the database."""
        try:
            return (self.session.table(DATABASE_CONFIG["favorites_table"])
                   .to_pandas())
        except Exception as e:
            st.error(f"Failed to load favorites: {str(e)}")
            return pd.DataFrame()
    
    def _load_my_charts(self) -> pd.DataFrame:
        """Load charts created by the current user."""
        try:
            current_user = self._get_current_user()
            return (self.session.table(DATABASE_CONFIG["chart_table"])
                   .filter(F.col('USER_NAME') == current_user)
                   .order_by('CREATION_TIMESTAMP')
                   .to_pandas())
        except Exception as e:
            st.error(f"Failed to load user charts: {str(e)}")
            return pd.DataFrame()
    
    def _get_current_user(self) -> str:
        """Get the current user name."""
        try:
            return self.session.get_current_user().replace('"', '')
        except Exception as e:
            st.error(f"Failed to get current user: {str(e)}")
            return "unknown_user"
    
    def refresh_data(self):
        """Refresh all session state data from the database."""
        st.session_state['charts'] = self._load_charts()
        st.session_state['favorite_charts'] = self._load_favorites()
        st.session_state['my_charts'] = self._load_my_charts()
    
    def get_search_service(self):
        """Get the Cortex search service for chart searching."""
        return (self.root
                .databases["AI_DEVELOPMENT"]
                .schemas["PUBLIC"]
                .cortex_search_services[DATABASE_CONFIG["chart_search_service"]])


# Global session manager instance
_session_manager = None


def get_session_manager() -> SessionManager:
    """
    Get the global session manager instance.
    
    Returns:
        SessionManager: The global session manager
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager 