"""
Main FastAPI application for the AI Multi-Search Assistant.
"""
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools.rag_search import search_documents
from tools.db_tool import query_database
import logging
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env file in the `server` directory
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Multi-Search Assistant",
    description="Simple agent with RAG document search",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global AgentExecutor
agent_executor: Optional[AgentExecutor] = None


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    query: str
    result: str
    tools_used: list = []
    context_chunks: list = []
    db_results: list = []


@app.on_event("startup")
async def startup():
    """Initialize the AgentExecutor."""
    global agent_executor

    try:
        # Check API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is required in the .env file")

        # 1. Define the LLM and Tools
        llm = ChatOpenAI(model=os.getenv(
            "MAIN_LLM_MODEL", "gpt-4o"), temperature=0.1)
        tools = [search_documents, query_database]

        # 2. Create the Agent Prompt
        # This is the agent's "brain" and tells it how to behave.
        prompt = ChatPromptTemplate.from_messages([
            ("system", """
You are a powerful and helpful AI assistant. Your primary goal is to answer the user's question directly using your own knowledge.

However, you have access to specialized tools for specific types of queries. You should only use these tools when the user's question is clearly about one of the following topics:

1.  **`search_documents`**: Use this tool ONLY for questions about AI, technology policy.
2.  **`query_database`**: Use this tool ONLY for questions about specific users, their account details, balances, or status.

For all other questions (e.g., greetings, jokes, general knowledge), answer directly without using any tools.

**Crucially, when you do use a tool, you MUST base your final answer exclusively on the information returned by that tool.** Do not add any information from your own knowledge. If the context from the tool is not sufficient, state that the answer could not be found in the provided documents or database.
"""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # 3. Create the Agent
        # This binds the LLM, prompt, and tools together into a runnable agent.
        agent = create_openai_tools_agent(llm, tools, prompt)

        # 4. Create the AgentExecutor
        # This is the runtime that will execute the agent's logic.
        # verbose=True will print the agent's thoughts to the console.
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

        logger.info("✅ AI Agent Executor ready!")

    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AI assistant. The AgentExecutor will handle the tool orchestration.
    """
    global agent_executor
    try:
        if not agent_executor:
            raise HTTPException(status_code=503, detail="Assistant not ready")

        logger.info(f"💬 Query: {request.query}")

        # The AgentExecutor handles the full conversation flow
        response = agent_executor.invoke({"input": request.query})

        # --- Extract data from the response ---
        final_answer = response.get(
            "output", "I apologize, but I encountered an error.")
        tools_used = []
        context_chunks = []
        db_results = []

        # Extract context data from the intermediate steps
        if "intermediate_steps" in response and response["intermediate_steps"]:
            for step in response["intermediate_steps"]:
                action, observation = step
                tools_used.append(action.tool)

                # The observation is the raw JSON string from our tools
                data = json.loads(observation)

                if action.tool == "search_documents":
                    context_chunks.extend(
                        data if isinstance(data, list) else [])
                elif action.tool == "query_database":
                    db_results.extend(data if isinstance(data, list) else [])

        return ChatResponse(
            query=request.query,
            result=final_answer,
            tools_used=tools_used,
            context_chunks=context_chunks,
            db_results=db_results
        )

    except Exception as e:
        logger.error(f"❌ Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """API info."""
    return {
        "message": "AI Multi-Search Assistant",
        "docs": "/docs",
        "chat": "/api/chat",
        "description": "Send questions to /api/chat - I'll search documents when needed!"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
