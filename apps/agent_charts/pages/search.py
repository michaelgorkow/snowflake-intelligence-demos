"""
Search page for the Agent Charts application.
Allows users to search for charts using text queries.
"""

import streamlit as st
from chart_service import ChartVisualizationService

# Initialize chart service
chart_service = ChartVisualizationService()

# Page title
st.title('🔍 Search Charts')

# Search input
search_query = st.text_input(
    "Search for a chart", 
    key="search_query",
    placeholder="Enter keywords to search for charts..."
)

# Render search results
chart_service.render_search_results(search_query)