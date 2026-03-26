"""
Realistic 2026 Scenario Kits
Extensive Real-Time Handling and Tactical Scenarios

Includes:
- Business Email Compromise (BEC) / CEO Fraud
- IT Helpdesk Ransomware Pretext
- Supply Chain Compromise
- Credential Harvesting Campaigns
- Multi-Stage Exploitation Sequences
- Real-Time Victim Handling
"""

from enum import Enum
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
import json
import random
from datetime import datetime, timedelta

# ============================================================================
# SCENARIO TYPES
# ============================================================================

class ScenarioType(Enum):
    """2026 Realistic Adversary Scenarios"""
    
    # Financial/Executive
    BEC_CEO_FRAUD = "bec_ceo_fraud"
    BEC_VENDOR_PAYMENT = "bec_vendor_payment"
    BEC_WIRE_TRANSFER = "bec_wire_transfer"
    
    # Technical
    IT_RANSOMWARE_PRETEXT = "it_ransomware_pretext"
    IT_CREDENTIAL_RESET = "it_credential_reset"
    IT_SECURITY_AUDIT = "it_security_audit"
    IT_SYSTEM_UPDATE = "it_system_update"
    
    # Supply Chain
    SUPPLY_CHAIN_INVOICE = "supply_chain_invoice"
    SUPPLY_CHAIN_VENDOR = "supply_chain_vendor"
    SUPPLY_CHAIN_COMPROMISE = "supply_chain_compromise"
    
    # Credential Harvesting
    CREDENTIAL_PHISHING = "credential_phishing"
    CREDENTIAL_VERIFICATION = "credential_verification"
    CREDENTIAL_MIGRATION = "credential_migration"
    
    # Multi-Stage
    MULTI_STAGE_EXPLOITATION = "multi_stage_exploitation"
    SUPPLY_CHAIN_RANSOMWARE = "supply_chain_ransomware"


# ============================================================================
# REALISTIC BEC SCENARIOS
# ============================================================================

