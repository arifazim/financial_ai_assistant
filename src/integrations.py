# Email, WhatsApp, SMS, Live Chat integration 
##### src/integrations.py #####

# Integration handlers for different channels
import yaml
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class IntegrationManager:
    def __init__(self):
        # Load config
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        
        print("Using Twilio WhatsApp integration...")
        
        # Initialize Twilio client
        if self.config["integrations"]["whatsapp"]["enabled"]:
            try:
                self.twilio_client = Client(
                    self.config["integrations"]["whatsapp"]["twilio_account_sid"],
                    self.config["integrations"]["whatsapp"]["twilio_auth_token"]
                )
                print("Twilio client initialized successfully")
            except Exception as e:
                print(f"Error initializing Twilio client: {str(e)}")
    
    def send_email(self, to_email: str, response: str):
        """Send response via email (simplified)"""
        print(f"[EMAIL] To: {to_email}")
        print(f"[EMAIL] Message: {response}")
        return True
    
    def send_whatsapp(self, to_number: str, response: str):
        """Send response via WhatsApp"""
        if not self.config["integrations"]["whatsapp"]["enabled"]:
            print("WhatsApp integration is disabled")
            return
        
        try:
            # Format the phone number correctly
            if not to_number.startswith("+"):
                to_number = "+" + to_number
            
            # Remove any spaces or dashes
            to_number = to_number.replace(" ", "").replace("-", "")
            
            print(f"Sending WhatsApp message to {to_number}")
            
            message = self.twilio_client.messages.create(
                body=response,
                from_=f"whatsapp:{self.config['integrations']['whatsapp']['from_number']}",
                to=f"whatsapp:{to_number}"
            )
            print(f"WhatsApp message sent successfully: {message.sid}")
            return True
            
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            return False

# Initialize integration manager
integration_manager = IntegrationManager()

def send_response_to_channel(channel: str, response: str, recipient: str = None):
    """Route response to appropriate channel"""
    print(f"Sending response via {channel} to {recipient}")
    
    if channel == "email" and recipient:
        integration_manager.send_email(recipient, response)
    elif channel == "whatsapp" and recipient:
        integration_manager.send_whatsapp(recipient, response)
    elif channel == "chat":
        print(f"[CHAT] Response: {response}")
    else:
        print(f"[UNKNOWN] Channel: {channel}, Response: {response}")