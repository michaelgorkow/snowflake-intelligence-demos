"""
Most recent charts page for the Agent Charts application.
Displays the latest charts created in the system.
"""

import streamlit as st
from chart_service import ChartVisualizationService

# Initialize chart service
chart_service = ChartVisualizationService()

# Page title
st.title('📅 Latest Charts')

# Render recent charts
chart_service.render_recent_charts()