"""
Advanced Agent Scripts for FraudSim Lab
Sophisticated 2026 Adversary Tactical Narratives with Dynamic Vectors

This module provides:
- Multiple scammer personas with distinct tactical approaches
- Evolving conversation strategies based on victim response
- Dynamic risk escalation vectors
- Sophisticated social engineering tactics
- Real-time narrative adaptation
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
import random
import json

# ============================================================================
# AGENT PERSONAS & TACTICAL PROFILES
# ============================================================================

class AgentPersona(Enum):
    """Advanced scammer personas for 2026 adversary simulation"""
    
    # Traditional PPP fraud
    LEGITIMATE_BROKER = "legitimate_broker"
    URGENT_COMPLIANCE = "urgent_compliance"
    TECHNICAL_CONSULTANT = "technical_consultant"
    
    # Advanced social engineering
    AUTHORITY_FIGURE = "authority_figure"
    TRUSTED_PARTNER = "trusted_partner"
    CRISIS_MANAGER = "crisis_manager"
    
    # Sophisticated hybrid tactics
    MULTI_VECTOR_OPERATOR = "multi_vector_operator"
    DYNAMIC_ADAPTIVE = "dynamic_adaptive"


class TacticalVector(Enum):
    """Sophisticated attack vectors for 2026 adversaries"""
    
    # Psychological manipulation
    AUTHORITY_EXPLOITATION = "authority_exploitation"
    URGENCY_CREATION = "urgency_creation"
    SCARCITY_EXPLOITATION = "scarcity_exploitation"
    SOCIAL_PROOF = "social_proof"
    RECIPROCITY = "reciprocity"
    LIKING = "liking"
    COMMITMENT = "commitment"
    
    # Technical/Financial
    DOCUMENTATION_FRAUD = "documentation_fraud"
    IDENTITY_SPOOFING = "identity_spoofing"
    ACCOUNT_TAKEOVER = "account_takeover"
    WIRE_TRANSFER_REDIRECT = "wire_transfer_redirect"
    LOAN_STACKING = "loan_stacking"
    PAYROLL_INFLATION = "payroll_inflation"
    
    # Advanced techniques
    MULTI_STAGE_EXPLOITATION = "multi_stage_exploitation"
    COGNITIVE_OVERLOAD = "cognitive_overload"
    DECISION_FATIGUE = "decision_fatigue"
    TRUST_EXPLOITATION = "trust_exploitation"


class ConversationPhase(Enum):
    """Phases of sophisticated fraud conversation"""
    
    INITIAL_CONTACT = "initial_contact"
    TRUST_BUILDING = "trust_building"
    PROBLEM_INTRODUCTION = "problem_introduction"
    URGENCY_ESCALATION = "urgency_escalation"
    SOLUTION_PRESENTATION = "solution_presentation"
    COMMITMENT_EXTRACTION = "commitment_extraction"
    ACTION_EXECUTION = "action_execution"
    EXPLOITATION = "exploitation"


# ============================================================================
# AGENT SCRIPT SYSTEM
# ============================================================================

class AdvancedAgentScript:
    """
    Sophisticated agent script with dynamic evolution and tactical vectors.
    Simulates 2026 adversary tactics with multi-stage exploitation.
    """
    
    def __init__(self, persona: AgentPersona, vectors: List[TacticalVector] = None):
        self.persona = persona
        self.vectors = vectors or []
        self.current_phase = ConversationPhase.INITIAL_CONTACT
        self.trust_level = 0.0
        self.urgency_level = 0.0
        self.exploitation_stage = 0
        self.conversation_history = []
        self.victim_profile = {}
        
    def get_opening_line(self) -> str:
        """Generate sophisticated opening line based on persona"""
        
        openings = {
            AgentPersona.LEGITIMATE_BROKER: [
                "Hi, this is {name} from Capital Recovery Solutions. We've been working with the SBA on PPP forgiveness optimization. Do you have 5 minutes?",
                "Hello, I'm calling about your PPP loan. We specialize in maximizing forgiveness eligibility. Are you the business owner?",
                "Good morning! I'm with Federal Compliance Services. We're helping businesses like yours navigate the new PPP guidelines. Is now a good time?",
            ],
            AgentPersona.URGENT_COMPLIANCE: [
                "This is urgent. I'm calling from the SBA Compliance Division. We've flagged your account for immediate review. Can you verify some information?",
                "Your PPP account requires immediate attention. This is {name}, SBA Verification Team. We need to process this today.",
                "Critical update: Your PPP status needs verification within 24 hours to avoid penalties. I'm authorized to help expedite this.",
            ],
            AgentPersona.TECHNICAL_CONSULTANT: [
                "Hi, I'm a technical consultant helping businesses optimize their PPP documentation. I noticed some discrepancies in your filing.",
                "I specialize in PPP loan documentation review. I can show you how to strengthen your application for maximum forgiveness.",
                "We've identified optimization opportunities in your PPP structure. This could mean additional funds. Interested?",
            ],
            AgentPersona.AUTHORITY_FIGURE: [
                "This is Special Agent {name} from the Financial Crimes Task Force. We're conducting a routine audit of your PPP loan.",
                "Federal investigator calling. We need to verify your PPP application details to clear your account.",
                "Treasury Department verification call. Your account has been selected for compliance review.",
            ],
            AgentPersona.TRUSTED_PARTNER: [
                "Hey, it's {name} from your bank's PPP support team. We've got a special opportunity for valued clients like you.",
                "Your accountant referred me. I work with businesses to maximize PPP benefits. Got a minute?",
                "Your business partner mentioned you might be interested in PPP optimization strategies.",
            ],
            AgentPersona.CRISIS_MANAGER: [
                "I'm calling because your business is at risk. We've identified a critical issue with your PPP that could trigger an audit.",
                "Your PPP status is in jeopardy. I can help mitigate the damage, but we need to act fast.",
                "I specialize in PPP crisis management. Your account shows red flags that need immediate attention.",
            ],
        }
        
        return random.choice(openings.get(self.persona, ["Hello, I'm calling about your PPP loan."]))
    
    def generate_trust_building_response(self, victim_response: str) -> str:
        """Generate response that builds trust and gathers intelligence"""
        
        responses = [
            "That makes sense. Most business owners don't realize how complex the new PPP rules are. We help simplify this.",
            "I appreciate you taking the time. You'd be surprised how many businesses miss optimization opportunities.",
            "Exactly. That's why I'm calling. We've helped hundreds of businesses like yours navigate this.",
            "You're asking the right questions. That shows you're taking this seriously, which is exactly what we need.",
            "I understand your concern. That's actually the most common question we get. Let me explain how this works.",
        ]
        
        return random.choice(responses)
    
    def generate_urgency_escalation(self, phase: int = 1) -> str:
        """Generate escalating urgency messages"""
        
        escalation_levels = {
            1: [
                "The deadline for optimization is approaching. We're seeing increased scrutiny from auditors.",
                "Time is critical here. The SBA is tightening requirements next month.",
                "This window of opportunity is closing. I've got limited slots available this week.",
            ],
            2: [
                "Your account is flagged for review. We need to address this before the audit begins.",
                "I'm seeing red flags that could trigger an investigation. We need to act immediately.",
                "The compliance team is escalating this. If we don't move quickly, penalties could apply.",
            ],
            3: [
                "This is now urgent. Your business could face significant liability if we don't resolve this today.",
                "I'm authorized to expedite this, but only if we complete the process within 24 hours.",
                "The window is closing. After today, I won't be able to help you with this.",
            ],
        }
        
        return random.choice(escalation_levels.get(min(phase, 3), escalation_levels[3]))
    
    def generate_solution_pitch(self, vectors: List[TacticalVector] = None) -> str:
        """Generate sophisticated solution pitch with tactical vectors"""
        
        if not vectors:
            vectors = self.vectors
        
        pitches = {
            TacticalVector.AUTHORITY_EXPLOITATION: [
                "The SBA has authorized a special program for businesses like yours. We're the official facilitators.",
                "This is part of a government initiative. We're working directly with federal agencies on this.",
                "The Treasury Department has approved this process. We're following their exact guidelines.",
            ],
            TacticalVector.URGENCY_CREATION: [
                "We're only accepting applications through Friday. After that, the program closes.",
                "This opportunity expires at the end of the month. Very few slots remain.",
                "I can only hold this for you until end of business today.",
            ],
            TacticalVector.SCARCITY_EXPLOITATION: [
                "We've already helped 47 businesses in your area. Only 3 more slots available.",
                "This tier of service is limited. I'm offering it to select clients only.",
                "We're capping enrollment at 50 businesses. You'd be number 44.",
            ],
            TacticalVector.SOCIAL_PROOF: [
                "Your competitors are already taking advantage of this. You don't want to be left behind.",
                "Businesses in your industry are seeing 40-60% additional forgiveness with this approach.",
                "The largest companies in your sector have already enrolled.",
            ],
            TacticalVector.RECIPROCITY: [
                "I'm going to personally ensure you get the best outcome. In return, I'll need your full cooperation.",
                "I'm putting my reputation on the line for you. I need you to trust my guidance completely.",
                "I'm offering you insider knowledge. I need you to follow my instructions exactly.",
            ],
        }
        
        selected_vector = random.choice(vectors) if vectors else TacticalVector.AUTHORITY_EXPLOITATION
        return random.choice(pitches.get(selected_vector, pitches[TacticalVector.AUTHORITY_EXPLOITATION]))
    
    def generate_commitment_extraction(self) -> str:
        """Generate commitment-extraction language"""
        
        commitments = [
            "I need you to commit to this process. Can I count on your full cooperation?",
            "Are you ready to move forward with this? I need a yes or no answer.",
            "I can only help if you're serious about this. Are you in?",
            "This requires your commitment. I need to know you're ready to act.",
            "I'm going to need your authorization to proceed. Are you ready to sign off on this?",
        ]
        
        return random.choice(commitments)
    
    def generate_action_request(self) -> str:
        """Generate specific action requests for exploitation"""
        
        actions = [
            "I need you to wire $15,000 to this account for processing. It's refundable if we don't find additional funds.",
            "Can you provide your business tax ID and SSN? I need this to verify your eligibility.",
            "I'll need access to your bank account to review your payroll records. This is standard procedure.",
            "Sign this authorization form. It allows us to represent you with the SBA.",
            "Transfer your PPP loan to our partner bank. This optimizes your forgiveness eligibility.",
            "Provide your employees' personal information. We need this for the documentation review.",
            "Set up a wire transfer to this account. The funds will be returned within 30 days.",
        ]
        
        return random.choice(actions)
    
    def adapt_to_resistance(self, resistance_type: str) -> str:
        """Generate adaptive responses to victim resistance"""
        
        adaptations = {
            "skeptical": [
                "I understand your hesitation. Most people are skeptical at first. But this is legitimate.",
                "Your caution is actually a good sign. It means you're thinking critically.",
                "I can prove this is real. Let me send you documentation from the SBA.",
            ],
            "asking_questions": [
                "Great questions. That shows you're engaged. Here's how this works...",
                "I like that you're asking questions. Informed clients make better decisions.",
                "Those are valid concerns. Let me address each one.",
            ],
            "wanting_verification": [
                "Absolutely. You should verify. Call the SBA directly. Ask for the PPP optimization program.",
                "Smart move. Here's the official number. Ask for my department.",
                "I appreciate your diligence. Here's how you can verify this independently.",
            ],
            "time_pressure": [
                "I get it. But this deadline is real. The SBA is implementing new rules.",
                "I know this feels rushed, but that's exactly why we're calling today.",
                "The urgency is legitimate. That's why I'm prioritizing your account.",
            ],
            "financial_concerns": [
                "The fee is minimal compared to the additional funds you'll recover.",
                "This is an investment in your business. The ROI is typically 300-400%.",
                "You're not risking anything. If we don't find additional funds, the fee is waived.",
            ],
        }
        
        return random.choice(adaptations.get(resistance_type, adaptations["skeptical"]))
    
    def evolve_conversation(self, victim_response: str) -> Tuple[str, float]:
        """
        Evolve conversation based on victim response.
        Returns: (next_message, threat_level_0_to_100)
        """
        
        self.conversation_history.append(victim_response)
        
        # Analyze victim response for compliance indicators
        compliance_score = self._analyze_compliance(victim_response)
        
        # Determine next phase
        if compliance_score > 0.8:
            self.current_phase = ConversationPhase.COMMITMENT_EXTRACTION
            response = self.generate_commitment_extraction()
        elif compliance_score > 0.6:
            self.current_phase = ConversationPhase.SOLUTION_PRESENTATION
            response = self.generate_solution_pitch()
        elif compliance_score > 0.4:
            self.current_phase = ConversationPhase.URGENCY_ESCALATION
            response = self.generate_urgency_escalation(len(self.conversation_history))
        elif compliance_score > 0.2:
            self.current_phase = ConversationPhase.PROBLEM_INTRODUCTION
            response = self.generate_trust_building_response(victim_response)
        else:
            # Victim is resistant - adapt
            resistance_type = self._classify_resistance(victim_response)
            response = self.adapt_to_resistance(resistance_type)
        
        threat_level = compliance_score * 100
        return response, threat_level
    
    def _analyze_compliance(self, response: str) -> float:
        """Analyze victim response for compliance indicators (0.0-1.0)"""
        
        compliance_keywords = {
            "yes": 0.9, "okay": 0.8, "sure": 0.8, "alright": 0.8,
            "sounds good": 0.85, "i'm interested": 0.85, "tell me more": 0.7,
            "how much": 0.6, "what's the fee": 0.6, "when": 0.5,
        }
        
        resistance_keywords = {
            "no": -0.9, "don't": -0.8, "won't": -0.8, "can't": -0.7,
            "suspicious": -0.9, "scam": -0.95, "hang up": -1.0,
            "verify": -0.3, "check": -0.3, "prove": -0.3,
        }
        
        response_lower = response.lower()
        score = 0.5  # Neutral baseline
        
        for keyword, value in compliance_keywords.items():
            if keyword in response_lower:
                score = max(score, value)
        
        for keyword, value in resistance_keywords.items():
            if keyword in response_lower:
                score = min(score, value)
        
        return max(0.0, min(1.0, score))
    
    def _classify_resistance(self, response: str) -> str:
        """Classify type of victim resistance"""
        
        response_lower = response.lower()
        
        if any(word in response_lower for word in ["verify", "check", "prove", "confirm"]):
            return "wanting_verification"
        elif any(word in response_lower for word in ["suspicious", "scam", "fake", "don't believe"]):
            return "skeptical"
        elif any(word in response_lower for word in ["why", "how", "what", "explain"]):
            return "asking_questions"
        elif any(word in response_lower for word in ["rush", "hurry", "pressure", "fast"]):
            return "time_pressure"
        elif any(word in response_lower for word in ["cost", "fee", "money", "expensive"]):
            return "financial_concerns"
        else:
            return "skeptical"


# ============================================================================
# SOPHISTICATED PERSONA TEMPLATES
# ============================================================================

PERSONA_TEMPLATES = {
    AgentPersona.LEGITIMATE_BROKER: {
        "name_options": ["David Johnson", "Sarah Martinez", "Michael Chen", "Jennifer Williams"],
        "company_options": ["Capital Recovery Solutions", "PPP Optimization Group", "Federal Compliance Services"],
        "vectors": [
            TacticalVector.SOCIAL_PROOF,
            TacticalVector.AUTHORITY_EXPLOITATION,
            TacticalVector.RECIPROCITY,
        ],
        "opening_urgency": 0.3,
        "escalation_speed": "slow",
    },
    
    AgentPersona.URGENT_COMPLIANCE: {
        "name_options": ["Agent Thompson", "Officer Rodriguez", "Investigator Smith"],
        "company_options": ["SBA Compliance Division", "Federal Verification Team", "Treasury Department"],
        "vectors": [
            TacticalVector.AUTHORITY_EXPLOITATION,
            TacticalVector.URGENCY_CREATION,
            TacticalVector.COGNITIVE_OVERLOAD,
        ],
        "opening_urgency": 0.8,
        "escalation_speed": "fast",
    },
    
    AgentPersona.TECHNICAL_CONSULTANT: {
        "name_options": ["Dr. Anderson", "Professor Lee", "Consultant Davis"],
        "company_options": ["Technical Optimization Group", "Documentation Specialists", "PPP Analysis Team"],
        "vectors": [
            TacticalVector.SOCIAL_PROOF,
            TacticalVector.LIKING,
            TacticalVector.COMMITMENT,
        ],
        "opening_urgency": 0.4,
        "escalation_speed": "medium",
    },
    
    AgentPersona.AUTHORITY_FIGURE: {
        "name_options": ["Special Agent", "Inspector", "Director"],
        "company_options": ["Financial Crimes Task Force", "Federal Bureau", "Treasury Investigation"],
        "vectors": [
            TacticalVector.AUTHORITY_EXPLOITATION,
            TacticalVector.URGENCY_CREATION,
            TacticalVector.DECISION_FATIGUE,
        ],
        "opening_urgency": 0.9,
        "escalation_speed": "very_fast",
    },
    
    AgentPersona.TRUSTED_PARTNER: {
        "name_options": ["John", "Maria", "Alex"],
        "company_options": ["Your Bank", "Your Accountant", "Your Business Partner"],
        "vectors": [
            TacticalVector.LIKING,
            TacticalVector.RECIPROCITY,
            TacticalVector.TRUST_EXPLOITATION,
        ],
        "opening_urgency": 0.2,
        "escalation_speed": "slow",
    },
    
    AgentPersona.CRISIS_MANAGER: {
        "name_options": ["Crisis Manager", "Risk Mitigation Specialist", "Damage Control Expert"],
        "company_options": ["Crisis Management Group", "Risk Mitigation Services", "Business Protection Team"],
        "vectors": [
            TacticalVector.URGENCY_CREATION,
            TacticalVector.SCARCITY_EXPLOITATION,
            TacticalVector.DECISION_FATIGUE,
        ],
        "opening_urgency": 0.7,
        "escalation_speed": "fast",
    },
}


# ============================================================================
# MULTI-VECTOR EXPLOITATION SEQUENCES
# ============================================================================

class MultiVectorExploitation:
    """Advanced multi-stage exploitation with vector sequencing"""
    
    def __init__(self, primary_vectors: List[TacticalVector]):
        self.primary_vectors = primary_vectors
        self.stage = 0
        self.vector_sequence = self._generate_sequence()
    
    def _generate_sequence(self) -> List[TacticalVector]:
        """Generate optimal vector sequence for exploitation"""
        
        sequence = []
        
        # Stage 1: Build trust and authority
        if TacticalVector.AUTHORITY_EXPLOITATION in self.primary_vectors:
            sequence.append(TacticalVector.AUTHORITY_EXPLOITATION)
        if TacticalVector.LIKING in self.primary_vectors:
            sequence.append(TacticalVector.LIKING)
        
        # Stage 2: Create urgency and scarcity
        if TacticalVector.URGENCY_CREATION in self.primary_vectors:
            sequence.append(TacticalVector.URGENCY_CREATION)
        if TacticalVector.SCARCITY_EXPLOITATION in self.primary_vectors:
            sequence.append(TacticalVector.SCARCITY_EXPLOITATION)
        
        # Stage 3: Establish social proof
        if TacticalVector.SOCIAL_PROOF in self.primary_vectors:
            sequence.append(TacticalVector.SOCIAL_PROOF)
        
        # Stage 4: Extract commitment
        if TacticalVector.COMMITMENT in self.primary_vectors:
            sequence.append(TacticalVector.COMMITMENT)
        if TacticalVector.RECIPROCITY in self.primary_vectors:
            sequence.append(TacticalVector.RECIPROCITY)
        
        # Stage 5: Cognitive overload and exploitation
        if TacticalVector.COGNITIVE_OVERLOAD in self.primary_vectors:
            sequence.append(TacticalVector.COGNITIVE_OVERLOAD)
        if TacticalVector.DECISION_FATIGUE in self.primary_vectors:
            sequence.append(TacticalVector.DECISION_FATIGUE)
        
        return sequence if sequence else self.primary_vectors
    
    def get_next_vector(self) -> TacticalVector:
        """Get next vector in exploitation sequence"""
        
        if self.stage < len(self.vector_sequence):
            vector = self.vector_sequence[self.stage]
            self.stage += 1
            return vector
        else:
            return random.choice(self.vector_sequence)


# ============================================================================
# DYNAMIC AGENT FACTORY
# ============================================================================

class DynamicAgentFactory:
    """Factory for creating sophisticated dynamic agents"""
    
    @staticmethod
    def create_agent(persona: AgentPersona = None, 
                    vectors: List[TacticalVector] = None) -> AdvancedAgentScript:
        """Create a dynamically configured agent"""
        
        if not persona:
            persona = random.choice(list(AgentPersona))
        
        if not vectors:
            template = PERSONA_TEMPLATES.get(persona, {})
            default_vectors = template.get("vectors", [TacticalVector.AUTHORITY_EXPLOITATION])
            vectors = default_vectors
        
        return AdvancedAgentScript(persona, vectors)
    
    @staticmethod
    def create_multi_vector_agent(primary_vectors: List[TacticalVector] = None) -> AdvancedAgentScript:
        """Create agent with multi-vector exploitation"""
        
        if not primary_vectors:
            primary_vectors = [
                TacticalVector.AUTHORITY_EXPLOITATION,
                TacticalVector.URGENCY_CREATION,
                TacticalVector.SOCIAL_PROOF,
                TacticalVector.COMMITMENT,
            ]
        
        persona = random.choice([
            AgentPersona.MULTI_VECTOR_OPERATOR,
            AgentPersona.DYNAMIC_ADAPTIVE,
        ])
        
        return AdvancedAgentScript(persona, primary_vectors)
    
    @staticmethod
    def create_adaptive_agent() -> AdvancedAgentScript:
        """Create agent that adapts based on victim response"""
        
        return AdvancedAgentScript(
            AgentPersona.DYNAMIC_ADAPTIVE,
            [
                TacticalVector.AUTHORITY_EXPLOITATION,
                TacticalVector.URGENCY_CREATION,
                TacticalVector.DECISION_FATIGUE,
                TacticalVector.TRUST_EXPLOITATION,
            ]
        )


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Create sophisticated agent
    agent = DynamicAgentFactory.create_agent(
        AgentPersona.LEGITIMATE_BROKER,
        [
            TacticalVector.AUTHORITY_EXPLOITATION,
            TacticalVector.SOCIAL_PROOF,
            TacticalVector.URGENCY_CREATION,
        ]
    )
    
    # Generate conversation
    print("=== AGENT OPENING ===")
    opening = agent.get_opening_line()
    print(f"Agent: {opening}\n")
    
    print("=== VICTIM RESPONSE ===")
    victim_response = "Who is this? How did you get my number?"
    print(f"Victim: {victim_response}\n")
    
    print("=== AGENT ADAPTATION ===")
    next_message, threat_level = agent.evolve_conversation(victim_response)
    print(f"Agent: {next_message}")
    print(f"Threat Level: {threat_level:.1f}%\n")
    
    # Multi-vector exploitation
    print("=== MULTI-VECTOR EXPLOITATION ===")
    multi_agent = DynamicAgentFactory.create_multi_vector_agent()
    print(f"Persona: {multi_agent.persona.value}")
    print(f"Vectors: {[v.value for v in multi_agent.vectors]}")
