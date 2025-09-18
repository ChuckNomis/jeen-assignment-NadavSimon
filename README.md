# 🤖 AI Multi-Search Assistant

A powerful, intelligent AI assistant with RAG (Retrieval-Augmented Generation) capabilities, featuring a modern ChatGPT-like interface. The system intelligently chooses between document search, database queries, or direct AI responses based on user intent.

![Project Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![React](https://img.shields.io/badge/React-19.1.1-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)

## ✨ Features

### 🧠 **Intelligent Tool Selection**

- **Smart Agent**: Uses LangChain agents to automatically choose the best tool for each query
- **Context-Aware**: Understands user intent and routes queries appropriately
- **Multi-Modal Search**: Seamlessly combines document search, database queries, and AI knowledge

### 📚 **Advanced Document Search (RAG)**

- **Vector Database**: ChromaDB with OpenAI embeddings for semantic search
- **6 Premium Documents**: Pre-loaded with AI policy and technology documents
- **Chunk Transparency**: Users can view exact document sources and content used
- **Smart Retrieval**: Returns most relevant document sections with metadata

### 🗄️ **Database Integration**

- **Natural Language to SQL**: Convert questions into database queries
- **PostgreSQL Backend**: Robust relational database with user account data
- **Secure Queries**: Sanitized and validated database operations

### 🎨 **Modern ChatGPT-like Interface**

- **Dark Theme**: Professional, eye-friendly design
- **Real-time Chat**: Instant responses with typing indicators
- **Source Visibility**: Expandable document chunks and database results
- **Mobile Responsive**: Works seamlessly on all devices
- **Tool Usage Display**: Shows which tools were used for transparency

## 🏗️ Architecture

```mermaid
graph TB
    A[React Frontend] --> B[FastAPI Backend]
    B --> C[LangChain Agent]
    C --> D[Document Search Tool]
    C --> E[Database Query Tool]
    C --> F[Direct LLM Tool]
    D --> G[ChromaDB Vector Store]
    E --> H[PostgreSQL Database]
    F --> I[OpenAI GPT-4]
    G --> J[AI Policy Documents]
    H --> K[User Account Data]
```

## 📁 Project Structure

```
jeen-assignment-NadavSimon/
├── 🖥️ client/                    # React frontend application
│   ├── public/                   # Static assets
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── ChatInterface.js  # Main chat container
│   │   │   ├── MessageList.js    # Message display
│   │   │   ├── Message.js        # Individual messages
│   │   │   ├── InputBox.js       # Message input
│   │   │   └── LoadingIndicator.js # Typing animation
│   │   ├── services/
│   │   │   └── api.js           # API communication
│   │   └── App.js               # Main application
│   ├── package.json             # Dependencies
│   └── CLIENT_README.md         # Frontend documentation
├── 🚀 server/                    # FastAPI backend
│   ├── tools/                    # AI tools
│   │   ├── rag_search.py        # Document search tool
│   │   └── db_tool.py           # Database query tool
│   ├── data/
│   │   ├── documents/           # PDF knowledge base
│   │   └── chroma_db/           # Vector database
│   ├── config/
│   │   ├── database_setup.py    # Database initialization
│   │   └── schema.sql           # Database schema
│   ├── main.py                  # FastAPI application
│   ├── process_documents.py     # Document ingestion
│   ├── test_agent.py           # Testing utilities
│   └── requirements.txt         # Python dependencies
├── requirements.txt             # Global dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** (recommended for compatibility)
- **Node.js 18+** and npm
- **PostgreSQL 15+** (for database functionality)
- **OpenAI API Key** (for AI capabilities)

### 1. Environment Setup

Create a `.env` file in the `server/` directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
MAIN_LLM_MODEL=gpt-4o

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/ai_assistant
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_assistant
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

### 2. Backend Setup

```bash
# Navigate to server directory
cd server

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database (if using PostgreSQL)
python config/database_setup.py

# Process documents (creates vector embeddings)
python process_documents.py

# Start the FastAPI server
python main.py
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to client directory
cd client

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 📖 Usage Guide

### 💬 **Chat Interface**

1. **Open your browser** to `http://localhost:3000`
2. **Type your question** in the input box
3. **Press Enter** or click the send button
4. **View the response** with optional source materials

### 🔍 **Query Types**

#### **Document Search Queries**

Ask about AI, technology policy, or related topics:

- _"What are the main AI risks mentioned in the documents?"_
- _"How should AI systems be regulated?"_
- _"What does NIST say about AI safety?"_

#### **Database Queries**

Ask about user accounts, balances, or status:

- _"What's John Doe's account balance?"_
- _"Show me all active users"_
- _"Find users with premium status"_

#### **General Questions**

Ask anything else for direct AI responses:

- _"Explain machine learning"_
- _"What's the weather like?"_
- _"Help me write a Python function"_

### 📋 **Source Transparency**

When document search is used:

1. Click **"Show Sources"** to see retrieved document chunks
2. View **source document names** and **page numbers**
3. Read **exact text content** used to generate the response
4. Verify information directly from the source materials

## 🛠️ API Documentation

### Core Endpoint

#### `POST /api/chat`

Send a message to the AI assistant.

**Request:**

```json
{
  "query": "What are the main AI safety concerns?"
}
```

**Response:**

```json
{
  "query": "What are the main AI safety concerns?",
  "result": "Based on the documents, the main AI safety concerns include...",
  "tools_used": ["search_documents"],
  "context_chunks": [
    {
      "page_content": "AI systems pose several risks...",
      "metadata": {
        "source": "nist.ai.100-1.pdf",
        "page": 15
      }
    }
  ],
  "db_results": []
}
```

#### `GET /`

Get API information and health status.

**Response:**

```json
{
  "message": "AI Multi-Search Assistant",
  "docs": "/docs",
  "chat": "/api/chat",
  "description": "Send questions to /api/chat - I'll search documents when needed!"
}
```

### Interactive API Docs

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

## 📚 Knowledge Base

The system includes 6 high-quality documents on AI and technology policy:

| Document                                                              | Topic                        | Pages |
| --------------------------------------------------------------------- | ---------------------------- | ----- |
| `AI_Opennes.pdf`                                                      | AI Openness and Transparency | 45    |
| `Assessing_Potential_Future_Artificial_Risks.pdf`                     | AI Risk Assessment           | 32    |
| `Future_Of_Social_Protection.pdf`                                     | AI and Social Systems        | 68    |
| `nist.ai.100-1.pdf`                                                   | NIST AI Framework            | 56    |
| `OECD_Final.pdf`                                                      | OECD AI Guidelines           | 78    |
| `WEF_Technology_Policy_Responsible_Design_Flourishing_World_2024.pdf` | Technology Policy            | 92    |

## 🔧 Configuration

### AI Model Settings

Modify the model in `server/main.py`:

```python
llm = ChatOpenAI(
    model=os.getenv("MAIN_LLM_MODEL", "gpt-4o"),
    temperature=0.1
)
```

### Frontend API URL

Update the API endpoint in `client/src/services/api.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";
```

### Document Processing

Add new documents to `server/data/documents/` and run:

```bash
cd server
python process_documents.py
```

## 🧪 Testing

### Backend Tests

```bash
cd server
python test_agent.py
```

### Frontend Tests

```bash
cd client
npm test
```

## 🐛 Troubleshooting

### Common Issues

#### **"Server not available" error**

- Ensure the FastAPI server is running on port 8000
- Check that your OpenAI API key is valid
- Verify the `.env` file is in the `server/` directory

#### **Document search not working**

- Run `python process_documents.py` to rebuild embeddings
- Check that documents exist in `server/data/documents/`
- Verify OpenAI API key has sufficient credits

#### **Database queries failing**

- Ensure PostgreSQL is running
- Check database connection settings in `.env`
- Run `python config/database_setup.py` to initialize

#### **Frontend won't connect**

- Check that both servers are running (port 3000 and 8000)
- Verify CORS settings in `server/main.py`
- Clear browser cache and restart

### Logs and Debugging

- **Backend logs**: Check the FastAPI server console output
- **Frontend logs**: Open browser developer tools
- **Verbose mode**: Set `verbose=True` in the AgentExecutor

## 🚀 Deployment

### Production Backend

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production Frontend

```bash
# Build for production
npm run build

# Serve static files with nginx or your preferred server
```

### Environment Variables

For production, set:

- `REACT_APP_API_URL=https://your-api-domain.com`
- Configure database with connection pooling
- Use environment-specific OpenAI API keys

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

## 📄 License

This project is part of the Jeen Assignment and is intended for educational and demonstration purposes.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the [FastAPI documentation](https://fastapi.tiangolo.com/)
3. Check [LangChain documentation](https://python.langchain.com/)
4. Open an issue in the repository

---

**Built with ❤️ using FastAPI, React, and LangChain**
