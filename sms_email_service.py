"""
SMS and Email Service Integration
Multi-Channel Communication for Fraud Simulation

Integrates:
- Twilio SMS API
- SMTP Email
- Email spoofing capabilities
- Real-time message tracking
- Delivery and response logging
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
from config import Config

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False


# ============================================================================
# SMS SERVICE
# ============================================================================

class SMSService:
    """Twilio SMS Integration for Multi-Channel Campaigns"""
    
    def __init__(self):
        self.client = None
        self.account_sid = Config.TWILIO_ACCOUNT_SID
        self.auth_token = Config.TWILIO_AUTH_TOKEN
        self.from_number = Config.TWILIO_PHONE_NUMBER
        self.message_log = []
        
        if TWILIO_AVAILABLE and self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.is_available = True
            except Exception as e:
                print(f"[SMS Service] Initialization error: {e}")
                self.is_available = False
        else:
            self.is_available = False
    
    def send_sms(self, to_number: str, message: str, 
                 campaign_id: str = None) -> Dict:
        """Send SMS message"""
        
        result = {
            "status": "failed",
            "message_sid": None,
            "to": to_number,
            "from": self.from_number,
            "body": message,
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_id,
        }
        
        if not self.is_available:
            result["status"] = "unavailable"
            result["error"] = "Twilio SMS service not configured"
            return result
        
        try:
            response = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            result["status"] = "sent"
            result["message_sid"] = response.sid
            self.message_log.append(result)
            
            return result
        
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            return result
    
    def send_sms_campaign(self, recipients: List[str], message: str,
                         campaign_id: str) -> List[Dict]:
        """Send SMS to multiple recipients"""
        
        results = []
        for recipient in recipients:
            result = self.send_sms(recipient, message, campaign_id)
            results.append(result)
        
        return results
    
    def send_verification_code_sms(self, to_number: str, code: str,
                                   service: str = "Your Service") -> Dict:
        """Send verification code SMS"""
        
        message = f"Your {service} verification code is: {code}. Do not share this code."
        return self.send_sms(to_number, message)
    
    def send_urgent_alert_sms(self, to_number: str, alert_type: str) -> Dict:
        """Send urgent alert SMS"""
        
        alerts = {
            "account_security": "⚠️ SECURITY ALERT: Unusual activity on your account. Click to verify: {link}",
            "payment_failed": "Payment failed on your account. Update payment method: {link}",
            "account_suspended": "Your account has been suspended. Restore access: {link}",
            "verification_needed": "Account verification needed. Verify now: {link}",
        }
        
        message = alerts.get(alert_type, "Alert: Action required on your account: {link}")
        return self.send_sms(to_number, message)
    
    def send_phishing_sms(self, to_number: str, phishing_link: str) -> Dict:
        """Send phishing SMS with malicious link"""
        
        messages = [
            f"Click to verify your account: {phishing_link}",
            f"Confirm your identity: {phishing_link}",
            f"Update your information: {phishing_link}",
            f"Verify your credentials: {phishing_link}",
        ]
        
        message = messages[0]  # Use first template
        return self.send_sms(to_number, message)
    
    def get_message_log(self, campaign_id: str = None) -> List[Dict]:
        """Get message log, optionally filtered by campaign"""
        
        if campaign_id:
            return [msg for msg in self.message_log if msg.get("campaign_id") == campaign_id]
        return self.message_log


# ============================================================================
# EMAIL SERVICE
# ============================================================================

class EmailService:
    """SMTP Email Integration with Spoofing Capabilities"""
    
    def __init__(self):
        self.smtp_server = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("MAIL_PORT", 587))
        self.sender_email = os.environ.get("MAIL_USERNAME", "")
        self.sender_password = os.environ.get("MAIL_PASSWORD", "")
        self.use_tls = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"
        self.message_log = []
        self.is_available = bool(self.sender_email and self.sender_password)
    
    def send_email(self, to_email: str, subject: str, body: str,
                   from_display: str = None, html: bool = False,
                   campaign_id: str = None, attachments: List[str] = None) -> Dict:
        """Send email"""
        
        result = {
            "status": "failed",
            "to": to_email,
            "from": from_display or self.sender_email,
            "subject": subject,
            "timestamp": datetime.now().isoformat(),
            "campaign_id": campaign_id,
        }
        
        if not self.is_available:
            result["status"] = "unavailable"
            result["error"] = "Email service not configured"
            return result
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = from_display or self.sender_email
            message["To"] = to_email
            
            # Add body
            if html:
                message.attach(MIMEText(body, "html"))
            else:
                message.attach(MIMEText(body, "plain"))
            
            # Add attachments
            if attachments:
                for attachment_path in attachments:
                    try:
                        with open(attachment_path, "rb") as attachment:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                "Content-Disposition",
                                f"attachment; filename= {os.path.basename(attachment_path)}"
                            )
                            message.attach(part)
                    except Exception as e:
                        print(f"[Email] Attachment error: {e}")
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            result["status"] = "sent"
            self.message_log.append(result)
            return result
        
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            return result
    
    def send_email_campaign(self, recipients: List[Dict], subject: str,
                           body: str, campaign_id: str) -> List[Dict]:
        """Send email to multiple recipients"""
        
        results = []
        for recipient in recipients:
            result = self.send_email(
                recipient.get("email"),
                subject,
                body,
                from_display=recipient.get("from_display"),
                campaign_id=campaign_id
            )
            results.append(result)
        
        return results
    
    def send_phishing_email(self, to_email: str, subject: str,
                           phishing_form: str, from_display: str = None,
                           campaign_id: str = None) -> Dict:
        """Send phishing email with credential harvesting form"""
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif;">
<div style="background-color: #f5f5f5; padding: 20px;">
<h2>Account Verification Required</h2>
<p>For security purposes, we need to verify your identity.</p>

{phishing_form}

<p style="color: #666; font-size: 12px;">
This is an automated message. Please do not reply to this email.
</p>
</div>
</body>
</html>
        """
        
        return self.send_email(
            to_email,
            subject,
            html_body,
            from_display=from_display,
            html=True,
            campaign_id=campaign_id
        )
    
    def send_urgent_alert_email(self, to_email: str, alert_type: str,
                               from_display: str = None) -> Dict:
        """Send urgent alert email"""
        
        alerts = {
            "account_security": {
                "subject": "URGENT: Account Security Alert",
                "body": "We detected unusual activity on your account. Please verify your identity immediately.",
            },
            "payment_failed": {
                "subject": "Payment Failed - Action Required",
                "body": "Your payment failed. Please update your payment method.",
            },
            "account_suspended": {
                "subject": "Account Suspended",
                "body": "Your account has been suspended. Click to restore access.",
            },
            "compliance_check": {
                "subject": "Mandatory Compliance Verification",
                "body": "We require verification of your account information for compliance purposes.",
            },
        }
        
        alert = alerts.get(alert_type, alerts["account_security"])
        return self.send_email(
            to_email,
            alert["subject"],
            alert["body"],
            from_display=from_display
        )
    
    def send_bec_email(self, to_email: str, ceo_name: str, amount: str,
                      vendor: str, from_display: str = None) -> Dict:
        """Send Business Email Compromise email"""
        
        subject = "URGENT: Wire Transfer Authorization - Confidential"
        body = f"""
{to_email.split('@')[0]},

I need you to process an urgent wire transfer immediately. This is confidential and time-sensitive.

WIRE DETAILS:
- Amount: ${amount}
- Recipient: {vendor}
- Reference: Acquisition

Please process this by EOD today. I'm in back-to-back meetings and won't be available to discuss.

Do NOT discuss this with anyone else in the company.

Once completed, send me confirmation.

Thanks,
{ceo_name}
CEO
        """
        
        return self.send_email(
            to_email,
            subject,
            body,
            from_display=from_display or f"{ceo_name} <ceo@company.com>"
        )
    
    def send_it_security_email(self, to_email: str, malicious_link: str) -> Dict:
        """Send IT security alert email with malicious link"""
        
        subject = "🚨 CRITICAL: Ransomware Detected - Immediate Action Required"
        body = f"""
CRITICAL SECURITY ALERT

Ransomware has been detected on your system.

IMMEDIATE ACTION REQUIRED:

1. Click here to download security isolation tool: {malicious_link}
2. Run the tool immediately
3. Do NOT use your computer until cleared by IT

If you do not take action within 30 minutes, your system will be automatically isolated.

Contact IT Security immediately if you have questions.

IT Security Team
        """
        
        return self.send_email(
            to_email,
            subject,
            body,
            from_display="IT Security <itsecurity@company.com>"
        )
    
    def get_message_log(self, campaign_id: str = None) -> List[Dict]:
        """Get message log, optionally filtered by campaign"""
        
        if campaign_id:
            return [msg for msg in self.message_log if msg.get("campaign_id") == campaign_id]
        return self.message_log


