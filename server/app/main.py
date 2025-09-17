"""
Simple AI Multi-Search Assistant

Uses LangChain's llm_with_tools for minimal agent functionality.
"""

from tools.rag_search import search_documents
from tools.db_tool import query_database
import logging
import os
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

# Add tools directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment
load_dotenv('../.env')

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

# Global LLM with tools
llm_with_tools = None


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
    """Initialize the LLM with tools."""
    global llm_with_tools

    try:
        # Check API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY required")

        # Initialize LLM
        llm = ChatOpenAI(
            model=os.getenv("MAIN_LLM_MODEL", "gpt-4o"),
            temperature=0.1
        )

        # Bind tools to LLM
        tools = [search_documents, query_database]
        llm_with_tools = llm.bind_tools(tools)

        logger.info("✅ AI Assistant ready!")

    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the AI assistant."""
    try:
        if not llm_with_tools:
            raise HTTPException(status_code=503, detail="Assistant not ready")

        logger.info(f"💬 Query: {request.query}")

        # Get response from LLM (it will automatically use tools if needed)
        response = llm_with_tools.invoke(request.query)

        # --- Main Agent Logic ---
        final_answer = ""
        context_data = []
        tools_used = []

        # Scenario 1: A tool was called
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tools_used = [call['name'] for call in response.tool_calls]

            # For simplicity, we'll process the first tool call
            tool_call = response.tool_calls[0]
            tool_name = tool_call['name']
            tool_args = tool_call['args']

            if tool_name == 'search_documents':
                raw_result = search_documents.invoke(tool_args)
                context_data = json.loads(raw_result)
                prompt_template = """
                Answer the user's question based on the following document excerpts.
                Keep your answer concise and directly reference the source documents.

                User Question: {query}

                Documents:
                {context}
                """
            elif tool_name == 'query_database':
                raw_result = query_database.invoke(tool_args)
                context_data = json.loads(raw_result)
                prompt_template = """
                Answer the user's question based on the following database query results.
                Format the answer clearly. If the result is a list, present it as a list.

                User Question: {query}

                Database Result:
                {context}
                """

            # Synthesize the final answer using the retrieved data
            synthesis_prompt = prompt_template.format(
                query=request.query, context=json.dumps(context_data, indent=2))
            final_answer_llm = ChatOpenAI(model=os.getenv(
                "MAIN_LLM_MODEL", "gpt-4o"), temperature=0.1)
            final_answer = final_answer_llm.invoke(synthesis_prompt).content

        # Scenario 2: No tool was called, direct answer
        else:
            final_answer = response.content

        return ChatResponse(
            query=request.query,
            result=final_answer,
            context_chunks=context_data if tools_used and tools_used[0] == 'search_documents' else [
            ],
            db_results=context_data if tools_used and tools_used[0] == 'query_database' else [
            ],
            tools_used=tools_used
        )

    except Exception as e:
        logger.error(f"❌ Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "healthy" if llm_with_tools else "not ready",
        "message": "AI Assistant with RAG search"
    }


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
    uvicorn.run(app, host="0.0.0.0", port=8000)
