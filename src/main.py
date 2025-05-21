# API server (FastAPI) 
##### src/main.py #####
import os
import yaml
import uuid  # Import uuid
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Prevent tokenizers warning

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from pydantic import BaseModel
from src.retrieval import retrieve_relevant_data
from src.fin_engine import generate_response
from src.integrations import send_response_to_channel

app = FastAPI()

# Add CORS middleware to allow browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load config for default values
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

conversation_histories = {}  # Global dictionary to store conversation histories

class QueryRequest(BaseModel):
    query: str
    channel: str  # e.g., "email", "whatsapp", "chat"
    recipient: str = None  # Optional recipient (phone number or email)
    session_id: str = None  # Optional session ID

@app.post("/ask")
def ask(query_request: QueryRequest):
    session_id = query_request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate new session_id if not provided
        conversation_histories[session_id] = []  # Initialize history for new session

    history = conversation_histories.get(session_id, [])

    # Get relevant data from knowledge base
    relevant_data = retrieve_relevant_data(query_request.query)
    
    # Generate response using history
    response = generate_response(query_request.query, relevant_data, history)
    
    # Update history
    history.append((query_request.query, response))
    conversation_histories[session_id] = history
    
    # Handle recipient
    recipient = query_request.recipient
    
    # If no recipient provided but channel requires one, use default from config
    if not recipient and query_request.channel == "whatsapp":
        recipient = config["integrations"]["whatsapp"].get("recipient_number")
        
    # Send response to appropriate channel
    send_response_to_channel(query_request.channel, response, recipient)
    
    return {"response": response, "session_id": session_id}

@app.get("/")
def root():
    return {"message": "Financial AI Agent API. Use /ask endpoint to ask questions."}