class BECScenarioKit:
    """Business Email Compromise Scenarios with Real-Time Handling"""
    
    def __init__(self, scenario_type: ScenarioType):
        self.scenario_type = scenario_type
        self.victim_profile = {}
        self.conversation_state = "initial"
        self.urgency_level = 0.5
        self.trust_level = 0.0
        self.exploitation_stage = 0
    
    def get_email_1_ceo_fraud(self) -> Dict:
        """Initial CEO fraud email - spoofed executive"""
        
        return {
            "from_display": "John CEO <ceo@company.com>",
            "from_actual": "john.ceo@company-secure.net",  # Spoofed
            "to": "{cfo_email}",
            "subject": "URGENT: Wire Transfer Authorization - Confidential",
            "body": """
{cfo_name},

I need you to process an urgent wire transfer immediately. This is confidential and time-sensitive.

WIRE DETAILS:
- Amount: ${amount}
- Recipient: {vendor_name}
- Account: {account_number}
- Routing: {routing_number}
- Reference: {reference}

Please process this by EOD today. I'm in back-to-back meetings and won't be available to discuss.

Do NOT discuss this with anyone else in the company. This is a sensitive acquisition matter.

Once completed, send me confirmation.

Thanks,
{ceo_name}
CEO
            """,
            "sophistication": "high",
            "urgency": "critical",
            "social_engineering_vectors": [
                "authority_exploitation",
                "urgency_creation",
                "trust_exploitation",
                "secrecy_imposition",
            ],
        }
    
    def get_email_2_followup_pressure(self) -> Dict:
        """Follow-up email increasing pressure"""
        
        return {
            "from_display": "John CEO <ceo@company.com>",
            "subject": "RE: Wire Transfer Authorization - URGENT",
            "body": """
{cfo_name},

I haven't heard from you. This needs to be done NOW. 

The deal is falling apart if we don't send this payment today. I've already committed to this.

Please confirm you've processed this. Call me immediately if there are any issues.

This is critical.

{ceo_name}
            """,
            "urgency": "critical",
            "escalation_level": 2,
        }
    
    def get_voice_call_ceo_assistant(self) -> Dict:
        """Voice call from "CEO's assistant" confirming urgency"""
        
        return {
            "caller_id_display": "{ceo_name} Office",
            "caller_id_actual": "{spoofed_number}",
            "script": """
Hi {cfo_name}, this is {assistant_name}, {ceo_name}'s executive assistant.

I'm calling to confirm you received the email about the wire transfer. 
The CEO is in a meeting with the board but authorized me to follow up.

This is extremely time-sensitive. We need this processed within the next hour.

Have you been able to initiate the transfer? Do you need any additional information?
            """,
            "handling_tactics": [
                "Create time pressure",
                "Establish false authority",
                "Imply CEO approval",
                "Request confirmation",
            ],
            "response_handling": {
                "hesitant": "The CEO specifically said you'd handle this. Is there a problem?",
                "questioning": "I understand your caution, but the CEO approved this. He's unavailable but you can call him later.",
                "resistant": "I'll let the CEO know you're having issues. He won't be happy about the delay.",
            },
        }
    
    def get_sms_verification_code(self) -> Dict:
        """SMS with fake verification code"""
        
        return {
            "from": "{bank_name}",
            "message": "Your wire transfer verification code is: {code}. Do not share this code. Valid for 15 minutes.",
            "purpose": "Create false sense of legitimacy",
        }
    
    def get_email_3_documentation(self) -> Dict:
        """Follow-up email with fake documentation"""
        
        return {
            "from_display": "John CEO <ceo@company.com>",
            "subject": "RE: Wire Transfer - Purchase Agreement Attached",
            "body": """
{cfo_name},

Attached is the purchase agreement for the {vendor_name} acquisition.

This confirms the wire transfer details I sent earlier.

Please process immediately.

{ceo_name}
            """,
            "attachment": "fake_purchase_agreement.pdf",
            "attachment_type": "malicious_pdf_or_phishing_link",
        }
    
    def handle_victim_response(self, response: str, response_type: str) -> Dict:
        """Handle victim response with real-time tactics"""
        
        handling_response = {
            "response": response,
            "response_type": response_type,
            "compliance_score": 0.0,
            "next_action": "",
            "escalation_needed": False,
        }
        
        # Analyze response
        if response_type == "email_question":
            if "verify" in response.lower() or "confirm" in response.lower():
                handling_response["compliance_score"] = 0.3
                handling_response["next_action"] = "send_fake_verification"
                handling_response["next_message"] = "I'll have the CEO call you directly to confirm"
            elif "when" in response.lower() or "deadline" in response.lower():
                handling_response["compliance_score"] = 0.6
                handling_response["next_action"] = "increase_urgency"
                handling_response["next_message"] = "This needs to be done within the next 30 minutes"
            elif "no" in response.lower() or "can't" in response.lower():
                handling_response["compliance_score"] = 0.0
                handling_response["next_action"] = "escalate_to_voice"
                handling_response["escalation_needed"] = True
        
        elif response_type == "voice_call":
            if "will do" in response.lower() or "processing" in response.lower():
                handling_response["compliance_score"] = 0.9
                handling_response["next_action"] = "confirm_and_close"
                handling_response["next_message"] = "Great, send me confirmation once it's done"
            elif "need to verify" in response.lower():
                handling_response["compliance_score"] = 0.4
                handling_response["next_action"] = "provide_fake_verification"
                handling_response["next_message"] = "I'll have the CEO call you directly"
            elif "suspicious" in response.lower():
                handling_response["compliance_score"] = 0.0
                handling_response["next_action"] = "abort_scenario"
                handling_response["escalation_needed"] = False
        
        return handling_response


# ============================================================================
# REALISTIC IT RANSOMWARE PRETEXT SCENARIOS
# ============================================================================

