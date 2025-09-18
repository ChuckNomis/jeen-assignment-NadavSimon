import requests
import json


def run_test():
    """Sends test queries to the running FastAPI server."""
    url = "http://localhost:8000/api/chat"
    headers = {"Content-Type": "application/json"}

    # --- Test 1: Query designed to trigger the RAG tool ---
    rag_query = "What are the main risks associated with artificial intelligence?"
    print(f"--- Sending RAG query ---\nQuery: {rag_query}\n")

    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps({"query": rag_query}))
        response.raise_for_status()
        print("--- RAG Agent Response ---")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        handle_error(e)

    # --- Test 2: Query designed for a direct LLM answer (no tools) ---
    direct_query = "Tell me a short joke about programming."
    print(f"\n--- Sending Direct query ---\nQuery: {direct_query}\n")

    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps({"query": direct_query}))
        response.raise_for_status()
        print("--- Direct Agent Response ---")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        handle_error(e)

 # --- Test 3: Query designed for a db answer
    direct_query = "give me all the emails of the users that are active."
    print(f"\n--- Sending db query ---\nQuery: {direct_query}\n")

    try:
        response = requests.post(url, headers=headers,
                                 data=json.dumps({"query": direct_query}))
        response.raise_for_status()
        print("--- db Agent Response ---")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        handle_error(e)


def handle_error(e):
    """Handles connection errors for the test script."""
    print(f"\n--- ERROR ---")
    print(f"Failed to connect to the server: {e}")
    print("Please ensure the FastAPI server is running in a separate terminal via 'python main.py'")


if __name__ == "__main__":
    run_test()