# ============================================================================
# MULTI-CHANNEL COORDINATOR
# ============================================================================

class MultiChannelCoordinator:
    """Coordinates SMS and Email for multi-channel campaigns"""
    
    def __init__(self):
        self.sms_service = SMSService()
        self.email_service = EmailService()
        self.campaign_log = {}
    
    def send_coordinated_message(self, campaign_id: str, target: Dict,
                                channels: List[str], messages: Dict) -> Dict:
        """Send coordinated message across multiple channels"""
        
        results = {
            "campaign_id": campaign_id,
            "target": target,
            "channels": channels,
            "results": {},
            "timestamp": datetime.now().isoformat(),
        }
        
        # Send via SMS
        if "sms" in channels and "sms" in messages:
            sms_result = self.sms_service.send_sms(
                target.get("phone"),
                messages["sms"],
                campaign_id
            )
            results["results"]["sms"] = sms_result
        
        # Send via Email
        if "email" in channels and "email" in messages:
            email_msg = messages["email"]
            email_result = self.email_service.send_email(
                target.get("email"),
                email_msg.get("subject"),
                email_msg.get("body"),
                from_display=email_msg.get("from_display"),
                campaign_id=campaign_id
            )
            results["results"]["email"] = email_result
        
        self.campaign_log[campaign_id] = results
        return results
    
    def send_sequential_messages(self, campaign_id: str, target: Dict,
                                message_sequence: List[Dict]) -> Dict:
        """Send messages in sequence with delays"""
        
        results = {
            "campaign_id": campaign_id,
            "target": target,
            "sequence_results": [],
            "timestamp": datetime.now().isoformat(),
        }
        
        for i, message_config in enumerate(message_sequence):
            channel = message_config.get("channel")
            message = message_config.get("message")
            delay = message_config.get("delay_seconds", 0)
            
            # In production, would implement actual delay
            # For now, just send immediately
            
            if channel == "sms":
                result = self.sms_service.send_sms(
                    target.get("phone"),
                    message,
                    campaign_id
                )
            elif channel == "email":
                result = self.email_service.send_email(
                    target.get("email"),
                    message.get("subject"),
                    message.get("body"),
                    campaign_id=campaign_id
                )
            else:
                result = {"status": "unknown_channel"}
            
            results["sequence_results"].append({
                "step": i + 1,
                "channel": channel,
                "result": result,
            })
        
        self.campaign_log[campaign_id] = results
        return results
    
    def get_campaign_status(self, campaign_id: str) -> Dict:
        """Get campaign delivery status"""
        
        return self.campaign_log.get(campaign_id, {"error": "Campaign not found"})


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== SMS AND EMAIL SERVICE INTEGRATION ===\n")
    
    # Initialize services
    sms_service = SMSService()
    email_service = EmailService()
    coordinator = MultiChannelCoordinator()
    
    print(f"SMS Service Available: {sms_service.is_available}")
    print(f"Email Service Available: {email_service.is_available}\n")
    
    # Example target
    target = {
        "name": "John Smith",
        "email": "john@company.com",
        "phone": "+1234567890",
    }
    
    # Example: Send coordinated BEC campaign
    print("Example: Coordinated BEC Campaign")
    print("-" * 50)
    
    messages = {
        "email": {
            "subject": "URGENT: Wire Transfer Authorization",
            "body": "Need you to wire $250K to vendor account ASAP. CEO approved.",
            "from_display": "CEO <ceo@company.com>",
        },
        "sms": "CEO needs that wire ASAP. Check email for details.",
    }
    
    result = coordinator.send_coordinated_message(
        "bec_001",
        target,
        ["email", "sms"],
        messages
    )
    
    print(f"Campaign ID: {result['campaign_id']}")
    print(f"Email Status: {result['results'].get('email', {}).get('status')}")
    print(f"SMS Status: {result['results'].get('sms', {}).get('status')}")
