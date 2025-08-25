"""
Data service module for the Agent Charts application.
Handles all database operations, chart data processing, and favorites management.
"""

import streamlit as st
import pandas as pd
import json
from typing import List, Dict, Optional, Tuple

from session_manager import get_session_manager
from config import DATABASE_CONFIG, UI_CONFIG


class ChartDataService:
    """Service for handling chart data operations."""
    
    def __init__(self):
        self.session_manager = get_session_manager()
        self.session = self.session_manager.session
    
    @st.cache_data(ttl=600)
    def get_chart_data(_self, sql_query: str) -> pd.DataFrame:
        """
        Execute SQL query and return chart data with caching.
        
        Args:
            sql_query: SQL query to execute
        
        Returns:
            DataFrame: Query results
        """
        try:
            return _self.session.sql(sql_query).to_pandas()
        except Exception as e:
            st.error(f"Failed to execute query: {str(e)}")
            return pd.DataFrame()
    
    def prepare_chart_specification(self, chart_spec: str, sql_query: str) -> Tuple[Dict, pd.DataFrame]:
        """
        Prepare chart specification with data for visualization.
        
        Args:
            chart_spec: JSON chart specification
            sql_query: SQL query to fetch chart data
        
        Returns:
            Tuple of (chart_spec_dict, chart_data)
        """
        try:
            chart_spec_dict = json.loads(chart_spec)
            chart_data = self.get_chart_data(sql_query)
            chart_spec_dict['data'] = chart_data
            return chart_spec_dict, chart_data
        except json.JSONDecodeError as e:
            st.error(f"Invalid chart specification: {str(e)}")
            return {}, pd.DataFrame()
        except Exception as e:
            st.error(f"Failed to prepare chart: {str(e)}")
            return {}, pd.DataFrame()
    
    def get_favorite_count(self, chart_uuid: str) -> int:
        """
        Get the number of favorites for a specific chart.
        
        Args:
            chart_uuid: UUID of the chart
        
        Returns:
            int: Number of favorites
        """
        try:
            favorites_df = st.session_state.get('favorite_charts', pd.DataFrame())
            if favorites_df.empty:
                return 0
            return len(favorites_df[favorites_df['CHART_UUID'] == chart_uuid])
        except Exception:
            return 0
    
    def is_chart_favorited_by_user(self, chart_uuid: str, user_name: str) -> bool:
        """
        Check if a chart is favorited by a specific user.
        
        Args:
            chart_uuid: UUID of the chart
            user_name: Name of the user
        
        Returns:
            bool: True if favorited by user
        """
        try:
            favorites_df = st.session_state.get('favorite_charts', pd.DataFrame())
            if favorites_df.empty:
                return False
            return len(favorites_df[
                (favorites_df['USER_NAME'] == user_name) & 
                (favorites_df['CHART_UUID'] == chart_uuid)
            ]) > 0
        except Exception:
            return False
    
    def toggle_favorite(self, chart_uuid: str, user_name: str) -> bool:
        """
        Toggle favorite status for a chart.
        
        Args:
            chart_uuid: UUID of the chart
            user_name: Name of the user
        
        Returns:
            bool: True if operation was successful
        """
        try:
            is_favorite = self.is_chart_favorited_by_user(chart_uuid, user_name)
            
            if is_favorite:
                # Remove from favorites
                self.session.sql(f"""
                    DELETE FROM {DATABASE_CONFIG['favorites_table']} 
                    WHERE USER_NAME = '{user_name}' AND CHART_UUID = '{chart_uuid}'
                """).collect()
                
                # Update session state
                st.session_state['favorite_charts'] = st.session_state['favorite_charts'][
                    ~((st.session_state['favorite_charts']['USER_NAME'] == user_name) &
                      (st.session_state['favorite_charts']['CHART_UUID'] == chart_uuid))
                ]
                return True
            else:
                # Add to favorites
                self.session.sql(f"""
                    INSERT INTO {DATABASE_CONFIG['favorites_table']} (USER_NAME, CHART_UUID)
                    VALUES ('{user_name}', '{chart_uuid}')
                """).collect()
                
                # Update session state
                new_favorite = pd.DataFrame({
                    'USER_NAME': [user_name],
                    'CHART_UUID': [chart_uuid]
                })
                st.session_state['favorite_charts'] = pd.concat([
                    st.session_state['favorite_charts'], new_favorite
                ], ignore_index=True)
                return True
                
        except Exception as e:
            st.error(f"Error updating favorites: {str(e)}")
            return False
    
    def search_charts(self, query: str, limit: int = None) -> List[Dict]:
        """
        Search for charts using the Cortex search service.
        
        Args:
            query: Search query
            limit: Maximum number of results (default from config)
        
        Returns:
            List of chart UUIDs matching the search
        """
        if not query.strip():
            return []
        
        try:
            search_service = self.session_manager.get_search_service()
            search_limit = limit or UI_CONFIG["search_limit"]
            
            response = search_service.search(
                query=query,
                columns=["CHART_UUID"],
                limit=search_limit
            )
            
            return response.results
        except Exception as e:
            st.error(f"Search failed: {str(e)}")
            return []
    
    def get_charts_by_uuids(self, chart_uuids: List[str]) -> pd.DataFrame:
        """
        Get charts filtered by specific UUIDs, ordered by the provided UUID list.
        
        Args:
            chart_uuids: List of chart UUIDs to filter by (order preserved)
        
        Returns:
            DataFrame: Filtered charts ordered by the provided UUID list
        """
        try:
            charts_df = st.session_state.get('charts', pd.DataFrame())
            if charts_df.empty or not chart_uuids:
                return pd.DataFrame()
            
            # Filter charts that exist in the provided UUIDs
            filtered_charts = charts_df[charts_df['CHART_UUID'].isin(chart_uuids)]
            
            if filtered_charts.empty:
                return pd.DataFrame()
            
            # Create ordering based on the provided chart_uuids list
            # Convert chart_uuids to a categorical with the correct order
            uuid_order = pd.Categorical(filtered_charts['CHART_UUID'], categories=chart_uuids, ordered=True)
            filtered_charts = filtered_charts.assign(uuid_order=uuid_order)
            
            # Sort by the categorical order and drop the helper column
            result = filtered_charts.sort_values('uuid_order').drop('uuid_order', axis=1)
            
            return result
            
        except Exception as e:
            st.error(f"Failed to filter charts: {str(e)}")
            return pd.DataFrame()
    
    def get_most_favorited_charts(self, limit: int = None) -> pd.DataFrame:
        """
        Get charts sorted by favorite count.
        
        Args:
            limit: Maximum number of charts to return
        
        Returns:
            DataFrame: Charts sorted by favorite count
        """
        try:
            charts_df = st.session_state.get('charts', pd.DataFrame())
            favorites_df = st.session_state.get('favorite_charts', pd.DataFrame())
            
            if charts_df.empty:
                return pd.DataFrame()
            
            # Count favorites per chart
            if not favorites_df.empty:
                favorite_counts = favorites_df.groupby('CHART_UUID').size().reset_index(name='FAVORITE_COUNT')
                
                # Merge with charts data
                charts_with_favorites = charts_df.merge(
                    favorite_counts, 
                    on='CHART_UUID', 
                    how='left'
                ).fillna({'FAVORITE_COUNT': 0})
            else:
                charts_with_favorites = charts_df.copy()
                charts_with_favorites['FAVORITE_COUNT'] = 0
            
            # Sort by favorite count descending, then by creation timestamp descending
            result = charts_with_favorites.sort_values(
                ['FAVORITE_COUNT', 'CREATION_TIMESTAMP'], 
                ascending=[False, False]
            )
            
            chart_limit = limit or UI_CONFIG["charts_per_page"]
            return result.head(chart_limit)
            
        except Exception as e:
            st.error(f"Failed to get most favorited charts: {str(e)}")
            return pd.DataFrame()
    
    def get_user_favorite_charts(self, user_name: str) -> pd.DataFrame:
        """
        Get charts favorited by a specific user.
        
        Args:
            user_name: Name of the user
        
        Returns:
            DataFrame: User's favorite charts
        """
        try:
            charts_df = st.session_state.get('charts', pd.DataFrame())
            favorites_df = st.session_state.get('favorite_charts', pd.DataFrame())
            
            if charts_df.empty or favorites_df.empty:
                return pd.DataFrame()
            
            # Get chart UUIDs favorited by user
            user_favorite_uuids = favorites_df[
                favorites_df['USER_NAME'] == user_name
            ]['CHART_UUID'].tolist()
            
            # Filter charts
            return charts_df[
                charts_df['CHART_UUID'].isin(user_favorite_uuids)
            ].sort_values('CREATION_TIMESTAMP', ascending=False)
            
        except Exception as e:
            st.error(f"Failed to get user favorite charts: {str(e)}")
            return pd.DataFrame()
    
    def refresh_all_data(self):
        """Refresh all cached data from the database."""
        self.session_manager.refresh_data()
        # Clear the cache for chart data
        self.get_chart_data.clear() 