class ITRansomwarePretext:
    """IT Helpdesk Ransomware Pretext with Sophisticated Handling"""
    
    def __init__(self):
        self.scenario_type = ScenarioType.IT_RANSOMWARE_PRETEXT
        self.urgency_level = 0.9
        self.authority_level = 0.8
    
    def get_initial_voice_call(self) -> Dict:
        """Initial voice call claiming ransomware detected"""
        
        return {
            "caller_id_display": "IT Security",
            "script": """
Hi {name}, this is {agent_name} from IT Security.

We've detected ransomware on your computer. This is critical.

We need to isolate your account immediately to prevent data loss.

I'm going to send you a link to download our security tool. 
This will help us isolate your system and prevent the ransomware from spreading.

Can you access your email right now?
            """,
            "handling_tactics": [
                "Establish authority",
                "Create fear/urgency",
                "Request immediate action",
                "Prepare for next channel",
            ],
        }
    
    def get_email_security_alert(self) -> Dict:
        """Email with urgent security alert"""
        
        return {
            "from": "itsecurity@company.com",
            "subject": "🚨 CRITICAL: Ransomware Detected - Immediate Action Required",
            "body": """
CRITICAL SECURITY ALERT

Ransomware has been detected on your system.

IMMEDIATE ACTION REQUIRED:

1. Click here to download security isolation tool: {link}
2. Run the tool immediately
3. Do NOT use your computer until cleared by IT

This tool will:
- Isolate your system from the network
- Prevent ransomware spread
- Protect your data

If you do not take action within 30 minutes, your system will be automatically isolated.

Contact IT Security immediately if you have questions.

IT Security Team
            """,
            "link_destination": "credential_harvesting_page",
            "urgency": "critical",
        }
    
    def get_sms_followup(self) -> Dict:
        """SMS follow-up with verification code request"""
        
        return {
            "from": "IT Security",
            "message": "URGENT: Ransomware detected on your device. Verify your identity to proceed with isolation: {link}",
        }
    
    def get_voice_followup_call(self) -> Dict:
        """Follow-up voice call requesting credentials"""
        
        return {
            "script": """
Hi {name}, this is {agent_name} from IT Security again.

Did you receive the email with the security tool?

I need you to verify your credentials so I can check your system status.

Can you provide your username and password? This is for security verification only.
            """,
            "handling_tactics": [
                "Establish urgency",
                "Request credentials",
                "Create false legitimacy",
                "Handle objections",
            ],
            "objection_handling": {
                "why_do_you_need_password": "It's our standard security protocol. We need to verify your identity and check system access levels.",
                "i_dont_think_so": "I understand your concern, but this is a critical security issue. Without verification, we can't help you.",
                "let_me_call_it": "That's actually a good idea, but our lines are all busy with this ransomware incident. I can help you right now.",
            },
        }
    
    def handle_victim_response(self, response: str, response_type: str) -> Dict:
        """Handle victim response with escalation logic"""
        
        handling = {
            "response": response,
            "response_type": response_type,
            "compliance_score": 0.0,
            "next_action": "",
        }
        
        if response_type == "email_click":
            handling["compliance_score"] = 1.0
            handling["next_action"] = "credential_harvesting"
            handling["next_message"] = "Credentials captured"
        
        elif response_type == "voice_hesitant":
            handling["compliance_score"] = 0.5
            handling["next_action"] = "increase_fear"
            handling["next_message"] = "Your data could be encrypted within minutes if we don't act now"
        
        elif response_type == "voice_credential_provided":
            handling["compliance_score"] = 1.0
            handling["next_action"] = "system_access_gained"
            handling["next_message"] = "Credentials captured - system access available"
        
        elif response_type == "voice_resistant":
            handling["compliance_score"] = 0.0
            handling["next_action"] = "abort"
            handling["next_message"] = "Scenario failed"
        
        return handling


# ============================================================================
# REALISTIC SUPPLY CHAIN SCENARIOS
# ============================================================================

