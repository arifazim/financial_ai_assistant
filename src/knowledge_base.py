##### src/knowledge_base.py #####
# Simplified knowledge base implementation
import os
import json

knowledge_base_path = "data/knowledge_base.json"
knowledge_data = []

if os.path.exists(knowledge_base_path):
    with open(knowledge_base_path, "r") as f:
        knowledge_data = json.load(f)

def embed_text(text: str):
    # Simplified embedding function that just returns the text
    return text

def load_knowledge_base():
    return knowledge_data