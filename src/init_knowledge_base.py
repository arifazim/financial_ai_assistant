import json
import os

# Load FAQ data
with open("data/faq.json", "r") as f:
    faq_data = json.load(f)

# Load help articles
with open("data/help_articles.json", "r") as f:
    help_data = json.load(f)

# Convert to knowledge base format
knowledge_base = []

# Add FAQ items
for item in faq_data:
    knowledge_base.append({
        "text": f"Q: {item['question']}\nA: {item['answer']}",
        "source": "FAQ"
    })

# Add help articles
for item in help_data:
    knowledge_base.append({
        "text": f"{item['title']}\n{item['content']}",
        "source": "Help Article"
    })

# Save combined knowledge base
with open("data/knowledge_base.json", "w") as f:
    json.dump(knowledge_base, f, indent=2)
