# Improved Fin AI Engine with fallback information
import yaml
import re

def validate_response(response):
    # Simple validation function
    if not response:
        return "I don't have enough information to answer that question."
    return response

class FinancialAI:
    def __init__(self):
        # Load config
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        
        print("Using improved Financial Q&A engine with fallbacks...")
        
        # Initialize fallback information for common financial topics
        self.fallback_info = {
            'roth ira': """
A Roth IRA is a retirement account with tax advantages:
1. Contributions are made with after-tax dollars
2. Qualified withdrawals in retirement are tax-free
3. No required minimum distributions (RMDs) during your lifetime
4. Flexibility to withdraw contributions (not earnings) without penalties
5. Good for those who expect to be in a higher tax bracket in retirement

Note: This is general information. Please consult with our financial advisors for personalized advice.
""",
            'ira': """
Individual Retirement Accounts (IRAs) are tax-advantaged accounts designed to help you save for retirement:
1. Traditional IRAs may offer tax-deductible contributions
2. Roth IRAs offer tax-free withdrawals in retirement
3. Contribution limits apply ($6,500 for 2023, $7,500 if over 50)
4. Early withdrawal penalties may apply before age 59½
5. Various investment options available within the account

Note: This is general information. Please consult with our financial advisors for personalized advice.
""",
            '401k': """
A 401(k) is an employer-sponsored retirement plan with these features:
1. Tax-deferred contributions that reduce your taxable income
2. Employer matching contributions may be available
3. Higher contribution limits than IRAs
4. Limited investment options selected by your employer
5. Loans may be available from your account

Note: This is general information. Please consult with our financial advisors for personalized advice.
"""
        }

    def generate_response(self, query: str, context) -> str:
        try:
            # If we have context items
            if isinstance(context, list) and context:
                # Extract relevant information from context
                if len(context) == 1:
                    # If only one item, use it directly
                    answer = self._format_single_response(query, context[0])
                else:
                    # If multiple items, combine them
                    answer = self._format_combined_response(query, context)
            else:
                # No relevant information found, try fallback information
                answer = self._get_fallback_response(query)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            answer = f"Error generating response: {str(e)}"
        
        return validate_response(answer)
    
    def _format_single_response(self, query, item):
        """Format a response from a single knowledge base item"""
        text = item['text']
        
        # If it's a FAQ (Q&A format)
        if text.startswith("Q:"):
            parts = text.split("\nA:")
            if len(parts) > 1:
                question = parts[0].replace("Q:", "").strip()
                answer = parts[1].strip()
                
                # Check if this is actually relevant to the query
                if self._is_relevant_to_query(query, question, answer):
                    return f"{answer}\n\nThis information is from our FAQ on: {question}"
                else:
                    # If not relevant, try fallback
                    return self._get_fallback_response(query)
        
        # For other types of content, check relevance
        if self._is_relevant_to_query(query, "", text):
            return f"{text}\n\nSource: {item.get('source', 'Knowledge Base')}"
        else:
            return self._get_fallback_response(query)
    
    def _format_combined_response(self, query, items):
        """Format a response from multiple knowledge base items"""
        response_parts = []
        
        for item in items:
            text = item['text']
            
            # If it's a FAQ (Q&A format)
            if text.startswith("Q:"):
                parts = text.split("\nA:")
                if len(parts) > 1:
                    question = parts[0].replace("Q:", "").strip()
                    answer = parts[1].strip()
                    
                    # Only include if relevant
                    if self._is_relevant_to_query(query, question, answer):
                        response_parts.append(answer)
            else:
                # Only include if relevant
                if self._is_relevant_to_query(query, "", text):
                    response_parts.append(text)
        
        # If we have relevant parts, use them
        if response_parts:
            combined = "\n\n".join(response_parts)
            return f"Here's what I found about '{query}':\n\n{combined}\n\nSource: Financial Knowledge Base"
        else:
            # If no relevant parts, use fallback
            return self._get_fallback_response(query)
    
    def _is_relevant_to_query(self, query, question, answer):
        """Determine if a response is actually relevant to the query"""
        query_lower = query.lower()
        combined_text = (question + " " + answer).lower()
        
        # Extract key terms from query
        query_terms = set(re.findall(r'\b\w+\b', query_lower))
        
        # Check for key financial terms in both query and response
        financial_terms = ['ira', 'roth', '401k', 'retirement', 'investment', 'fund', 'stock', 'bond']
        query_fin_terms = [term for term in financial_terms if term in query_lower]
        
        # If query has financial terms, make sure at least one is in the response
        if query_fin_terms:
            return any(term in combined_text for term in query_fin_terms)
        
        # Otherwise, check if at least half of query terms are in the response
        matching_terms = sum(1 for term in query_terms if term in combined_text and len(term) > 3)
        return matching_terms >= len(query_terms) / 3  # At least 1/3 of terms match
    
    def _get_fallback_response(self, query):
        """Provide fallback information when knowledge base doesn't have relevant info"""
        query_lower = query.lower()
        
        # Check for specific financial topics
        for topic, info in self.fallback_info.items():
            if topic in query_lower:
                return f"{info}\n\nNote: This is general information not specific to our services. For personalized advice, please contact our financial advisors."
        
        # Generic fallback
        return f"I don't have specific information about '{query}' in my knowledge base. Please try asking about our investment services, fees, account setup, or contact information. For personalized financial advice, please contact our advisors."

# Initialize the AI engine
fin_ai = FinancialAI()
generate_response = fin_ai.generate_response