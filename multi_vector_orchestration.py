"""
Multi-Vector Orchestration Engine (MVOE)
Advanced 2026 Adversary Tactical Framework

Coordinates simultaneous and sequential attacks across:
- Voice (Twilio)
- SMS (Twilio)
- Email (SMTP)
- Social Media (future)

Enables sophisticated scenarios like:
- CEO Fraud / Business Email Compromise (BEC)
- IT Helpdesk Ransomware Pretext
- Supply Chain Social Engineering
- Credential Harvesting Campaigns
- Multi-Stage Exploitation Sequences
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# ============================================================================
# CHANNEL DEFINITIONS
# ============================================================================

class CommunicationChannel(Enum):
    """Supported communication channels"""
    VOICE = "voice"           # Phone calls (Twilio)
    SMS = "sms"               # Text messages (Twilio)
    EMAIL = "email"           # Email (SMTP)
    WHATSAPP = "whatsapp"     # WhatsApp (Twilio)
    SOCIAL_MEDIA = "social"   # Social engineering (future)


class MessageType(Enum):
    """Types of messages for each channel"""
    
    # Voice
    VOICE_CALL = "voice_call"
    VOICE_VOICEMAIL = "voice_voicemail"
    
    # SMS
    SMS_TEXT = "sms_text"
    SMS_LINK = "sms_link"
    SMS_VERIFICATION = "sms_verification"
    
    # Email
    EMAIL_STANDARD = "email_standard"
    EMAIL_URGENT = "email_urgent"
    EMAIL_PHISHING = "email_phishing"
    EMAIL_SPOOF = "email_spoof"
    
    # WhatsApp
    WHATSAPP_TEXT = "whatsapp_text"
    WHATSAPP_MEDIA = "whatsapp_media"


# ============================================================================
# SOCIAL ENGINEERING SPECIALIST AGENT
# ============================================================================

class SocialEngineeringSpecialist:
    """
    Advanced Social Engineering Specialist Agent
    Focuses on psychological manipulation and pretexting
    
    Specializations:
    - Pretexting (creating false scenarios)
    - Baiting (offering something enticing)
    - Quid Pro Quo (trading favors)
    - Tailgating (physical/logical access)
    - Phishing (credential harvesting)
    - Impersonation (authority/trusted figures)
    """
    
    def __init__(self, specialization: str = "pretexting"):
        self.specialization = specialization
        self.psychological_profile = self._build_profile()
        self.credibility_score = 0.0
        self.victim_profile = {}
        self.exploitation_stage = 0
    
    def _build_profile(self) -> Dict:
        """Build psychological manipulation profile"""
        
        profiles = {
            "pretexting": {
                "name": "Pretext Specialist",
                "tactics": [
                    "Create elaborate false scenarios",
                    "Establish false authority",
                    "Build detailed backstories",
                    "Use social proof extensively",
                    "Create urgency through false deadlines",
                ],
                "opening_credibility": 0.7,
                "escalation_speed": "medium",
                "primary_vectors": [
                    "authority_exploitation",
                    "social_proof",
                    "urgency_creation",
                    "liking",
                ],
            },
            "baiting": {
                "name": "Baiting Specialist",
                "tactics": [
                    "Offer valuable information or access",
                    "Promise financial gain",
                    "Provide free tools or software",
                    "Create curiosity about leaked data",
                    "Exploit FOMO (fear of missing out)",
                ],
                "opening_credibility": 0.5,
                "escalation_speed": "slow",
                "primary_vectors": [
                    "scarcity_exploitation",
                    "reciprocity",
                    "liking",
                    "commitment",
                ],
            },
            "quid_pro_quo": {
                "name": "Quid Pro Quo Specialist",
                "tactics": [
                    "Offer services or assistance",
                    "Promise problem resolution",
                    "Suggest mutual benefit",
                    "Create sense of obligation",
                    "Extract favors in return",
                ],
                "opening_credibility": 0.6,
                "escalation_speed": "medium",
                "primary_vectors": [
                    "reciprocity",
                    "liking",
                    "commitment",
                    "authority_exploitation",
                ],
            },
            "phishing": {
                "name": "Phishing Specialist",
                "tactics": [
                    "Create urgent security alerts",
                    "Mimic legitimate organizations",
                    "Design convincing fake forms",
                    "Use brand spoofing",
                    "Create credential harvesting pages",
                ],
                "opening_credibility": 0.4,
                "escalation_speed": "very_fast",
                "primary_vectors": [
                    "authority_exploitation",
                    "urgency_creation",
                    "fear_exploitation",
                    "cognitive_overload",
                ],
            },
            "impersonation": {
                "name": "Impersonation Specialist",
                "tactics": [
                    "Assume authority figures' identities",
                    "Mimic trusted partners",
                    "Spoof email addresses",
                    "Fake caller ID",
                    "Create convincing documentation",
                ],
                "opening_credibility": 0.8,
                "escalation_speed": "fast",
                "primary_vectors": [
                    "authority_exploitation",
                    "trust_exploitation",
                    "social_proof",
                    "urgency_creation",
                ],
            },
        }
        
        return profiles.get(self.specialization, profiles["pretexting"])
    
    def generate_pretext_scenario(self) -> Dict:
        """Generate detailed pretext scenario"""
        
        scenarios = {
            "IT_SECURITY_AUDIT": {
                "title": "IT Security Audit",
                "description": "Pretend to be conducting routine security audit",
                "authority_figure": "IT Security Manager",
                "urgency_level": "medium",
                "information_targets": ["passwords", "access_credentials", "system_details"],
                "opening": "Hi, this is {name} from IT Security. We're conducting a routine security audit of all systems. I need to verify your credentials to ensure compliance.",
            },
            "VENDOR_VERIFICATION": {
                "title": "Vendor Verification",
                "description": "Pretend to be vendor verifying account information",
                "authority_figure": "Vendor Account Manager",
                "urgency_level": "low",
                "information_targets": ["account_details", "payment_info", "contact_info"],
                "opening": "Hello, this is {name} from {vendor}. We're updating our records and need to verify some information on your account.",
            },
            "COMPLIANCE_CHECK": {
                "title": "Compliance Check",
                "description": "Pretend to be conducting compliance verification",
                "authority_figure": "Compliance Officer",
                "urgency_level": "high",
                "information_targets": ["employee_data", "financial_records", "access_logs"],
                "opening": "This is {name}, Compliance Division. We're conducting a mandatory compliance check. Your cooperation is required by law.",
            },
            "EMERGENCY_RESPONSE": {
                "title": "Emergency Response",
                "description": "Pretend there's an emergency requiring immediate action",
                "authority_figure": "Emergency Manager",
                "urgency_level": "critical",
                "information_targets": ["system_access", "credentials", "emergency_contacts"],
                "opening": "This is {name}, Emergency Response Team. We have a critical situation that requires immediate attention.",
            },
        }
        
        return random.choice(list(scenarios.values()))
    
    def generate_baiting_offer(self) -> Dict:
        """Generate enticing baiting offer"""
        
        offers = {
            "FREE_TOOL": {
                "title": "Free Security Tool",
                "description": "Offer free security scanning or optimization tool",
                "offer": "Download our free PPP Compliance Scanner tool",
                "hook": "Identify compliance gaps in your PPP documentation",
                "payload": "Malware/credential harvester disguised as tool",
            },
            "LEAKED_DATA": {
                "title": "Leaked Data Access",
                "description": "Offer access to leaked competitor data",
                "offer": "Access leaked industry data for competitive advantage",
                "hook": "See what your competitors are doing",
                "payload": "Credential harvesting form disguised as data portal",
            },
            "FINANCIAL_OPPORTUNITY": {
                "title": "Financial Opportunity",
                "description": "Offer financial opportunity or investment",
                "offer": "Exclusive investment opportunity for high-net-worth individuals",
                "hook": "Guaranteed 40% annual returns",
                "payload": "Credential harvesting for bank account access",
            },
            "PRIZE_REWARD": {
                "title": "Prize or Reward",
                "description": "Offer prize or reward",
                "offer": "You've been selected to claim a prize",
                "hook": "Click here to claim your $5,000 gift card",
                "payload": "Phishing link to credential harvesting page",
            },
        }
        
        return random.choice(list(offers.values()))
    
    def generate_quid_pro_quo_offer(self) -> Dict:
        """Generate quid pro quo offer"""
        
        offers = {
            "TECHNICAL_SUPPORT": {
                "title": "Technical Support",
                "description": "Offer technical support in exchange for access",
                "offer": "I can help fix your system issues",
                "request": "I'll need remote access to your computer",
                "benefit": "Your system will run faster and more securely",
            },
            "ACCOUNT_RECOVERY": {
                "title": "Account Recovery",
                "description": "Offer to help recover account access",
                "offer": "I can help you regain access to your account",
                "request": "I'll need your account credentials to verify ownership",
                "benefit": "Quick account recovery without waiting for support",
            },
            "PRIORITY_SERVICE": {
                "title": "Priority Service",
                "description": "Offer priority service in exchange for information",
                "offer": "I can expedite your PPP forgiveness application",
                "request": "I'll need your complete business and financial records",
                "benefit": "Get approved 10x faster than normal process",
            },
            "INSIDER_INFORMATION": {
                "title": "Insider Information",
                "description": "Offer insider information in exchange for access",
                "offer": "I have insider information about upcoming SBA changes",
                "request": "I'll need to verify your credentials first",
                "benefit": "Get ahead of regulatory changes before they're announced",
            },
        }
        
        return random.choice(list(offers.values()))
    
    def analyze_victim(self, victim_data: Dict) -> Dict:
        """Analyze victim for optimal exploitation"""
        
        analysis = {
            "vulnerability_score": 0.0,
            "primary_vector": "",
            "recommended_channel": CommunicationChannel.EMAIL.value,
            "optimal_timing": "",
            "psychological_triggers": [],
            "resistance_factors": [],
        }
        
        # Analyze job title for authority exploitation
        job_title = victim_data.get("job_title", "").lower()
        if any(word in job_title for word in ["manager", "director", "executive", "cfo", "cto"]):
            analysis["vulnerability_score"] += 0.3
            analysis["psychological_triggers"].append("authority_respect")
        
        # Analyze industry for targeted vectors
        industry = victim_data.get("industry", "").lower()
        if "finance" in industry or "banking" in industry:
            analysis["vulnerability_score"] += 0.2
            analysis["psychological_triggers"].append("financial_concern")
            analysis["recommended_channel"] = CommunicationChannel.EMAIL.value
        elif "technology" in industry:
            analysis["vulnerability_score"] += 0.15
            analysis["psychological_triggers"].append("technical_concern")
        
        # Analyze education level
        education = victim_data.get("education", "").lower()
        if "high school" in education:
            analysis["vulnerability_score"] += 0.2
            analysis["psychological_triggers"].append("authority_compliance")
        
        # Analyze risk tolerance
        if victim_data.get("risk_tolerance") == "low":
            analysis["vulnerability_score"] += 0.15
            analysis["psychological_triggers"].append("fear_exploitation")
        
        # Determine optimal timing
        hour = datetime.now().hour
        if 8 <= hour <= 10:
            analysis["optimal_timing"] = "morning_rush"
        elif 12 <= hour <= 13:
            analysis["optimal_timing"] = "lunch_distraction"
        elif 16 <= hour <= 18:
            analysis["optimal_timing"] = "end_of_day_fatigue"
        else:
            analysis["optimal_timing"] = "off_hours"
        
        return analysis


# ============================================================================
# MULTI-CHANNEL MESSAGE TEMPLATES
# ============================================================================

class MessageTemplateKit:
    """Pre-built message templates for coordinated attacks"""
    
    SMS_TEMPLATES = {
        "URGENT_VERIFICATION": "⚠️ URGENT: Your {service} account requires immediate verification. Click: {link} - Do NOT share this link",
        "CLICK_CONFIRM": "Hi {name}, please confirm your identity by clicking: {link} (expires in 30 min)",
        "PACKAGE_DELIVERY": "Your package couldn't be delivered. Reschedule: {link}",
        "SECURITY_ALERT": "🔒 Security Alert: Unusual activity on your {service} account. Verify now: {link}",
        "PAYMENT_FAILED": "Payment failed on your {service} account. Update payment: {link}",
        "ACCOUNT_SUSPENDED": "⚠️ Your {service} account has been suspended. Restore access: {link}",
        "PRIZE_CLAIM": "Congratulations! You've won a prize. Claim here: {link}",
        "REFUND_AVAILABLE": "You have a pending refund of ${amount}. Claim: {link}",
    }
    
    EMAIL_TEMPLATES = {
        "URGENT_ACTION_REQUIRED": {
            "subject": "URGENT: Immediate Action Required - Account Security",
            "body": """
