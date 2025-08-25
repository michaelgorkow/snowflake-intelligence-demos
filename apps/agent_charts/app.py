"""
Main application file for the Agent Charts application.

This is a Streamlit multi-page application for viewing and managing
AI-generated charts. Users can search, favorite, and explore charts
created by the AI agent system.

The application provides:
- Chart search functionality
- Recent charts view
- Most favorited charts
- Personal chart management (created charts and favorites)
- Detailed chart view with metadata and specifications
"""

import streamlit as st
from session_manager import get_session_manager
from config import UI_CONFIG

# Configure Streamlit page
st.set_page_config(
    page_title=UI_CONFIG["page_title"],
    layout=UI_CONFIG["layout"],
    page_icon="📊"
)

# Initialize session manager (this handles all data loading and session setup)
session_manager = get_session_manager()

# Define navigation structure
pages = {
    "🌐 Community": [
        st.Page("pages/search.py", title="Search Charts", icon="🔍"),
        st.Page("pages/most_recent.py", title="Recent Charts", icon="📅"),
        st.Page("pages/most_favorites.py", title="Top Favorites", icon="⭐"),
    ],
    "👤 Personal": [
        st.Page("pages/my_favorites.py", title="My Favorites", icon="❤️"),
        st.Page("pages/created_by_me.py", title="My Creations", icon="🎨"),
        st.Page("pages/chart_details.py", title="Chart Details", icon="📊"),
    ],
}

# Create navigation and run the app
pg = st.navigation(pages)
pg.run()