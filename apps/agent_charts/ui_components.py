"""
UI components module for the Agent Charts application.
Contains reusable Streamlit components and styling utilities.
"""

import streamlit as st
from datetime import datetime
from config import CHART_STYLES


def create_metadata_card(icon: str, text: str) -> str:
    """
    Create a styled metadata card with an icon and text.
    
    Args:
        icon: Emoji or icon to display
        text: Text content for the card
    
    Returns:
        str: HTML string for the metadata card
    """
    style = CHART_STYLES["metadata_card"]
    return f"""
    <div style="
        text-align: center; 
        padding: {style['padding']}; 
        background: {style['background']}; 
        border-radius: {style['border_radius']}; 
        margin: 2px; 
        border: 1px solid {style['background']};
        box-shadow: {style['box_shadow']};
    ">
        <span style="
            font-size: 12px; 
            color: {style['color']}; 
            font-weight: 500;
            white-space: nowrap; 
            overflow: hidden; 
            text-overflow: ellipsis; 
            display: block;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
        ">{icon} {text}</span>
    </div>
    """


def display_chart_metadata(user_name: str, semantic_view: str, timestamp: datetime, favorite_count: int):
    """
    Display chart metadata in a formatted row.
    
    Args:
        user_name: Name of the chart creator
        semantic_view: Semantic view name
        timestamp: Chart creation timestamp
        favorite_count: Number of favorites for this chart
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metadata_card("👤", user_name), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metadata_card("📊", semantic_view), unsafe_allow_html=True)
    
    with col3:
        ts = timestamp.strftime("%Y-%m-%d %H:%M")
        st.markdown(create_metadata_card("📅", ts), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metadata_card("⭐", str(favorite_count)), unsafe_allow_html=True)


def display_question_card(question: str):
    """
    Display the original question in a styled card.
    
    Args:
        question: The original question text
    """
    style = CHART_STYLES["question_card"]
    st.markdown(f"""
    <div style="
        padding: {style['padding']}; 
        background-color: {style['background']}; 
        border-left: {style['border_left']}; 
        border-radius: {style['border_radius']}; 
        margin: 10px 0;
    ">
        <p style="margin: 0; font-size: 16px; font-style: italic;">"{question}"</p>
    </div>
    """, unsafe_allow_html=True)


def create_action_buttons(page: str, chart_uuid: str, is_favorite: bool) -> tuple[bool, bool]:
    """
    Create action buttons for chart details and favorite toggle.
    
    Args:
        page: Current page identifier
        chart_uuid: UUID of the chart
        is_favorite: Whether the chart is currently favorited
    
    Returns:
        tuple: (details_clicked, favorite_clicked)
    """
    col1, col2 = st.columns(2)
    
    with col1:
        details_clicked = st.button(
            "📋 Chart Details", 
            key=f"{page}_{chart_uuid}_chart_details", 
            use_container_width=True, 
            type="secondary"
        )
    
    with col2:
        button_text = "❌ Remove from Favorites" if is_favorite else "⭐ Add to Favorite"
        favorite_clicked = st.button(
            button_text, 
            key=f"{page}_{chart_uuid}_favorite_toggle", 
            use_container_width=True, 
            type="primary"
        )
    
    return details_clicked, favorite_clicked


def display_expandable_section(title: str, content, content_type: str = "text", expanded: bool = False):
    """
    Display content in an expandable section.
    
    Args:
        title: Title for the expandable section
        content: Content to display (DataFrame, str, dict, etc.)
        content_type: Type of content ('dataframe', 'code', 'json', 'text')
        expanded: Whether to show expanded by default
    """
    with st.expander(title, expanded=expanded):
        if content_type == "dataframe":
            if content is not None and not content.empty:
                st.dataframe(content, use_container_width=True)
            else:
                st.info("No data available")
        elif content_type == "code":
            st.code(content, language='sql')
        elif content_type == "json":
            st.json(content)
        else:
            st.write(content)


def display_two_column_layout(items: list, render_function):
    """
    Display items in a two-column layout.
    
    Args:
        items: List of items to display
        render_function: Function to render each item
    """
    col1, col2 = st.columns(2)
    
    for counter, item in enumerate(items):
        if counter % 2 == 0:
            with col1:
                render_function(item, counter)
        else:
            with col2:
                render_function(item, counter)


def show_error_message(message: str):
    """
    Display a standardized error message.
    
    Args:
        message: Error message to display
    """
    st.error(f"❌ {message}")


def show_success_message(message: str):
    """
    Display a standardized success message.
    
    Args:
        message: Success message to display
    """
    st.success(f"✅ {message}")


def show_info_message(message: str):
    """
    Display a standardized info message.
    
    Args:
        message: Info message to display
    """
    st.info(f"ℹ️ {message}")


def show_loading_spinner(text: str = "Loading..."):
    """
    Display a loading spinner with text.
    
    Args:
        text: Loading text to display
    """
    return st.spinner(text) 