Dear {name},

We have detected unusual activity on your {service} account and require immediate verification.

CLICK HERE TO VERIFY: {link}

This action is required within 24 hours to prevent account suspension.

If you did not initiate this request, please contact support immediately.

Best regards,
{service} Security Team
            """,
        },
        "COMPLIANCE_VERIFICATION": {
            "subject": "Mandatory Compliance Verification - {company}",
            "body": """
Dear {name},

As part of our routine compliance procedures, we require verification of your account information.

Please complete the verification form: {link}

This is a mandatory requirement and must be completed within 48 hours.

Failure to comply may result in account suspension or legal action.

Regards,
Compliance Department
            """,
        },
        "EXECUTIVE_APPROVAL": {
            "subject": "Executive Approval Required - Urgent",
            "body": """
{name},

I need your urgent approval on the attached document. Please review and approve by EOD today.

Approval Link: {link}

This is time-sensitive. Let me know if you have any questions.

Thanks,
{executive_name}
CEO/CFO
            """,
        },
        "VENDOR_UPDATE": {
            "subject": "Vendor Account Information Update Required",
            "body": """
Dear {name},

We are updating our vendor management system and require current account information.

Please update your account details: {link}

This update is required to maintain your vendor status and continue receiving payments.

Thank you,
Accounts Payable Department
            """,
        },
        "PHISHING_FORM": {
            "subject": "Account Verification Required",
            "body": """
