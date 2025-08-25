# Agent Charts Application

A Streamlit multi-page application for viewing and managing AI-generated charts. Users can search, favorite, and explore charts created by the AI agent system.

## Architecture

The application has been restructured with a clean separation of concerns:

### Core Modules

- **`app.py`** - Main application entry point with navigation setup
- **`config.py`** - Centralized configuration for database, UI, and styling settings
- **`session_manager.py`** - Manages Snowflake sessions and application state initialization
- **`data_service.py`** - Data access layer for chart operations and database interactions
- **`chart_service.py`** - Business logic for chart visualization and rendering
- **`ui_components.py`** - Reusable UI components and styling utilities

### Pages

All pages in the `pages/` directory are now simplified and use the service layer:

- **`search.py`** - Chart search functionality
- **`most_recent.py`** - Display latest charts
- **`most_favorites.py`** - Show most favorited charts
- **`my_favorites.py`** - User's favorite charts
- **`created_by_me.py`** - Charts created by current user
- **`chart_details.py`** - Detailed chart view with metadata

## Features

- 🔍 **Chart Search** - Full-text search using Snowflake Cortex Search
- 📅 **Recent Charts** - View the latest generated charts
- ⭐ **Favorites System** - Save and manage favorite charts
- 👤 **Personal Views** - See your own charts and favorites
- 📊 **Detailed View** - Explore chart specifications, SQL queries, and data

## Key Improvements

1. **Modular Architecture** - Clean separation between data, business logic, and UI
2. **Reusable Components** - Consistent styling through shared UI components
3. **Centralized Configuration** - Easy configuration management
4. **Better Error Handling** - Comprehensive error handling throughout the application
5. **Documentation** - Extensive code comments and docstrings
6. **Performance** - Efficient data caching and session management

## Configuration

Database and application settings are centralized in `config.py`. Update the configuration there to modify:

- Database table names
- Connection parameters
- UI settings
- Styling preferences

## Running the Application

```bash
streamlit run app.py
```

Make sure you have the required Snowflake connection and the necessary database tables set up as defined in the configuration. 