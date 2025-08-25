"""
Chart details page for the Agent Charts application.
Displays detailed information about a specific chart including
the original question, SQL query, and chart specification.
"""

import streamlit as st
from chart_service import ChartVisualizationService

# Initialize chart service
chart_service = ChartVisualizationService()

# Page title
st.title('📊 Chart Details')

# Check if a chart has been selected
if 'selected_chart_uuid' not in st.session_state:
    st.error("❌ No chart selected.")
    st.info("Please navigate back and select a chart to view its details.")
else:
    # Render chart details
    chart_service.render_chart_details(st.session_state['selected_chart_uuid'])