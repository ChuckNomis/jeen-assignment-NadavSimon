"""
Database Tool to query the PostgreSQL database.
"""

import os
import json
import psycopg2
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv('../.env')
load_dotenv('.env')

# --- Database Connection ---


def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

# --- Tool Definition ---


@tool
def query_database(natural_language_query: str) -> str:
    """
    Query the PostgreSQL database to answer questions about users, their balances, and account status.

    Args:
        natural_language_query (str): The user's question in plain English.

    Returns:
        str: A JSON string containing the query result or an error message.
    """
    schema = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        balance NUMERIC(10, 2) DEFAULT 0.00,
        active BOOLEAN DEFAULT TRUE
    );
    """

    prompt = f"""
    Based on the following database schema, convert the user's question into a valid PostgreSQL query.
    Only output the SQL query and nothing else.

    Schema:
    {schema}

    User Question: "{natural_language_query}"

    SQL Query:
    """

    try:
        # 1. Generate SQL from the natural language query
        llm = ChatOpenAI(
            model=os.getenv("TEXT_TO_SQL_MODEL", "gpt-4o-mini"),
            temperature=0
        )
        sql_query = llm.invoke(prompt).content.strip()

        # 2. Execute the query
        conn = get_db_connection()
        if not conn:
            return json.dumps({"error": "Failed to connect to the database."})

        cursor = conn.cursor()
        cursor.execute(sql_query)

        column_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # 3. Format and return the results
        if not rows:
            return json.dumps({"result": "Query executed successfully, but no results were found."})

        results = [dict(zip(column_names, row)) for row in rows]
        # Use default=str for decimals
        return json.dumps(results, indent=2, default=str)

    except Exception as e:
        return json.dumps({"error": f"An error occurred: {str(e)}"}, indent=2)