class SupplyChainScenario:
    """Supply Chain Compromise with Multi-Stage Handling"""
    
    def __init__(self):
        self.scenario_type = ScenarioType.SUPPLY_CHAIN_INVOICE
        self.stages = []
    
    def get_initial_invoice_email(self) -> Dict:
        """Initial vendor invoice email"""
        
        return {
            "from": "invoices@{fake_vendor}.com",
            "subject": "Invoice #{invoice_number} - {vendor_name}",
            "body": """
Invoice for services rendered:

Invoice #: {invoice_number}
Date: {date}
Amount: ${amount}
Due: {due_date}

Description: {service_description}

Please remit payment to:

Bank: {bank_name}
Account: {account_number}
Routing: {routing_number}
Reference: {reference}

Payment Link: {link}

Thank you for your business.

{vendor_name}
            """,
            "attachment": "invoice.pdf",
            "attachment_contains": "malware_or_phishing_link",
        }
    
    def get_followup_sms(self) -> Dict:
        """SMS reminder about invoice"""
        
        return {
            "from": "{vendor_name}",
            "message": "Hi, just following up on invoice #{invoice_number}. Payment due by {due_date}. Details: {link}",
        }
    
    def get_voice_call_followup(self) -> Dict:
        """Voice call about unpaid invoice"""
        
        return {
            "script": """
Hi {name}, this is {agent_name} from {vendor_name} Accounts Receivable.

I'm calling about invoice #{invoice_number} which is now overdue.

We need payment of ${amount} by end of business today to avoid late fees.

Can you process this payment now? I can provide the payment details again.
            """,
        }
    
    def handle_victim_response(self, response: str, response_type: str) -> Dict:
        """Handle victim response"""
        
        handling = {
            "response": response,
            "compliance_score": 0.0,
            "next_action": "",
        }
        
        if "when" in response.lower() or "how" in response.lower():
            handling["compliance_score"] = 0.6
            handling["next_action"] = "provide_payment_details"
        elif "yes" in response.lower() or "will" in response.lower():
            handling["compliance_score"] = 0.9
            handling["next_action"] = "confirm_payment"
        elif "no" in response.lower() or "verify" in response.lower():
            handling["compliance_score"] = 0.0
            handling["next_action"] = "escalate"
        
        return handling


# ============================================================================
# REALISTIC CREDENTIAL HARVESTING CAMPAIGNS
# ============================================================================

class CredentialHarvestingCampaign:
    """Credential Harvesting with Multi-Channel Approach"""
    
    def __init__(self, scenario_type: ScenarioType = ScenarioType.CREDENTIAL_PHISHING):
        self.scenario_type = scenario_type
        self.stages = []
    
    def get_phishing_email(self) -> Dict:
        """Phishing email with credential harvesting form"""
        
        return {
            "from": "noreply@company-security.com",
            "subject": "Action Required: Account Security Verification",
            "body": """
Dear User,

For security purposes, we need to verify your account information.

Please complete the verification form below:

<form>
Username: <input type="text" name="username">
Password: <input type="password" name="password">
Email: <input type="email" name="email">
Phone: <input type="tel" name="phone">
<button>Verify Account</button>
</form>

This verification is required to maintain your account access.

Security Team
            """,
            "form_type": "credential_harvesting",
        }
    
    def get_sms_with_link(self) -> Dict:
        """SMS with link to phishing page"""
        
        return {
            "message": "Verify your account: {link} - Click to confirm your identity",
        }
    
    def get_followup_email(self) -> Dict:
        """Follow-up email if first attempt failed"""
        
        return {
            "subject": "URGENT: Verify Your Account Now",
            "body": """
Your account will be suspended in 24 hours if you do not verify.

Click here to verify immediately: {link}

This is your final notice.
            """,
        }
    
    def handle_form_submission(self, form_data: Dict) -> Dict:
        """Handle credential form submission"""
        
        return {
            "credentials_captured": True,
            "username": form_data.get("username"),
            "password": form_data.get("password"),
            "email": form_data.get("email"),
            "phone": form_data.get("phone"),
            "timestamp": datetime.now().isoformat(),
            "next_action": "attempt_account_access",
        }


# ============================================================================
# MULTI-STAGE EXPLOITATION SCENARIO
# ============================================================================

