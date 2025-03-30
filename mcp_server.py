# server.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from loguru import logger
from mcp.server.fastmcp import FastMCP
from urllib.parse import quote_plus
# Load environment variables
load_dotenv()

# Database configuration
password = quote_plus(os.getenv('POSTGRES_PASSWORD'))
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{password}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
print(DATABASE_URL)

# Create engine and session factory
try:
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Successfully connected to PostgreSQL database")
except Exception as e:
    logger.error(f"Error connecting to PostgreSQL database: {e}")
    raise

# Create an MCP server
mcp = FastMCP("Demo")

@mcp.tool()
def query_data(sql: str) -> str:
    """Execute SQL queries safely"""
    logger.info(f"Executing SQL query: {sql}")
    db = SessionLocal()
    try:
        # Execute the query
        result = db.execute(text(sql))
        db.commit()
        
        # Check if the query returns rows (like SELECT)
        if result.returns_rows:
            rows = result.fetchall()
            return "\n".join(str(row) for row in rows)
        else:
            # For CREATE, INSERT, UPDATE, DELETE statements
            return "Query executed successfully"
            
    except Exception as e:
        db.rollback()
        logger.error(f"Query error: {e}")
        return f"Error: {str(e)}"
    finally:
        db.close()

@mcp.prompt()
def example_prompt(code: str) -> str:
    return f"Please review this code:\n\n{code}"

if __name__ == "__main__":
    print("Starting server...")
    # Initialize and run the server
    mcp.run(transport="stdio")