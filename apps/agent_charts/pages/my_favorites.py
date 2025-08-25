"""
My favorites page for the Agent Charts application.
Displays charts that the current user has favorited.
"""

import streamlit as st
from chart_service import ChartVisualizationService

# Initialize chart service
chart_service = ChartVisualizationService()

# Page title
st.title('❤️ My Favorite Charts')

# Get current user from session state
current_user = st.session_state.get('current_user', '')

# Render user's favorite charts
chart_service.render_user_favorite_charts(current_user)