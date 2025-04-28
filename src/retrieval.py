# Improved semantic search with better relevance scoring
##### src/retrieval.py #####
from src.knowledge_base import load_knowledge_base

def retrieve_relevant_data(query: str, top_k=3):
    knowledge_data = load_knowledge_base()
    
    # Split query into keywords for better matching
    query_keywords = set(query.lower().split())
    
    # Extract main topic from query (e.g., "Roth IRA" from "What are the benefits of a Roth IRA?")
    query_lower = query.lower()
    
    # Score each item in the knowledge base
    scored_items = []
    for item in knowledge_data:
        text = item['text'].lower()
        
        # Calculate a relevance score based on keyword matches
        score = 0
        
        # Check for exact phrase matches first (highest priority)
        if query_lower in text:
            score += 10
        
        # Check for individual keyword matches
        for keyword in query_keywords:
            if keyword in text:
                score += 1
                
                # Give extra weight to important financial terms
                if keyword in ['ira', 'roth', '401k', 'retirement', 'investment', 'fund', 'stock', 'bond']:
                    score += 2
                    
                # Give extra weight to titles/questions
                if "Q:" in item['text'] and keyword in item['text'].split("Q:")[1].split("A:")[0].lower():
                    score += 3
        
        # Only include items with a minimum relevance
        if score > 0:
            scored_items.append((score, item))
    
    # Sort by score (highest first) and take top_k
    scored_items.sort(reverse=True, key=lambda x: x[0])
    
    # Return only the items, not the scores
    results = [item for score, item in scored_items[:top_k]]
    
    # If no results found, return an empty list
    return results if results else []
