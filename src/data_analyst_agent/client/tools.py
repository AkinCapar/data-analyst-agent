import sqlite3
import pandas as pd
from langchain_core.tools import tool
import os
import matplotlib.pyplot as plt

DB_PATH = "data/superstore.db"

@tool
def get_database_schema() -> str:
    """
    Returns the schema of the SQLite database.
    Use this tool FIRST to understand the table names, column names, and data types
    before writing any SQL queries.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        schemas = cursor.fetchall()
        conn.close()
        
        if not schemas:
            return "No tables found in the database."
            
        schema_text = "\n\n".join([schema[0] for schema in schemas if schema[0]])
        return f"Database Schema:\n{schema_text}"
        
    except Exception as e:
        return f"Error retrieving schema: {str(e)}"

@tool
def execute_sql_query(query: str) -> str:
    """
    Executes a SELECT SQL query against the database and returns the results.
    Input MUST be a valid SQLite SELECT query. 
    Use this tool to fetch data to answer the user's question.
    """
    if not query.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed. You cannot modify the database."
        
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            return "The query executed successfully, but returned no results."
            
        if len(df) > 50:
            df_preview = df.head(50)
            return f"Result is too large ({len(df)} rows). Showing first 50 rows:\n{df_preview.to_markdown(index=False)}"
            
        return df.to_markdown(index=False)
        
    except Exception as e:        
        return f"SQL Execution Error: {str(e)}\nPlease fix your SQL query and try again."
    


@tool
def execute_python_chart_code(sql_query: str, python_code: str) -> str:
    """
    Executes a SQL query to fetch data, then runs the provided Python code to generate a chart.
    
    The Python code is executed in a RESTRICTED environment where ONLY:
    - 'df' (the pandas DataFrame containing the SQL results)
    - 'plt' (matplotlib.pyplot)
    are available. So do not use this tool if you are not generating a plt chart.
    
    RULES for writing the python_code:
    1. Do NOT import pandas or matplotlib. They are already provided.
    2. Use the 'df' variable to plot your data.
    3. You MUST save the final figure using exactly: plt.savefig('output/latest_chart.png', bbox_inches='tight')
    4. Always clear the figure at the end using: plt.clf()
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        
        if df.empty:
            return "Error: The SQL query returned no data. Cannot draw chart."
        os.makedirs("output", exist_ok=True)
        
        chart_path = "output/latest_chart.png"
        if os.path.exists(chart_path):
            os.remove(chart_path)
            
        safe_globals = {
            "__builtins__": {}, 
            "plt": plt,
            "df": df
        }
        
        exec(python_code, safe_globals)
        
        if os.path.exists(chart_path):
            return f"SUCCESS: Chart successfully generated and saved at '{chart_path}'. Tell the user to look at the screen."
        else:
            return "Error: Python code ran successfully, but the image was not saved. Did you forget to call plt.savefig('output/latest_chart.png')?"
            
    except Exception as e:
        return f"Python Execution Error: {str(e)}\nPlease fix your python_code and try again."