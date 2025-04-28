# Financial AI Agent

A powerful AI-powered assistant for financial services that uses Retrieval Augmented Generation (RAG) to provide accurate financial information and advice through multiple communication channels.

## Project Objective

The Financial AI Agent aims to provide instant, accurate responses to customer inquiries about financial products, services, and general financial knowledge. By leveraging modern AI technologies and a knowledge base of financial information, this agent helps financial institutions:

- Reduce customer support workload
- Provide 24/7 automated assistance
- Deliver consistent and accurate financial information
- Reach customers through their preferred communication channels (WhatsApp, Email, Live Chat)

## How This Project Helps

### For Financial Institutions
- **Cost Reduction**: Automates routine customer inquiries, reducing support staff requirements
- **Improved Customer Experience**: Provides instant responses at any time of day
- **Scalability**: Handles multiple customer inquiries simultaneously
- **Consistency**: Ensures all customers receive the same accurate information
- **Multi-channel Support**: Reaches customers through WhatsApp, Email, and Live Chat

### For Customers
- **Instant Answers**: Get immediate responses to financial questions
- **Convenience**: Access information through preferred communication channels
- **24/7 Availability**: Get assistance outside of business hours
- **Personalized Information**: Receive relevant information based on specific queries

## System Architecture & Workflow

The Financial AI Agent follows this workflow:

1. **Knowledge Base Creation** (`knowledge_base.py`):
   - Financial information is stored in structured format
   - Documents are embedded using sentence transformers
   - Vector database is created for semantic search

2. **Query Processing & Retrieval** (`retrieval.py`):
   - User query is received through API
   - Query is embedded and semantically searched against knowledge base
   - Most relevant information is retrieved

3. **Response Generation** (`fin_engine.py`):
   - Retrieved context is combined with user query
   - AI model generates natural language response
   - Response is validated for accuracy and compliance

4. **API & Integration** (`main.py`, `integrations.py`):
   - FastAPI server handles incoming requests
   - Response is delivered through appropriate channel (WhatsApp, Email, Chat)
   - Conversation history can be maintained for context

## Project Structure

```
fin_ai_agent/
│── models/                  # Stores the AI model (if using local LLM)
│── data/                    # Stores FAQs, PDFs, Help Articles
│── embeddings/              # Vectorized knowledge base
│── src/
│   ├── main.py              # (4) API Server with FastAPI
│   ├── retrieval.py         # (2) Retrieve Relevant Data (RAG)
│   ├── knowledge_base.py    # (1) Load and Embed Knowledge Base
│   ├── fin_engine.py        # (3) Generate AI Response using RAG + LLM
│   ├── integrations.py      # (5) WhatsApp, Email, Live Chat Integration
│   ├── security.py          # AI safety and compliance checks
│── requirements.txt         # Python dependencies
│── config.yaml              # Configuration file
│── README.md                # Documentation
│── Dockerfile               # Docker configuration
│── docker-compose.yml       # Docker Compose configuration
```

## Setup and Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Docker (for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fin_ai_agent.git
   cd fin_ai_agent
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**
   - Edit `config.yaml` to set up your:
     - API keys
     - Twilio credentials for WhatsApp
     - Email settings
     - Model preferences

5. **Prepare knowledge base**
   - Add your financial FAQs, documents, and help articles to the `data/` directory
   - Format should follow the existing JSON structure in `data/knowledge_base.json`

6. **Run the application**
   ```bash
   uvicorn src.main:app --host 127.0.0.1 --port 8000
   ```

7. **Access the API**
   - API documentation: http://127.0.0.1:8000/docs
   - Test endpoint: http://127.0.0.1:8000/

## Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t fin_ai_agent .
   ```

2. **Run with Docker**
   ```bash
   docker run -d -p 8000:8000 --name fin_ai_agent fin_ai_agent
   ```

3. **Using Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Scaling with Docker Compose**
   ```bash
   docker-compose up -d --scale fin_ai_agent=3
   ```

## Cloud Deployment Options

### AWS Deployment
1. Push Docker image to Amazon ECR
2. Deploy using ECS or EKS
3. Set up API Gateway and load balancer

### Google Cloud Deployment
1. Push Docker image to Google Container Registry
2. Deploy using Google Cloud Run or GKE
3. Set up Cloud Endpoints for API management

### Azure Deployment
1. Push Docker image to Azure Container Registry
2. Deploy using Azure Container Instances or AKS
3. Set up API Management

## Using the API

### Making Requests

```bash
# Chat channel example
curl -X 'POST' \
  'http://127.0.0.1:8000/ask' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What are the benefits of a Roth IRA?",
  "channel": "chat"
}'

# WhatsApp channel example
curl -X 'POST' \
  'http://127.0.0.1:8000/ask' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "What are your investment services?",
  "channel": "whatsapp",
  "recipient": "+1234567890"
}'

# Email channel example
curl -X 'POST' \
  'http://127.0.0.1:8000/ask' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "How do I open an account?",
  "channel": "email",
  "recipient": "customer@example.com"
}'
```

## Enhancement Opportunities

### Short-term Improvements
1. **Conversation Memory**: Add session management to remember context from previous questions
2. **User Authentication**: Implement secure authentication for personalized responses
3. **Response Templates**: Create customizable templates for different types of financial queries
4. **Feedback Loop**: Add user feedback mechanism to improve responses over time
5. **Analytics Dashboard**: Track usage patterns and common questions

### Medium-term Enhancements
1. **Multi-language Support**: Add capability to handle queries in multiple languages
2. **Voice Interface**: Integrate with voice assistants or phone systems
3. **Personalization Engine**: Tailor responses based on user profile and history
4. **Advanced Security**: Implement additional security measures for handling sensitive financial data
5. **A/B Testing Framework**: Test different response formats for effectiveness

### Long-term Vision
1. **Predictive Capabilities**: Anticipate customer needs based on patterns and data
2. **Financial Planning Tools**: Integrate calculators and planning tools into responses
3. **Omnichannel Experience**: Seamless transition between channels while maintaining context
4. **Regulatory Compliance Engine**: Automated checks for financial advice compliance
5. **Integration with Core Banking Systems**: Direct access to customer account information

## Monitoring and Maintenance

### Logging
- Application logs are stored in the `logs/` directory
- Use log rotation to manage log files

### Monitoring
- Implement health checks at `/health` endpoint
- Set up alerts for error rates and response times

### Updating the Knowledge Base
1. Add new content to the data files
2. Run the embedding process to update the vector database
3. Restart the application to load the updated knowledge base

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or support, please contact [your-email@example.com](mailto:your-email@example.com).