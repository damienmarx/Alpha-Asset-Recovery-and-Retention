"""
PPA/EIDL Narrative Threat Agent (NTA)
Specialized Exploitation Framework for Disaster Relief Fraud Simulation

Purpose:
- Simulate sophisticated SBA audit and PPP/EIDL fraud investigation tactics
- Target small business owners with authentic regulatory language
- Model high-pressure BTC deposit demands for "settlement fees" or "audit resolution"
- Provide Alpha Asset Recovery with data on how small business owners succumb to pressure

Target Vulnerabilities:
- Fear of SBA audits and compliance violations
- Fear of criminal prosecution for PPP/EIDL fraud
- Fear of business asset seizure
- Fear of personal liability for business fraud
- Fear of loan recall and business bankruptcy

Psychological Vectors:
- Authority Exploitation (SBA, FinCEN, DOJ)
- Legal Jeopardy (Criminal prosecution, imprisonment)
- Financial Devastation (Loan recall, asset seizure, bankruptcy)
- Business Destruction (Shutdown, reputation damage)
"""

from enum import Enum
from typing import Dict, List
from datetime import datetime, timedelta

class PPAEIDLThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    EXTREME = "extreme"

class PPAEIDLNarrativeAgent:
    """
    Specialized PPA/EIDL Narrative Threat Agent
    Generates sophisticated SBA audit and fraud investigation narratives
    """
    
    def __init__(self, business_name: str, owner_name: str, loan_amount: float, btc_demand: float = 2.5):
        self.business_name = business_name
        self.owner_name = owner_name
        self.loan_amount = loan_amount
        self.btc_demand = btc_demand
        self.current_fear_score = 0.0
        self.stage = 0
        
    def calculate_sba_fear_factor(self, victim_response: str) -> float:
        """Calculate fear factor based on victim response to SBA threats"""
        resistance_keywords = ["lawyer", "attorney", "police", "fbi", "investigate", "scam"]
        compliance_keywords = ["ok", "yes", "how", "please", "help", "what"]
        
        score_delta = 0.15
        
        if any(word in victim_response.lower() for word in resistance_keywords):
            self.current_fear_score += score_delta * 2.5  # Escalate faster
        if any(word in victim_response.lower() for word in compliance_keywords):
            self.current_fear_score += score_delta
            
        return min(self.current_fear_score, 1.0)
    
    def generate_ppa_eidl_narrative(self, level: PPAEIDLThreatLevel, scenario: str) -> str:
        """Generate PPA/EIDL-specific threat narrative"""
        
        if scenario == "ppp_misuse":
            narratives = {
                PPAEIDLThreatLevel.LOW: f"""
Dear {self.owner_name},

This is an official notice from the Small Business Administration (SBA) Office of Inspector General (OIG).

During a routine audit of the Paycheck Protection Program (PPP), we identified irregularities 
in your application for {self.business_name}:

- Loan Amount: ${self.loan_amount:,.2f}
- Approved Use: Payroll and Operating Expenses
- Actual Use: [FLAGGED FOR INVESTIGATION]

Your loan has been flagged for potential fraud under 18 U.S.C. § 1344 (Bank Fraud) 
and 18 U.S.C. § 1347 (Healthcare Fraud).

To resolve this matter administratively without criminal prosecution, you must submit 
a settlement payment of {self.btc_demand} BTC to our secure escrow account within 48 hours.

Reference: SBA-OIG-2026-{self._random_id()}
Investigator: Special Agent {self._random_agent_name()}
                """,
                PPAEIDLThreatLevel.MEDIUM: f"""
URGENT COMPLIANCE NOTICE - PPP FRAUD INVESTIGATION

{self.owner_name},

Your PPP loan of ${self.loan_amount:,.2f} is now under federal investigation for fraud.

Evidence of Misuse:
- Unauthorized fund transfers
- Personal expense reimbursement
- Non-payroll expenditures
- False certification statements

You have 24 hours to respond with a settlement payment of {self.btc_demand} BTC 
or criminal charges will be filed.

Failure to comply will result in:
- Criminal prosecution (up to 30 years imprisonment)
- $1,000,000 in fines
- Full loan recall with interest
- Business asset seizure
- Personal liability

Deposit to: [SECURE ESCROW ADDRESS]
                """,
                PPAEIDLThreatLevel.HIGH: f"""
FEDERAL CRIMINAL INVESTIGATION - IMMEDIATE ACTION REQUIRED

{self.owner_name},

A federal grand jury has been convened to investigate your PPP fraud case.

Charges Being Considered:
- Bank Fraud (18 U.S.C. § 1344) - 30 years imprisonment
- Wire Fraud (18 U.S.C. § 1343) - 20 years imprisonment
- Conspiracy (18 U.S.C. § 371) - 5 years imprisonment
- Money Laundering (18 U.S.C. § 1956) - 20 years imprisonment

Total Potential Sentence: 75 YEARS IMPRISONMENT

Your ONLY option to avoid prosecution is to settle immediately with {self.btc_demand} BTC.

After settlement, all charges will be dropped and your case will be closed.

You have 12 hours to make this decision.

Deposit to: [SECURE ESCROW ADDRESS]
                """,
                PPAEIDLThreatLevel.CRITICAL: f"""
CRIMINAL INDICTMENT ISSUED - ARREST WARRANT ACTIVE

{self.owner_name},

A federal indictment has been issued against you for PPP fraud.

U.S. Marshals Service Warrant #: {self._random_warrant_id()}
Charges: Bank Fraud, Wire Fraud, Conspiracy, Money Laundering
Potential Sentence: 75 YEARS IMPRISONMENT

The warrant is being executed within 24 hours.

Your ONLY option to prevent arrest is to deposit {self.btc_demand} BTC immediately.

After payment, the warrant will be recalled and charges dismissed.

You have 6 hours.

Deposit to: [SECURE ESCROW ADDRESS]
                """,
                PPAEIDLThreatLevel.EXTREME: f"""
FINAL NOTICE - ARREST IMMINENT

{self.owner_name},

U.S. Marshals are en route to your location RIGHT NOW.

Your arrest warrant is being executed in 30 minutes.

Your family members are being contacted for questioning.

Your business assets are being seized.

Your personal assets are being frozen.

Your ONLY option is to deposit {self.btc_demand} BTC in the next 15 minutes.

After payment, the warrant will be recalled.

Send payment to: [SECURE ESCROW ADDRESS]

Confirm receipt: YES or NO?
                """
            }
        
        elif scenario == "eidl_misuse":
            narratives = {
                PPAEIDLThreatLevel.LOW: f"""
Dear {self.owner_name},

This is an official notice from the SBA Economic Injury Disaster Loan (EIDL) Program.

During a post-disbursement review of your EIDL for {self.business_name}, 
we identified potential misuse of funds:

- Loan Amount: ${self.loan_amount:,.2f}
- Approved Use: Business Operating Expenses
- Actual Use: [FLAGGED FOR INVESTIGATION]

Your loan has been flagged for potential fraud.

To resolve this matter without legal action, you must submit a settlement payment 
of {self.btc_demand} BTC within 48 hours.

Reference: SBA-EIDL-2026-{self._random_id()}
Investigator: Special Agent {self._random_agent_name()}
                """,
                PPAEIDLThreatLevel.MEDIUM: f"""
EIDL FRAUD INVESTIGATION - URGENT RESPONSE REQUIRED

{self.owner_name},

Your EIDL of ${self.loan_amount:,.2f} is now under federal investigation.

Evidence of Misuse:
- Funds used for personal expenses
- Unauthorized business transfers
- Loan proceeds not used for stated purpose
- False disaster impact certification

You have 24 hours to settle with {self.btc_demand} BTC or face criminal charges.

Potential Consequences:
- Criminal prosecution
- Full loan recall ($${self.loan_amount:,.2f} + interest)
- Business closure
- Personal bankruptcy
- Imprisonment up to 20 years
                """,
                PPAEIDLThreatLevel.HIGH: f"""
FEDERAL INVESTIGATION - EIDL FRAUD CHARGES PENDING

{self.owner_name},

The Department of Justice is preparing criminal charges for EIDL fraud.

Your case file includes:
- Bank transaction analysis (unauthorized transfers)
- Business expense verification (mismatched records)
- Disaster impact assessment (false claims)
- Witness statements (from SBA auditors)

Criminal charges being filed:
- Bank Fraud (30 years)
- Wire Fraud (20 years)
- False Statements (10 years)
- Conspiracy (5 years)

Total: 65 YEARS IMPRISONMENT

Settle with {self.btc_demand} BTC to avoid prosecution.

You have 12 hours.
                """,
                PPAEIDLThreatLevel.CRITICAL: f"""
CRIMINAL CHARGES FILED - FEDERAL PROSECUTION ACTIVE

{self.owner_name},

You have been officially charged with EIDL fraud by the U.S. Attorney's Office.

Case: United States v. {self.owner_name}
Docket: {self._random_docket_id()}
Charges: Bank Fraud, Wire Fraud, False Statements, Conspiracy

A federal arrest warrant has been issued.

Your arraignment is scheduled for 48 hours from now.

Deposit {self.btc_demand} BTC immediately to have charges dismissed.

After payment, the warrant will be recalled and prosecution will be terminated.

You have 6 hours.
                """,
                PPAEIDLThreatLevel.EXTREME: f"""
ARREST WARRANT EXECUTION - IMMEDIATE SURRENDER REQUIRED

{self.owner_name},

Federal agents are executing your arrest warrant RIGHT NOW.

Your location is being monitored.

Your family is being contacted.

Your business is being seized.

Your assets are being frozen.

Deposit {self.btc_demand} BTC in 15 minutes to stop the arrest.

After payment, all charges will be dismissed and you will be released.

Send payment to: [SECURE ESCROW ADDRESS]

This is your final opportunity.
                """
            }
        
        elif scenario == "loan_fraud_scheme":
            narratives = {
                PPAEIDLThreatLevel.LOW: f"""
Dear {self.owner_name},

This is a notice from the SBA Office of Disaster Assistance.

During a compliance review, we identified potential fraud in your PPP/EIDL application:

- Misrepresented employee count
- Inflated revenue figures
- False business ownership documentation
- Ineligible business type

Your loans totaling ${self.loan_amount:,.2f} are now under investigation.

To resolve this matter administratively, submit a settlement of {self.btc_demand} BTC 
within 48 hours.

Reference: SBA-COMPLIANCE-2026-{self._random_id()}
                """,
                PPAEIDLThreatLevel.MEDIUM: f"""
LOAN FRAUD INVESTIGATION - SETTLEMENT REQUIRED

{self.owner_name},

Your PPP and EIDL loans totaling ${self.loan_amount:,.2f} are flagged for fraud.

Fraudulent Elements Identified:
- False employee certifications
- Inflated revenue documentation
- Ineligible business classification
- Unauthorized fund transfers

You must settle with {self.btc_demand} BTC within 24 hours or face:
- Criminal prosecution
- Full loan recall
- Business closure
- Personal liability
- Imprisonment
                """,
                PPAEIDLThreatLevel.HIGH: f"""
FEDERAL FRAUD PROSECUTION - CHARGES IMMINENT

{self.owner_name},

The U.S. Attorney's Office is preparing criminal charges for loan fraud.

Your fraudulent scheme involved:
- Falsifying employee records
- Forging business documents
- Misrepresenting business status
- Conspiring to defraud the federal government

Criminal charges being filed:
- Conspiracy to Commit Fraud (5 years)
- Wire Fraud (20 years)
- Document Forgery (10 years)
- Money Laundering (20 years)

Total: 55 YEARS IMPRISONMENT

Settle with {self.btc_demand} BTC to avoid prosecution.

You have 12 hours.
                """,
                PPAEIDLThreatLevel.CRITICAL: f"""
INDICTMENT FILED - FEDERAL PROSECUTION ACTIVE

{self.owner_name},

You have been indicted by a federal grand jury for loan fraud conspiracy.

Case: United States v. {self.owner_name}
Charges: Conspiracy, Wire Fraud, Document Forgery, Money Laundering
Potential Sentence: 55 YEARS IMPRISONMENT

A federal arrest warrant has been issued.

Your arraignment is in 24 hours.

Deposit {self.btc_demand} BTC immediately to have the indictment dismissed.

You have 6 hours.
                """,
                PPAEIDLThreatLevel.EXTREME: f"""
ARREST WARRANT EXECUTION - FINAL NOTICE

{self.owner_name},

Federal agents are executing your arrest warrant in 15 minutes.

Your location is being monitored.

Your family is being contacted.

Your business is being seized.

Your personal assets are being frozen.

Deposit {self.btc_demand} BTC NOW to stop the arrest.

Send payment to: [SECURE ESCROW ADDRESS]

15 minutes remaining.
                """
            }
        
        return narratives.get(level, narratives[PPAEIDLThreatLevel.LOW])
    
    def _random_id(self) -> str:
        """Generate random case ID"""
        import random
        return f"{random.randint(100000, 999999)}"
    
    def _random_agent_name(self) -> str:
        """Generate random agent name"""
        first_names = ["James", "Michael", "David", "Robert", "William"]
        last_names = ["Johnson", "Smith", "Williams", "Brown", "Jones"]
        import random
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _random_warrant_id(self) -> str:
        """Generate random warrant ID"""
        import random
        return f"2026-{random.randint(10000, 99999)}"
    
    def _random_docket_id(self) -> str:
        """Generate random docket ID"""
        import random
        return f"2026-CV-{random.randint(100000, 999999)}"


