import pytest
from fastapi.testclient import TestClient
from src.main import app, conversation_histories  # Import app and conversation_histories

client = TestClient(app)

def test_conversation_memory():
    # Clear conversation histories for a clean test environment
    conversation_histories.clear()

    # First query
    query1 = "What is a Roth IRA?"
    response1 = client.post("/ask", json={"query": query1, "channel": "test"})
    
    assert response1.status_code == 200
    data1 = response1.json()
    assert "response" in data1
    assert "session_id" in data1
    
    session_id = data1["session_id"]
    response_text1 = data1["response"]

    # Assert that the first response is about Roth IRA
    assert "roth ira" in response_text1.lower()
    assert "tax-free" in response_text1.lower() # Specific detail about Roth IRA

    # Second query, dependent on the first, using the session_id
    query2 = "What are its benefits?"
    response2 = client.post("/ask", json={"query": query2, "channel": "test", "session_id": session_id})
    
    assert response2.status_code == 200
    data2 = response2.json()
    assert "response" in data2
    assert data2["session_id"] == session_id  # Ensure session_id is maintained

    response_text2 = data2["response"]

    # Assert that the second response uses context from the first query
    # It should mention benefits and relate to Roth IRA, not be a generic fallback.
    # Specific keywords to look for indicating contextually aware response about Roth IRA benefits:
    assert "benefits" in query2.lower() # Making sure the query was about benefits
    assert "tax-free" in response_text2.lower() or "withdrawals" in response_text2.lower() or "contributions" in response_text2.lower()
    
    # Check that it's not a generic fallback (which might happen if context is lost)
    assert "don't have specific information" not in response_text2.lower()
    assert "knowledge base" not in response_text2.lower() # common in some fallbacks

    # Check that the conversation history was actually stored and used
    assert session_id in conversation_histories
    assert len(conversation_histories[session_id]) == 2
    assert conversation_histories[session_id][0][0] == query1
    assert conversation_histories[session_id][0][1] == response_text1
    assert conversation_histories[session_id][1][0] == query2
    assert conversation_histories[session_id][1][1] == response_text2

def test_new_session_if_no_id_provided():
    # Clear conversation histories for a clean test environment
    conversation_histories.clear()

    query = "What is a 401k?"
    response = client.post("/ask", json={"query": query, "channel": "test"})

    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    new_session_id = data["session_id"]
    assert new_session_id is not None
    assert new_session_id in conversation_histories
    assert len(conversation_histories[new_session_id]) == 1

def test_ask_endpoint_without_session_id():
    response = client.post("/ask", json={"query": "Hello", "channel": "test"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "session_id" in data # Should generate a new session_id
    assert data["session_id"] is not None

def test_ask_endpoint_with_session_id():
    session_id = "test-session-123"
    conversation_histories[session_id] = [] # Initialize history for this session

    response = client.post("/ask", json={"query": "Hello again", "channel": "test", "session_id": session_id})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["session_id"] == session_id
    assert len(conversation_histories[session_id]) == 1 # History should be updated
    
    # Clean up
    del conversation_histories[session_id]

# A simple root endpoint test to ensure TestClient is working with the app
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Financial AI Agent API. Use /ask endpoint to ask questions."}
