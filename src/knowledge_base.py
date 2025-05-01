# Simplified knowledge base implementation
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

knowledge_base_path = "data/knowledge_base.json"
index_path = "data/faiss_index"
knowledge_data = []
# Initialize the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

if os.path.exists(knowledge_base_path):
    with open(knowledge_base_path, "r") as f:
        knowledge_data = json.load(f)

def embed_text(text: str):
    # Use the all-MiniLM-L6-v2 model to create embeddings
    return embedding_model.encode(text).tolist()

def load_knowledge_base():
    return knowledge_data

def create_index(force=False):
    """Create a FAISS index from the knowledge base data"""
    if not knowledge_data:
        print("No knowledge data available to index")
        return None
    
    # Delete existing index if force is True
    if force and os.path.exists(index_path):
        os.remove(index_path)
        print("Removed existing index to create a new one")
    
    # Get embedding dimension from the model
    dimension = len(embed_text("sample text"))
    
    # Create a FAISS index
    index = faiss.IndexFlatL2(dimension)
    
    # Create embeddings for all items in the knowledge base
    embeddings = []
    for i, item in enumerate(knowledge_data):
        # Process the text based on its format
        if 'text' in item:
            text = item['text']
            # For FAQ format, use both question and answer for better matching
            if text.startswith("Q:") and "\nA:" in text:
                parts = text.split("\nA:")
                question = parts[0].replace("Q:", "").strip()
                answer = parts[1].strip()
                # Create embedding for the combined text to capture both question and answer semantics
                embedding = embed_text(f"{question} {answer}")
                print(f"Indexed FAQ item {i}: {question[:30]}...")
            else:
                embedding = embed_text(text)
                print(f"Indexed text item {i}: {text[:30]}...")
            embeddings.append(embedding)
    
    if not embeddings:
        print("No content to index")
        return None
    
    # Convert to numpy array and add to index
    embeddings_np = np.array(embeddings).astype('float32')
    index.add(embeddings_np)
    
    # Save the index
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)
    
    print(f"Created index with {len(embeddings)} items")
    return index

def load_index():
    """Load the FAISS index if it exists, otherwise create it"""
    if os.path.exists(index_path):
        print("Loading existing index")
        try:
            return faiss.read_index(index_path)
        except Exception as e:
            print(f"Error loading index: {e}")
            print("Creating new index instead")
            return create_index(force=True)
    else:
        print("Creating new index")
        return create_index()

def search(query, k=5):
    """Search the knowledge base for items similar to the query"""
    # Load or create the index
    index = load_index()
    if index is None:
        print("No index available, falling back to keyword search")
        return []
    
    # Embed the query
    query_embedding = np.array([embed_text(query)]).astype('float32')
    
    # Search the index
    distances, indices = index.search(query_embedding, k)
    
    # Print debug info
    print(f"Query: '{query}'")
    print(f"Search results: {len(indices[0])} items")
    
    # Return the results
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(knowledge_data) and idx >= 0:
            result = knowledge_data[idx].copy()
            result['score'] = float(distances[0][i])
            # Print debug info for each result
            if 'text' in result:
                text_preview = result['text'][:50].replace('\n', ' ')
                print(f"Result {i}: score={result['score']:.4f}, text='{text_preview}...'")
            results.append(result)
    
    return results

def add_to_knowledge_base(item):
    """Add a new item to the knowledge base and update the index"""
    knowledge_data.append(item)
    
    # Save the updated knowledge base
    os.makedirs(os.path.dirname(knowledge_base_path), exist_ok=True)
    with open(knowledge_base_path, "w") as f:
        json.dump(knowledge_data, f, indent=2)
    
    # Update the index
    create_index(force=True)
    
    return len(knowledge_data) - 1  # Return the index of the added item

# Initialize the index when the module is loaded - force recreation
print("Initializing knowledge base index...")
index = create_index(force=True)