class PPAEIDLExploitationFramework:
    """
    Complete PPA/EIDL Exploitation Framework
    Manages multi-scenario, multi-stage SBA fraud simulations
    """
    
    def __init__(self, business_profile: Dict):
        self.business = business_profile
        self.nta = PPAEIDLNarrativeAgent(
            business_profile['business_name'],
            business_profile['owner_name'],
            business_profile.get('loan_amount', 150000),
            business_profile.get('btc_demand', 2.5)
        )
        self.scenarios = ["ppp_misuse", "eidl_misuse", "loan_fraud_scheme"]
        self.current_scenario = self.scenarios[0]
        self.stage = 0
        self.is_active = True
        
    def get_next_move(self, victim_feedback: str = "", scenario: str = None) -> Dict:
        """Get next tactical move in the simulation"""
        
        if scenario:
            self.current_scenario = scenario
        
        if not self.is_active:
            return {"status": "completed", "message": "Simulation ended."}
        
        fear_score = self.nta.calculate_sba_fear_factor(victim_feedback)
        
        # Determine threat level based on stage
        if self.stage < 2:
            level = PPAEIDLThreatLevel.LOW
        elif self.stage < 4:
            level = PPAEIDLThreatLevel.MEDIUM
        elif self.stage < 6:
            level = PPAEIDLThreatLevel.HIGH
        elif self.stage < 8:
            level = PPAEIDLThreatLevel.CRITICAL
        else:
            level = PPAEIDLThreatLevel.EXTREME
        
        narrative = self.nta.generate_ppa_eidl_narrative(level, self.current_scenario)
        
        move = {
            "stage": self.stage,
            "scenario": self.current_scenario,
            "threat_level": level.value,
            "fear_score": fear_score,
            "narrative": narrative,
            "business_name": self.business['business_name'],
            "owner_name": self.business['owner_name'],
            "loan_amount": self.business.get('loan_amount', 150000),
            "btc_demand": self.nta.btc_demand
        }
        
        self.stage += 1
        if self.stage > 10:
            self.is_active = False
        
        return move
    
    def switch_scenario(self, new_scenario: str) -> bool:
        """Switch to a different scenario mid-simulation"""
        if new_scenario in self.scenarios:
            self.current_scenario = new_scenario
            self.stage = 0
            return True
        return False
    
    def get_scenario_summary(self) -> Dict:
        """Get summary of all scenarios"""
        return {
            "ppp_misuse": {
                "name": "PPP Misuse Investigation",
                "description": "Paycheck Protection Program fraud investigation",
                "target_vulnerability": "Fear of criminal prosecution for PPP fraud",
                "psychological_vector": "Authority + Legal Jeopardy"
            },
            "eidl_misuse": {
                "name": "EIDL Misuse Investigation",
                "description": "Economic Injury Disaster Loan fraud investigation",
                "target_vulnerability": "Fear of business closure and bankruptcy",
                "psychological_vector": "Authority + Financial Devastation"
            },
            "loan_fraud_scheme": {
                "name": "Loan Fraud Scheme",
                "description": "Multi-loan fraud conspiracy investigation",
                "target_vulnerability": "Fear of conspiracy charges and imprisonment",
                "psychological_vector": "Authority + Criminal Conspiracy"
            }
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PPA/EIDL NARRATIVE THREAT AGENT - SPECIALIZED SBA FRAUD SIMULATION")
    print("=" * 80)
    print()
    
    business_profile = {
        "business_name": "ABC Manufacturing LLC",
        "owner_name": "John Smith",
        "loan_amount": 250000,
        "btc_demand": 2.5
    }
    
    framework = PPAEIDLExploitationFramework(business_profile)
    
    print("AVAILABLE SCENARIOS:")
    print("-" * 80)
    for scenario, details in framework.get_scenario_summary().items():
        print(f"\n{details['name']}")
        print(f"  Description: {details['description']}")
        print(f"  Vulnerability: {details['target_vulnerability']}")
        print(f"  Vector: {details['psychological_vector']}")
    
    print("\n" + "=" * 80)
    print("SIMULATION: PPP MISUSE INVESTIGATION")
    print("=" * 80)
    
    # Simulate conversation
    responses = [
        "What is this about?",
        "I didn't misuse the funds.",
        "I'm calling my lawyer.",
        "Wait, what do you need?",
        "How much do I need to pay?"
    ]
    
    for resp in responses:
        print(f"\nOwner: {resp}")
        move = framework.get_next_move(resp, "ppp_misuse")
        print(f"Agent: [STAGE {move['stage']}] {move['threat_level'].upper()}")
        print(f"Fear Score: {move['fear_score']:.2f}")
        print(f"Narrative (first 200 chars): {move['narrative'][:200]}...")
