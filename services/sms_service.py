import os
import logging
from typing import List, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class SMSService:
    """Service for sending SMS notifications using Twilio"""
    
    def __init__(self):
        self.should_use_twilio = os.getenv('SHOULD_USE_TWILIO', 'false').lower() == 'true'
        
        if not self.should_use_twilio:
            logger.info("Twilio usage disabled by configuration. Using mock SMS service.")
            self.client = None
            return
            
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            logger.warning("Twilio credentials not configured. SMS functionality will be disabled.")
            self.client = None
        else:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Twilio SMS service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                self.client = None
    
    def is_enabled(self) -> bool:
        """Check if SMS service is properly configured and enabled"""
        return self.client is not None
    
    async def send_sms(self, to_number: str, message: str) -> dict:
        """
        Send SMS to a single number
        
        Args:
            to_number: Phone number to send SMS to (with country code)
            message: Message content
            
        Returns:
            dict: Result with success status and message details
        """
        if not self.is_enabled():
            logger.warning("SMS service not enabled. Cannot send SMS.")
            # Return mock response when Twilio is disabled
            logger.info(f"Mock SMS sent to {to_number}: {message}")
            return {
                "success": True,
                "message_sid": "mock_sms_id_" + to_number,
                "to": to_number,
                "status": "mock_delivered"
            }
        
        try:
            # Ensure phone number is in correct format
            if not to_number.startswith('+'):
                to_number = f"+{to_number}"
            
            message_obj = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            
            logger.info(f"SMS sent successfully to {to_number}. SID: {message_obj.sid}")
            return {
                "success": True,
                "message_sid": message_obj.sid,
                "to": to_number,
                "status": message_obj.status
            }
            
        except TwilioException as e:
            logger.error(f"Twilio error sending SMS to {to_number}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message_sid": None
            }
        except Exception as e:
            logger.error(f"Unexpected error sending SMS to {to_number}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message_sid": None
            }
    
    async def send_bulk_sms(self, phone_numbers: List[str], message: str) -> dict:
        """
        Send SMS to multiple numbers
        
        Args:
            phone_numbers: List of phone numbers to send SMS to
            message: Message content
            
        Returns:
            dict: Summary of results including successful and failed sends
        """
        if not self.is_enabled():
            logger.warning("SMS service not enabled. Cannot send bulk SMS.")
            # Return mock response for bulk SMS when Twilio is disabled
            logger.info(f"Mock bulk SMS sent to {len(phone_numbers)} numbers")
            return {
                "success": True,
                "successful_sends": [{
                    "phone_number": num,
                    "message_sid": f"mock_bulk_{i}"
                } for i, num in enumerate(phone_numbers)],
                "failed_sends": [],
                "summary": {
                    "sent": len(phone_numbers),
                    "failed": 0
                }
            }
        
        successful_sends = []
        failed_sends = []
        
        for phone_number in phone_numbers:
            result = await self.send_sms(phone_number, message)
            
            if result["success"]:
                successful_sends.append({
                    "phone_number": phone_number,
                    "message_sid": result["message_sid"]
                })
            else:
                failed_sends.append({
                    "phone_number": phone_number,
                    "error": result["error"]
                })
        
        total_sent = len(successful_sends)
        total_failed = len(failed_sends)
        
        logger.info(f"Bulk SMS completed: {total_sent} successful, {total_failed} failed")
        
        return {
            "success": total_sent > 0,
            "total_numbers": len(phone_numbers),
            "successful_sends": successful_sends,
            "failed_sends": failed_sends,
            "summary": {
                "sent": total_sent,
                "failed": total_failed
            }
        }

# SMS Templates
class SMSTemplates:
    """Predefined SMS templates for different banking scenarios"""
    
    @staticmethod
    def complaint_confirmation(ticket_id: str, customer_name: str) -> str:
        """Template for complaint confirmation SMS"""
        return f"Dear {customer_name}, your complaint has been registered with ticket ID: {ticket_id}. We will resolve it within 7-10 business days. Thank you for banking with us."
    
    @staticmethod
    def complaint_resolution(ticket_id: str, customer_name: str) -> str:
        """Template for complaint resolution SMS"""
        return f"Dear {customer_name}, your complaint {ticket_id} has been resolved. Please check your account or contact us if you need further assistance. Thank you for your patience."
    
    @staticmethod
    def dispute_confirmation(ticket_id: str, customer_name: str, amount: float) -> str:
        """Template for dispute confirmation SMS"""
        return f"Dear {customer_name}, your dispute for ₹{amount} has been registered with ticket ID: {ticket_id}. We will investigate and respond within 15-30 business days."
    
    @staticmethod
    def dispute_resolution(ticket_id: str, customer_name: str, status: str) -> str:
        """Template for dispute resolution SMS"""
        return f"Dear {customer_name}, your dispute {ticket_id} has been {status.lower()}. Please check your account for updates or contact us for more details."
    
    @staticmethod
    def account_alert(customer_name: str, alert_type: str, details: str) -> str:
        """Template for general account alerts"""
        return f"Dear {customer_name}, {alert_type}: {details}. If this wasn't you, please contact us immediately."
    
    @staticmethod
    def transaction_alert(customer_name: str, amount: float, transaction_type: str) -> str:
        """Template for transaction alerts"""
        return f"Dear {customer_name}, your account has been {transaction_type} with ₹{amount}. If this wasn't authorized by you, please contact us immediately."

# Initialize SMS service
sms_service = SMSService()