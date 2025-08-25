USE ROLE ACCOUNTADMIN;
USE SCHEMA AI_DEVELOPMENT.PUBLIC;

-- Procedure to send an email
CREATE OR REPLACE PROCEDURE send_mail(recipient TEXT, subject TEXT, text TEXT)
RETURNS TEXT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python')
IMPORTS = ('@CUSTOM_TOOLS/send_email.py')
HANDLER = 'send_email.send_email';

GRANT USAGE ON PROCEDURE send_mail(TEXT, TEXT, TEXT) TO ROLE AI_ENGINEER;

-- Procedure to read a webpage and return its text content
CREATE OR REPLACE FUNCTION read_webpage(url TEXT)
RETURNS TEXT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('requests', 'beautifulsoup4')
IMPORTS = ('@CUSTOM_TOOLS/read_webpage.py')
EXTERNAL_ACCESS_INTEGRATIONS = (ai_external_access_integration)
HANDLER = 'read_webpage.read_webpage';

GRANT USAGE ON FUNCTION read_webpage(TEXT) TO ROLE AI_ENGINEER;

-- Tables, procedures and search services for the Chart App 
CREATE OR REPLACE TABLE AGENT_GENERATED_CHARTS (
    CREATION_TIMESTAMP TIMESTAMP,
    USER_NAME VARCHAR(134217728),
    QUESTION VARCHAR(134217728),
    SQL_QUERY VARCHAR,
    CHART_SPEC TEXT,
    SEMANTIC_VIEW_NAME TEXT
);

GRANT INSERT, SELECT ON TABLE AGENT_GENERATED_CHARTS TO ROLE AI_ENGINEER;

CREATE OR REPLACE PROCEDURE save_chart(question TEXT, sql_query TEXT, chart_spec TEXT, SEMANTIC_VIEW_NAME TEXT)
RETURNS TEXT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'save_chart'
AS
$$

def save_chart(session, question: str, sql_query: str, chart_spec: str, semantic_view_name: str) -> str:
    sql_statement = """
INSERT INTO AGENT_GENERATED_CHARTS
SELECT CURRENT_TIMESTAMP(), CURRENT_USER(), ?, ?, ?, ?
"""

    session.sql(sql_statement, params=[question, sql_query, chart_spec, semantic_view_name]).collect()
    return 'Successfully saved chart in table AGENT_GENERATED_CHARTS.'
$$;

GRANT USAGE ON FUNCTION save_chart(TEXT, TEXT, TEXT, TEXT) TO ROLE AI_ENGINEER;

CREATE OR REPLACE TABLE AGENT_GENERATED_CHARTS_FAVORITES (
    CHART_UUID VARCHAR(134217728),
    USER_NAME VARCHAR(134217728)
);
GRANT INSERT, SELECT, DELETE ON TABLE AGENT_GENERATED_CHARTS_FAVORITES TO ROLE AI_ENGINEER;

CREATE OR REPLACE CORTEX SEARCH SERVICE chart_search_service
  ON QUESTION
  ATTRIBUTES CHART_UUID
  WAREHOUSE = AI_WH
  TARGET_LAG = '1 minute'
  EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
  AS (
    SELECT
        QUESTION, CHART_UUID
    FROM AI_DEVELOPMENT.PUBLIC.AGENT_GENERATED_CHARTS
);

GRANT USAGE ON CORTEX SEARCH SERVICE chart_search_service TO ROLE AI_ENGINEER;