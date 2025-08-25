"""
Chart service module for the Agent Charts application.
Handles chart visualization, rendering, and display logic.
"""

import streamlit as st
import pandas as pd
from typing import List, Optional

from data_service import ChartDataService
from ui_components import (
    display_chart_metadata, display_question_card, create_action_buttons,
    display_expandable_section, display_two_column_layout, show_info_message,
    show_success_message, show_error_message
)
from config import UI_CONFIG


class ChartVisualizationService:
    """Service for handling chart visualization and rendering."""
    
    def __init__(self):
        self.data_service = ChartDataService()
    
    def render_chart_tile(self, chart_data: pd.Series, page: str, counter: int = 0):
        """
        Render a single chart tile with visualization and metadata.
        
        Args:
            chart_data: Chart data row from DataFrame
            page: Current page identifier
            counter: Chart counter for layout purposes
        """
        chart_uuid = chart_data['CHART_UUID']
        chart_spec = chart_data['CHART_SPEC']
        sql_query = chart_data['SQL_QUERY']
        user_name = chart_data['USER_NAME']
        semantic_view = chart_data['SEMANTIC_VIEW_NAME']
        timestamp = chart_data['CREATION_TIMESTAMP']
        
        # Prepare chart specification with data
        chart_spec_dict, chart_query_data = self.data_service.prepare_chart_specification(
            chart_spec, sql_query
        )
        
        if not chart_spec_dict:
            show_error_message("Failed to load chart specification")
            return
        
        with st.container(border=True):
            # Main chart visualization
            st.vega_lite_chart(spec=chart_spec_dict, use_container_width=True)
            
            # Chart metadata
            favorite_count = self.data_service.get_favorite_count(chart_uuid)
            display_chart_metadata(user_name, semantic_view, timestamp, favorite_count)
            
            # Action buttons
            st.markdown("---")
            current_user = st.session_state.get('current_user', '')
            is_favorite = self.data_service.is_chart_favorited_by_user(chart_uuid, current_user)
            details_clicked, favorite_clicked = create_action_buttons(page, chart_uuid, is_favorite)
            
            # Handle button actions
            if details_clicked:
                st.session_state['selected_chart_uuid'] = chart_uuid
                st.switch_page("pages/chart_details.py")
            
            if favorite_clicked:
                success = self.data_service.toggle_favorite(chart_uuid, current_user)
                if success:
                    action = "removed from" if is_favorite else "added to"
                    show_success_message(f"Chart {action} favorites!")
                    st.rerun()
    
    def render_chart_grid(self, charts_df: pd.DataFrame, page: str = "default"):
        """
        Render charts in a two-column grid layout.
        
        Args:
            charts_df: DataFrame containing chart data
            page: Page identifier for button keys
        """
        if charts_df.empty:
            show_info_message("No charts found.")
            return
        
        # Create list of chart data for two-column layout
        chart_items = [charts_df.iloc[i] for i in range(len(charts_df))]
        
        # Render function for each chart
        def render_chart(chart_data, counter):
            self.render_chart_tile(chart_data, page, counter)
        
        # Display in two-column layout
        display_two_column_layout(chart_items, render_chart)
    
    def render_chart_details(self, chart_uuid: str):
        """
        Render detailed view of a specific chart.
        
        Args:
            chart_uuid: UUID of the chart to display
        """
        # Get chart data
        charts_df = st.session_state.get('charts', pd.DataFrame())
        chart_data = charts_df[charts_df['CHART_UUID'] == chart_uuid]
        
        if chart_data.empty:
            show_error_message("Chart not found!")
            return
        
        chart = chart_data.iloc[0]
        chart_spec = chart['CHART_SPEC']
        sql_query = chart['SQL_QUERY']
        user_name = chart['USER_NAME']
        semantic_view = chart['SEMANTIC_VIEW_NAME']
        timestamp = chart['CREATION_TIMESTAMP']
        question = chart['QUESTION']
        
        # Prepare chart for visualization
        chart_spec_dict, chart_query_data = self.data_service.prepare_chart_specification(
            chart_spec, sql_query
        )
        
        if not chart_spec_dict:
            show_error_message("Failed to load chart specification")
            return
        
        # Main chart visualization
        st.markdown("### 📊 Chart Visualization")
        st.vega_lite_chart(spec=chart_spec_dict, use_container_width=True)
        
        # Chart metadata
        st.markdown("### 📋 Chart Information")
        favorite_count = self.data_service.get_favorite_count(chart_uuid)
        display_chart_metadata(user_name, semantic_view, timestamp, favorite_count)
        
        # Original question
        st.markdown("### ❓ Original Question")
        display_question_card(question)
        
        # Expandable sections for additional details
        display_expandable_section(
            "🔍 Click to view SQL query", 
            sql_query, 
            "code", 
            expanded=False
        )
        
        display_expandable_section(
            "📊 Click to view query results", 
            chart_query_data, 
            "dataframe", 
            expanded=False
        )
        
        display_expandable_section(
            "⚙️ Click to view Vega-Lite specification", 
            chart_spec_dict, 
            "json", 
            expanded=False
        )
    
    def render_recent_charts(self, limit: int = None):
        """
        Render the most recent charts.
        
        Args:
            limit: Maximum number of charts to display
        """
        charts_df = st.session_state.get('charts', pd.DataFrame())
        chart_limit = limit or UI_CONFIG["charts_per_page"]
        recent_charts = charts_df.head(chart_limit)
        
        self.render_chart_grid(recent_charts, "most_recent")
    
    def render_most_favorited_charts(self, limit: int = None):
        """
        Render the most favorited charts.
        
        Args:
            limit: Maximum number of charts to display
        """
        most_favorited = self.data_service.get_most_favorited_charts(limit)
        
        if most_favorited.empty:
            show_info_message("No charts have been favorited yet.")
            return
        
        self.render_chart_grid(most_favorited, "most_favorites")
    
    def render_user_charts(self, user_name: str, limit: int = None):
        """
        Render charts created by a specific user.
        
        Args:
            user_name: Name of the user
            limit: Maximum number of charts to display
        """
        user_charts_df = st.session_state.get('my_charts', pd.DataFrame())
        
        if user_charts_df.empty:
            show_info_message("You haven't created any charts yet.")
            return
        
        chart_limit = limit or UI_CONFIG["charts_per_page"]
        limited_charts = user_charts_df.head(chart_limit)
        
        self.render_chart_grid(limited_charts, "my_charts")
    
    def render_user_favorite_charts(self, user_name: str):
        """
        Render charts favorited by a specific user.
        
        Args:
            user_name: Name of the user
        """
        favorite_charts = self.data_service.get_user_favorite_charts(user_name)
        
        if favorite_charts.empty:
            show_info_message(
                "You haven't added any charts to your favorites yet. "
                "Browse charts and click '⭐ Add to Favorite' to see them here!"
            )
            return
        
        self.render_chart_grid(favorite_charts, "favorite_charts")
    
    def render_search_results(self, search_query: str):
        """
        Render search results for charts.
        
        Args:
            search_query: Search query string
        """
        if not search_query.strip():
            # Show all charts if no search query
            charts_df = st.session_state.get('charts', pd.DataFrame())
            self.render_chart_grid(charts_df, "search")
            return
        
        # Perform search
        search_results = self.data_service.search_charts(search_query)
        
        if not search_results:
            show_info_message(f"No charts found for '{search_query}'")
            return
        
        # Extract chart UUIDs from search results
        chart_uuids = [result["CHART_UUID"] for result in search_results]
        
        # Get charts by UUIDs
        filtered_charts = self.data_service.get_charts_by_uuids(chart_uuids)
        
        if filtered_charts.empty:
            show_info_message(f"No charts found for '{search_query}'")
            return
        
        st.info(f"Charts for '{search_query}'")
        self.render_chart_grid(filtered_charts, "search") 