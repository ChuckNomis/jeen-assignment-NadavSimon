# 🤖 AI Multi-Search Assistant

A powerful AI assistant with RAG (Retrieval-Augmented Generation) capabilities and a modern ChatGPT-like interface. Intelligently chooses between document search, database queries, or direct AI responses.

## 🚀 Quick Setup

### Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **PostgreSQL 15+**
- **OpenAI API Key**

### 1. Environment Setup

Create `.env` file in `server/` directory:

```env
# --- OpenAI Configuration ---
OPENAI_API_KEY=your_openai_api_key_here
MAIN_LLM_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-large
TEXT_TO_SQL_MODEL=gpt-4o

# --- PostgreSQL Database Configuration (defaults) ---
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_assistant
DB_USER=postgres
DB_PASSWORD=postgres123
```

### 2. How to Start the Backend

```bash
cd server

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python config/database_setup.py

# Process documents for search
The documents are already processed and are in the VectorDB

# Start server
python main.py
```

**Backend available at:** `http://localhost:8000`

### 3. How to Start the Frontend

```bash
cd client
npm install
npm start
```

**Frontend available at:** `http://localhost:3000`

### 4. How to Set Up the Database

The system uses PostgreSQL with a simple schema:

````sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    balance NUMERIC(10, 2) DEFAULT 0.00,
    active BOOLEAN DEFAULT TRUE
);



-- Optional: Add sample test data for testing (run manually if needed)
INSERT INTO users (name, email, balance, active) VALUES
('John Doe', 'john.doe@example.com', 1500.50, TRUE),
('Jane Smith', 'jane.smith@example.com', 2750.00, TRUE),
('Bob Johnson', 'bob.johnson@example.com', 500.25, TRUE),
('Alice Brown', 'alice.brown@example.com', 0.00, FALSE),
('Charlie Wilson', 'charlie.wilson@example.com', 3200.75, TRUE)
ON CONFLICT (email) DO NOTHING;

-- Example SQL query to test the database:
SELECT name, email, balance FROM users WHERE active = TRUE ORDER BY balance DESC;



## 🔍 Example Queries to Test

### 📚 Document Search Tool (searches uploaded documents)

- _"What are the different levels of vehicle automation?"_
- _"How can architects incorporate renewable energy into building design?"_
- _"What are the main cybersecurity risks associated with AI systems?"_
- _"For African violet or geranium, which cutting type does the guide recommend and what after‑care steps ensure successful rooting?"_

### 🗄️ Database Tool (queries user database)

- _"What are the emails of the active users?"_
- _"Who has the highest account balance?"_

### 💬 No Tool (direct AI responses)

- _"Tell me a joke"_

## 📚 Knowledge Base

The system includes 8 documents covering:

| Document                                              | Topic               | Description                 |
| ----------------------------------------------------- | ------------------- | --------------------------- |
| `15cpb_autonomousdriving.pdf`                         | Autonomous Vehicles | Self-driving car technology |
| `Autonomous-Vehicles-An-Overview.pdf`                 | Autonomous Vehicles | Vehicle systems overview    |
| `Architects_Primer_Renewable_Energy.pdf`              | Renewable Energy    | Energy integration guide    |
| `WLW_Renewable-Energy-Primer_Final.pdf`               | Renewable Energy    | Energy systems              |
| `WEF_Artificial_Intelligence_and_Cybersecurity_*.pdf` | AI & Cybersecurity  | Security risks/rewards      |
| `Propagating-and-Growing-House-Plants.pdf`            | Plant Care          | Plant propagation guide     |
| `kegr103.pdf`                                         | Technical           | Engineering specs           |
| `3f4e3dfb-en.pdf`                                     | Technical           | Reference material          |

## 🛠️ API

### Main Endpoint: `POST /api/chat`

```json
{
  "query": "What are the main AI safety concerns?"
}
````

**Response:**

```json
{
  "query": "What are the main AI safety concerns?",
  "result": "Based on the documents...",
  "tools_used": ["search_documents"],
  "context_chunks": [...],
  "db_results": [...]
}
```

### Interactive Docs: `http://localhost:8000/docs`

---

**Built with FastAPI, React, and LangChain**
