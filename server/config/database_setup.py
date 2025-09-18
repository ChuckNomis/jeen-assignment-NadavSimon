"""
Database setup script for AI Multi-Search Assistant
Sets up PostgreSQL database with users table schema.
"""

import os
import psycopg
from pathlib import Path
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database_and_schema():
    """
    Create the database and set up the schema using the provided SQL file.
    """

    # Database configuration
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'user': os.getenv('DB_USER', 'postgres'),  # Default PostgreSQL user
        # You'll need to set this
        'password': os.getenv('DB_PASSWORD', 'postgres123'),
        'dbname': 'postgres'  # Connect to default database first
    }

    target_db = os.getenv('DB_NAME', 'ai_assistant')

    try:
        # Connect to PostgreSQL (to the default 'postgres' database)
        logger.info("Connecting to PostgreSQL...")
        with psycopg.connect(**db_config) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:

                # Check if database exists
                cur.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s", (target_db,))
                if not cur.fetchone():
                    # Create the database
                    logger.info(f"Creating database: {target_db}")
                    cur.execute(f"CREATE DATABASE {target_db}")
                    logger.info(
                        f"✅ Database '{target_db}' created successfully")
                else:
                    logger.info(f"Database '{target_db}' already exists")

        # Connect to the new database and create schema
        db_config['dbname'] = target_db
        logger.info(f"Connecting to {target_db} database...")

        with psycopg.connect(**db_config) as conn:
            with conn.cursor() as cur:

                # Read and execute the schema SQL
                schema_file = Path(__file__).parent / 'schema.sql'
                logger.info(f"Reading schema from: {schema_file}")

                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()

                # Execute the schema
                logger.info("Creating tables and inserting sample data...")
                cur.execute(schema_sql)
                conn.commit()

                # Verify the setup
                cur.execute("SELECT to_regclass('public.users')")
                table_exists = cur.fetchone()[0]

                if table_exists:
                    logger.info("✅ Schema setup complete!")
                    logger.info("✅ Users table created successfully.")
                else:
                    logger.error(
                        "❌ Schema setup failed: 'users' table not found.")
                    return False

                return True

    except psycopg.Error as e:
        logger.error(f"❌ Database error: {e}")
        return False
    except FileNotFoundError:
        logger.error(f"❌ Schema file not found: {schema_file}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


def test_connection():
    """Test the database connection and query some data."""

    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 5432)),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'postgres123'),
        'dbname': os.getenv('DB_NAME', 'ai_assistant')
    }

    try:
        logger.info("Testing database connection...")
        with psycopg.connect(**db_config) as conn:
            with conn.cursor() as cur:

                # Test query
                cur.execute("""
                    SELECT name, email, balance 
                    FROM users 
                    WHERE active = TRUE 
                    ORDER BY balance DESC
                """)

                active_users = cur.fetchall()

                logger.info("✅ Database connection successful!")
                logger.info(f"Found {len(active_users)} active users:")

                for user in active_users:
                    name, email, balance = user
                    logger.info(f"   - {name}: ${balance}")

                return True

    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        return False


if __name__ == "__main__":
    print("🗄️  Setting up PostgreSQL database for AI Multi-Search Assistant")
    print("=" * 60)

    print("\n1. Creating database and schema...")
    if create_database_and_schema():
        print("\n2. Testing connection...")
        if test_connection():
            print("\n🎉 Database setup completed successfully!")
            print("\n📋 Summary:")
            print(f"   ✅ Database: {os.getenv('DB_NAME', 'ai_assistant')}")
            print("   ✅ Table: users (with 0 sample records)")
            print("   ✅ Connection: Working")
            print("\n🔗 Connection String:")
            user = os.getenv('DB_USER', 'postgres')
            password = os.getenv('DB_PASSWORD', 'postgres123')
            host = os.getenv('DB_HOST', 'localhost')
            port = os.getenv('DB_PORT', 5432)
            dbname = os.getenv('DB_NAME', 'ai_assistant')
            print(f"   postgresql://{user}:{password}@{host}:{port}/{dbname}")
        else:
            print("\n❌ Database setup failed at connection test")
    else:
        print("\n❌ Database setup failed")
