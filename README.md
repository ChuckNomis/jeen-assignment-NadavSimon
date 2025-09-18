# AI Multi-Search Assistant

A simple AI assistant that answers user questions by intelligently choosing between RAG search, database queries, or direct LLM responses.

## Project Structure

```
jeen-assignment-NadavSimon/
├── server/                 # Backend FastAPI application
│   ├── venv/              # Python virtual environment
│   ├── requirements.txt   # Python dependencies
│   ├── app/              # FastAPI application code (to be created)
│   ├── tools/            # AI tools (RAG, DB, Direct LLM) (to be created)
│   └── config/           # Configuration files (to be created)
├── client/               # React frontend application (to be created)
├── .taskmaster/          # Task Master project management
└── README.md            # This file
```

## Features

- **Agent Controller**: LLM-based tool selection logic
- **RAG Tool**: Document search using semantic similarity with pgvector
- **Database Tool**: Natural language to SQL query conversion
- **Direct LLM**: Direct responses from the language model
- **Response Synthesis**: Consistent conversational output

## Setup

### Server (Backend)

1. Navigate to the server directory:

   ```bash
   cd server
   ```

2. Activate the virtual environment:

   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1

   # Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies (already done):
   ```bash
   pip install -r requirements.txt
   ```

### Database Setup

PostgreSQL with pgvector extension is required for vector search capabilities.

### Client (Frontend)

React frontend will be set up in the `client/` directory.

## Development Status

- ✅ Project structure setup
- ✅ Python virtual environment
- ✅ Core dependencies installed
- 🔄 PostgreSQL setup (next step)
- ⏳ FastAPI backend development
- ⏳ React frontend development
- ⏳ Integration testing

## Tech Stack

- **Backend**: FastAPI, Python 3.12 (Note: Using 3.12 is recommended to avoid compiling dependencies from source)
- **AI**: OpenAI GPT-4o, LangChain
- **Database**: PostgreSQL with pgvector
- **Frontend**: React (to be set up)
- **Document Processing**: pypdf, python-docx, beautifulsoup4
