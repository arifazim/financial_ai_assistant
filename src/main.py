# API server (FastAPI) 
##### src/main.py #####
import os
import yaml
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Prevent tokenizers warning

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.retrieval import retrieve_relevant_data
from src.fin_engine import generate_response
from src.integrations import send_response_to_channel

app = FastAPI()

# Load config for default values
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

class QueryRequest(BaseModel):
    query: str
    channel: str  # e.g., "email", "whatsapp", "chat"
    recipient: str = None  # Optional recipient (phone number or email)

@app.post("/ask")
def ask(query_request: QueryRequest):
    # Get relevant data from knowledge base
    relevant_data = retrieve_relevant_data(query_request.query)
    
    # Generate response
    response = generate_response(query_request.query, relevant_data)
    
    # Handle recipient
    recipient = query_request.recipient
    
    # If no recipient provided but channel requires one, use default from config
    if not recipient and query_request.channel == "whatsapp":
        recipient = config["integrations"]["whatsapp"].get("recipient_number")
        
    # Send response to appropriate channel
    send_response_to_channel(query_request.channel, response, recipient)
    
    return {"response": response}

@app.get("/")
def root():
    return {"message": "Financial AI Agent API. Use /ask endpoint to ask questions."}
