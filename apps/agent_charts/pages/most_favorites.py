"""
Most favorited charts page for the Agent Charts application.
Displays charts sorted by the number of favorites they have received.
"""

import streamlit as st
from chart_service import ChartVisualizationService

# Initialize chart service
chart_service = ChartVisualizationService()

# Page title
st.title('⭐ Most Favorited Charts')

# Render most favorited charts
chart_service.render_most_favorited_charts()