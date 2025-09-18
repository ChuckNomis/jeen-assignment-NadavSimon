"""
RAG Tool - just search and return top 3 chunks
"""

import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from langchain.tools import tool

# Disable ChromaDB telemetry to avoid warnings
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Try to load from multiple possible locations
load_dotenv('../.env')
load_dotenv('.env')


def get_collection():
    client = chromadb.PersistentClient(path="./data/chroma_db")
    embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    )
    return client.get_collection("ai_assistant_docs", embedding_function=embedding_fn)


@tool
def search_documents(query: str) -> str:
    """
    Search the vector database for relevant documents based on a user query.

    Args:
        query (str): The user's search query.

    Returns:
        str: A JSON string containing the top 3 most relevant document chunks with their metadata.
             Returns an error message if no documents are found or an exception occurs.
    """
    try:
        collection = get_collection()

        # Get top 3 similar documents with metadata
        results = collection.query(
            query_texts=[query],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )

        if not results.get("documents") or not results["documents"][0]:
            return '{"error": "No relevant documents found."}'

        # 1. Define a relevance score threshold
        # ChromaDB's distance is often L2 or cosine. For cosine, score = 1 - distance.
        # A lower distance is better. A score > 0.7 is generally considered good.
        relevance_threshold = 0.3

        # 2. Filter results based on the threshold and format them
        formatted_chunks = []
        for i, (chunk, metadata, distance) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0] if results.get("metadatas") else [{}],
            results["distances"][0] if results.get("distances") else [0.0]
        )):
            similarity_score = round(
                1 - distance, 3) if distance is not None else 0.0

            if similarity_score >= relevance_threshold:
                source = metadata.get('source_file', 'Unknown document')
                formatted_chunks.append({
                    "chunk_id": i + 1,
                    "content": chunk,
                    "source": source
                })

        # 3. Handle case where no documents met the threshold
        if not formatted_chunks:
            return '{"error": "No relevant documents found that meet the relevance threshold."}'

        import json
        return json.dumps(formatted_chunks, indent=2)

    except Exception as e:
        import json
        return json.dumps({"error": f"An error occurred during search: {str(e)}"}, indent=2)