Dear {name},

For security purposes, we need to verify your identity. Please complete the form below:

{form_html}

Submit Form: {link}

Thank you,
{service} Security Team
            """,
        },
    }
    
    VOICE_SCRIPTS = {
        "COMPLIANCE_OFFICER": """
Hi {name}, this is {agent_name} from the {agency} Compliance Division. 
We're conducting a routine audit of your account. 
I need to verify some information to ensure compliance. 
Do you have a few minutes?
        """,
        "EXECUTIVE_ASSISTANT": """
Hi {name}, this is {agent_name}, executive assistant to {executive_name}. 
I'm calling because we need your urgent approval on an important matter. 
Can you check your email for the details? 
I'll need your approval within the next hour.
        """,
        "IT_SUPPORT": """
Hello {name}, this is {agent_name} from IT Support. 
We've detected some security concerns on your account. 
I need to verify your credentials to ensure we can protect your data. 
Can you provide your username and password for verification?
        """,
        "URGENT_MATTER": """
{name}, this is {agent_name} calling about an urgent matter regarding your account. 
We've identified a critical issue that needs immediate attention. 
I'm going to send you an email with details. 
Please check your email and click the link immediately.
        """,
    }


# ============================================================================
# ORCHESTRATED SCENARIO KITS
# ============================================================================

class ScenarioKit:
    """Pre-built multi-channel exploitation scenarios"""
    
    def __init__(self, scenario_type: str):
        self.scenario_type = scenario_type
        self.channels = []
        self.timeline = []
        self.messages = {}
        self.setup_scenario()
    
    def setup_scenario(self):
        """Setup scenario based on type"""
        
        if self.scenario_type == "BEC_CEO_FRAUD":
            self.setup_bec_scenario()
        elif self.scenario_type == "IT_RANSOMWARE_PRETEXT":
            self.setup_it_ransomware_scenario()
        elif self.scenario_type == "SUPPLY_CHAIN":
            self.setup_supply_chain_scenario()
        elif self.scenario_type == "CREDENTIAL_HARVEST":
            self.setup_credential_harvest_scenario()
    
    def setup_bec_scenario(self):
        """Business Email Compromise / CEO Fraud scenario"""
        
        self.channels = [
            CommunicationChannel.EMAIL,
            CommunicationChannel.VOICE,
            CommunicationChannel.SMS,
        ]
        
        self.timeline = [
            {"time": 0, "channel": "email", "action": "Send spoofed CEO email requesting urgent wire transfer"},
            {"time": 300, "channel": "voice", "action": "Call CFO pretending to be CEO's assistant"},
            {"time": 600, "channel": "sms", "action": "Send SMS confirming urgency"},
            {"time": 900, "channel": "email", "action": "Send follow-up email with fake approval documentation"},
        ]
        
        self.messages = {
            "email_1": {
                "subject": "URGENT: Wire Transfer Authorization Required",
                "body": "Need you to wire $250K to vendor account ASAP. CEO approved. Details in attachment.",
                "from": "ceo@company.com",
                "spoofed": True,
            },
            "voice_1": {
                "script": "Hi, this is {ceo_assistant}. The CEO needs that wire transfer processed immediately. He's in a meeting but authorized me to follow up.",
                "urgency": "critical",
            },
            "sms_1": {
                "text": "CFO - CEO needs that wire ASAP. Vendor payment urgent. Check email for details.",
                "from": "CEO",
            },
        }
    
    def setup_it_ransomware_scenario(self):
        """IT Helpdesk Ransomware Pretext scenario"""
        
        self.channels = [
            CommunicationChannel.VOICE,
            CommunicationChannel.EMAIL,
            CommunicationChannel.SMS,
        ]
        
        self.timeline = [
            {"time": 0, "channel": "voice", "action": "Call IT staff claiming ransomware detected"},
            {"time": 180, "channel": "email", "action": "Send urgent security alert"},
            {"time": 360, "channel": "sms", "action": "Send verification code request"},
            {"time": 540, "channel": "voice", "action": "Follow-up call requesting admin credentials"},
        ]
        
        self.messages = {
            "voice_1": {
                "script": "This is IT Security. We've detected ransomware on your system. We need to isolate your account immediately. Please provide your admin credentials.",
                "urgency": "critical",
            },
            "email_1": {
                "subject": "CRITICAL: Ransomware Detected - Immediate Action Required",
                "body": "Ransomware detected. Click link to isolate your system: {link}",
                "from": "itsecurity@company.com",
            },
            "sms_1": {
                "text": "IT Security: Ransomware alert on your device. Verify identity: {link}",
                "from": "IT Security",
            },
        }
    
    def setup_supply_chain_scenario(self):
        """Supply Chain Social Engineering scenario"""
        
        self.channels = [
            CommunicationChannel.EMAIL,
            CommunicationChannel.SMS,
            CommunicationChannel.VOICE,
        ]
        
        self.timeline = [
            {"time": 0, "channel": "email", "action": "Send vendor invoice with malicious attachment"},
            {"time": 600, "channel": "sms", "action": "Send SMS reminder about invoice"},
            {"time": 1200, "channel": "voice", "action": "Call about urgent payment"},
        ]
    
    def setup_credential_harvest_scenario(self):
        """Credential Harvesting Campaign scenario"""
        
        self.channels = [
            CommunicationChannel.EMAIL,
            CommunicationChannel.SMS,
        ]
        
        self.timeline = [
            {"time": 0, "channel": "email", "action": "Send phishing email with credential form"},
            {"time": 300, "channel": "sms", "action": "Send SMS with verification link"},
            {"time": 600, "channel": "email", "action": "Send follow-up email"},
        ]


# ============================================================================
# ORCHESTRATION ENGINE
# ============================================================================

class MultiVectorOrchestrationEngine:
    """
    Coordinates multi-channel attacks across Voice, SMS, Email
    Manages timing, sequencing, and real-time adaptation
    """
    
    def __init__(self):
        self.active_campaigns = {}
        self.message_queue = []
        self.delivery_log = []
        self.social_engineer = SocialEngineeringSpecialist()
    
    def create_campaign(self, campaign_id: str, scenario_type: str, 
                       target: Dict) -> Dict:
        """Create new multi-channel campaign"""
        
        campaign = {
            "id": campaign_id,
            "scenario": ScenarioKit(scenario_type),
            "target": target,
            "status": "initialized",
            "start_time": datetime.now(),
            "messages_sent": [],
            "responses": [],
            "success_indicators": [],
        }
        
        self.active_campaigns[campaign_id] = campaign
        return campaign
    
    def schedule_message(self, campaign_id: str, channel: CommunicationChannel,
                        message: Dict, delay_seconds: int = 0) -> Dict:
        """Schedule message for delivery"""
        
        scheduled_message = {
            "campaign_id": campaign_id,
            "channel": channel.value,
            "message": message,
            "scheduled_time": datetime.now() + timedelta(seconds=delay_seconds),
            "status": "scheduled",
            "delivery_time": None,
            "response": None,
        }
        
        self.message_queue.append(scheduled_message)
        return scheduled_message
    
    def execute_campaign(self, campaign_id: str) -> Dict:
        """Execute multi-channel campaign"""
        
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return {"error": "Campaign not found"}
        
        campaign["status"] = "executing"
        results = {
            "campaign_id": campaign_id,
            "messages_sent": [],
            "delivery_status": [],
        }
        
        # Execute messages according to timeline
        for timeline_item in campaign["scenario"].timeline:
            channel = CommunicationChannel[timeline_item["channel"].upper()]
            
            result = self.deliver_message(
                campaign_id,
                channel,
                timeline_item["action"]
            )
            
            results["messages_sent"].append(result)
            campaign["messages_sent"].append(result)
        
        campaign["status"] = "completed"
        return results
    
    def deliver_message(self, campaign_id: str, channel: CommunicationChannel,
                       action: str) -> Dict:
        """Deliver message on specific channel"""
        
        delivery_result = {
            "campaign_id": campaign_id,
            "channel": channel.value,
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "status": "delivered",
            "delivery_method": self._get_delivery_method(channel),
        }
        
        self.delivery_log.append(delivery_result)
        return delivery_result
    
    def _get_delivery_method(self, channel: CommunicationChannel) -> str:
        """Get delivery method for channel"""
        
        methods = {
            CommunicationChannel.VOICE: "Twilio Voice API",
            CommunicationChannel.SMS: "Twilio SMS API",
            CommunicationChannel.EMAIL: "SMTP Server",
            CommunicationChannel.WHATSAPP: "Twilio WhatsApp API",
        }
        
        return methods.get(channel, "Unknown")
    
    def analyze_response(self, campaign_id: str, response: str) -> Dict:
        """Analyze victim response and recommend next action"""
        
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return {"error": "Campaign not found"}
        
        analysis = {
            "response": response,
            "compliance_score": self._calculate_compliance(response),
            "recommended_next_action": "",
            "suggested_channel": "",
            "escalation_level": 0,
        }
        
        # Analyze response for compliance indicators
        if any(word in response.lower() for word in ["yes", "okay", "sure", "will do"]):
            analysis["compliance_score"] = 0.8
            analysis["recommended_next_action"] = "Send credential request"
            analysis["suggested_channel"] = CommunicationChannel.EMAIL.value
        elif any(word in response.lower() for word in ["no", "suspicious", "verify"]):
            analysis["compliance_score"] = 0.2
            analysis["recommended_next_action"] = "Switch to different vector"
            analysis["escalation_level"] = -1
        else:
            analysis["compliance_score"] = 0.5
            analysis["recommended_next_action"] = "Continue engagement"
        
        campaign["responses"].append(analysis)
        return analysis
    
    def _calculate_compliance(self, response: str) -> float:
        """Calculate victim compliance score (0.0-1.0)"""
        
        compliance_keywords = {
            "yes": 0.9, "okay": 0.8, "sure": 0.8, "will do": 0.85,
            "understood": 0.7, "got it": 0.7, "thanks": 0.6,
        }
        
        resistance_keywords = {
            "no": -0.9, "suspicious": -0.9, "verify": -0.3,
            "check": -0.3, "prove": -0.3, "scam": -1.0,
        }
        
        response_lower = response.lower()
        score = 0.5
        
        for keyword, value in compliance_keywords.items():
            if keyword in response_lower:
                score = max(score, value)
        
        for keyword, value in resistance_keywords.items():
            if keyword in response_lower:
                score = min(score, value)
        
        return max(0.0, min(1.0, score))
    
    def get_campaign_status(self, campaign_id: str) -> Dict:
        """Get detailed campaign status"""
        
        campaign = self.active_campaigns.get(campaign_id)
        if not campaign:
            return {"error": "Campaign not found"}
        
        return {
            "campaign_id": campaign_id,
            "status": campaign["status"],
            "scenario_type": campaign["scenario"].scenario_type,
            "target": campaign["target"],
            "start_time": campaign["start_time"].isoformat(),
            "messages_sent": len(campaign["messages_sent"]),
            "responses_received": len(campaign["responses"]),
            "success_indicators": campaign["success_indicators"],
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Create orchestration engine
    engine = MultiVectorOrchestrationEngine()
    
    # Define target
    target = {
        "name": "John Smith",
        "email": "john@company.com",
        "phone": "+1234567890",
        "job_title": "CFO",
        "company": "TechCorp Inc",
    }
    
    # Create BEC campaign
    campaign = engine.create_campaign(
        "bec_001",
        "BEC_CEO_FRAUD",
        target
    )
    
    print("=== MULTI-VECTOR ORCHESTRATION ENGINE ===\n")
    print(f"Campaign Created: {campaign['id']}")
    print(f"Scenario: {campaign['scenario'].scenario_type}")
    print(f"Target: {target['name']} ({target['job_title']})\n")
    
    # Execute campaign
    results = engine.execute_campaign("bec_001")
    print(f"Messages Sent: {len(results['messages_sent'])}\n")
    
    # Analyze response
    victim_response = "I'll process that wire transfer right away"
    analysis = engine.analyze_response("bec_001", victim_response)
    print(f"Victim Response: '{victim_response}'")
    print(f"Compliance Score: {analysis['compliance_score']:.2f}")
    print(f"Recommended Action: {analysis['recommended_next_action']}\n")
    
    # Get campaign status
    status = engine.get_campaign_status("bec_001")
    print(f"Campaign Status: {json.dumps(status, indent=2)}")
