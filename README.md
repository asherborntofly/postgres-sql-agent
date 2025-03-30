# MCP PostgreSQL Agent

> An AI-powered PostgreSQL agent using MCP (Machine Control Protocol) to interact with a PostgreSQL database through natural language.

## Key Features

* Create an AI PostgreSQL agent using MCP
* Interact with PostgreSQL database using natural language
* Use GPT-4 Turbo to generate SQL queries
* Execute SQL queries safely with SQLAlchemy
* Comprehensive error handling and logging

## Tech Stack

* OpenAI GPT-4 Turbo
* LangChain
* MCP (Machine Control Protocol)
* SQLAlchemy
* PostgreSQL
* Python-dotenv
* Loguru

## Getting Started

### Prerequisites

* Python 3.x
* PostgreSQL database
* OpenAI API key
* PostgreSQL database credentials

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your credentials:
```
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=your_host
POSTGRES_PORT=your_port
POSTGRES_DB=your_database
```

### Usage

1. In a separate terminal, run the client:
```bash
python mcp_client.py
```

2. Enter your SQL queries in natural language

Note that you don't need to explicitly run the server, as the client automatically runs it.

## Project Structure

## Implementation Details

### Server (`mcp_server.py`)
* Implements FastMCP server for PostgreSQL interaction
* Provides secure query execution through SQLAlchemy
* Includes comprehensive error handling and logging
* Supports both query and modification operations

### Client (`mcp_client.py`)
* Implements an async chat interface
* Uses GPT-4 Turbo through LangChain
* Maintains chat history for context
* Provides a clean CLI interface

## Environment Variables

* `POSTGRES_USER`: PostgreSQL username
* `POSTGRES_PASSWORD`: PostgreSQL password
* `POSTGRES_HOST`: Database host
* `POSTGRES_PORT`: Database port
* `POSTGRES_DB`: Database name

## Security

* SQL queries are executed safely using SQLAlchemy's text template
* Database credentials are securely managed through environment variables
* Automatic query transaction management with commit/rollback

## License
MIT License