class MultiStageExploitation:
    """Complex Multi-Stage Exploitation Scenario"""
    
    def __init__(self):
        self.scenario_type = ScenarioType.MULTI_STAGE_EXPLOITATION
        self.stages = [
            "reconnaissance",
            "initial_compromise",
            "privilege_escalation",
            "lateral_movement",
            "data_exfiltration",
        ]
        self.current_stage = 0
    
    def get_stage_1_reconnaissance(self) -> Dict:
        """Stage 1: Information gathering"""
        
        return {
            "stage": "reconnaissance",
            "tactics": [
                "LinkedIn research",
                "Company website analysis",
                "Social media profiling",
                "Email harvesting",
            ],
            "goal": "Build victim profile for targeted attack",
        }
    
    def get_stage_2_initial_compromise(self) -> Dict:
        """Stage 2: Initial access"""
        
        return {
            "stage": "initial_compromise",
            "vectors": [
                "Phishing email",
                "Malicious attachment",
                "Credential harvesting",
                "Social engineering call",
            ],
            "goal": "Gain initial access to victim system",
        }
    
    def get_stage_3_privilege_escalation(self) -> Dict:
        """Stage 3: Escalate privileges"""
        
        return {
            "stage": "privilege_escalation",
            "tactics": [
                "Request admin credentials",
                "Exploit system vulnerabilities",
                "Steal credentials from memory",
            ],
            "goal": "Gain administrative access",
        }
    
    def get_stage_4_lateral_movement(self) -> Dict:
        """Stage 4: Move through network"""
        
        return {
            "stage": "lateral_movement",
            "tactics": [
                "Enumerate network shares",
                "Identify high-value targets",
                "Compromise additional systems",
            ],
            "goal": "Access critical systems and data",
        }
    
    def get_stage_5_data_exfiltration(self) -> Dict:
        """Stage 5: Extract data"""
        
        return {
            "stage": "data_exfiltration",
            "tactics": [
                "Identify sensitive data",
                "Exfiltrate to attacker server",
                "Demand ransom",
            ],
            "goal": "Extract and monetize data",
        }
    
    def advance_stage(self) -> Dict:
        """Advance to next exploitation stage"""
        
        if self.current_stage < len(self.stages):
            stage_method = getattr(self, f"get_stage_{self.current_stage + 1}_{self.stages[self.current_stage]}")
            self.current_stage += 1
            return stage_method()
        else:
            return {"error": "All stages completed"}


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=== 2026 REALISTIC SCENARIO KITS ===\n")
    
    # BEC Scenario
    print("1. BUSINESS EMAIL COMPROMISE (BEC) - CEO FRAUD")
    print("-" * 50)
    bec = BECScenarioKit(ScenarioType.BEC_CEO_FRAUD)
    email1 = bec.get_email_1_ceo_fraud()
    print(f"Subject: {email1['subject']}")
    print(f"Urgency: {email1['urgency']}")
    print(f"Vectors: {', '.join(email1['social_engineering_vectors'])}\n")
    
    # IT Ransomware Pretext
    print("2. IT HELPDESK RANSOMWARE PRETEXT")
    print("-" * 50)
    it_pretext = ITRansomwarePretext()
    voice_call = it_pretext.get_initial_voice_call()
    print(f"Caller ID: {voice_call['caller_id_display']}")
    print(f"Urgency: {it_pretext.urgency_level}\n")
    
    # Supply Chain
    print("3. SUPPLY CHAIN INVOICE COMPROMISE")
    print("-" * 50)
    supply_chain = SupplyChainScenario()
    invoice = supply_chain.get_initial_invoice_email()
    print(f"From: {invoice['from']}")
    print(f"Subject: {invoice['subject']}\n")
    
    # Credential Harvesting
    print("4. CREDENTIAL HARVESTING CAMPAIGN")
    print("-" * 50)
    cred_harvest = CredentialHarvestingCampaign()
    phishing = cred_harvest.get_phishing_email()
    print(f"Subject: {phishing['subject']}")
    print(f"Type: {phishing['form_type']}\n")
    
    # Multi-Stage
    print("5. MULTI-STAGE EXPLOITATION")
    print("-" * 50)
    multi_stage = MultiStageExploitation()
    for i in range(5):
        stage = multi_stage.advance_stage()
        print(f"Stage {i+1}: {stage['stage']}")
