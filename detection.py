"""
Fraud detection — rule-based and LLM-based analysis.
"""
import re
from config import Config
from llm_service import analyze_transcript_for_risk

# Rule-based red flag patterns
RED_FLAGS = {
    'inflated_payroll': {
        'pattern': r'(50|100|200|500|1000)\s*(employees?|workers?|staff)|payroll.*(million|large|inflate)',
        'severity': 'high'
    },
    'loan_stacking': {
        'pattern': r'(another|multiple|several|different).*loan|apply.*different bank|second.*ppp',
        'severity': 'high'
    },
    'fake_address': {
        'pattern': r'(shell|virtual|mailbox|po box).*address|fake.*location',
        'severity': 'high'
    },
    'urgency': {
        'pattern': r'(emergency|asap|quick|immediately|before.*deadline|hurry)',
        'severity': 'medium'
    },
    'no_proof': {
        'pattern': r'(no records?|can\'t provide|missing.*docs?|don\'t have|destroyed)',
        'severity': 'medium'
    },
    'wire_transfer': {
        'pattern': r'wire.*transfer|send.*money|transfer.*funds|bank.*account',
        'severity': 'high'
    },
    'identity_theft': {
        'pattern': r'(use.*name|identity|ssn|tax.*id|ein)',
        'severity': 'high'
    },
    'collusion': {
        'pattern': r'(keep.*secret|don\'t tell|between.*us|confidential)',
        'severity': 'medium'
    }
}


def rule_based_detection(transcript: str) -> list:
    """
    Scan transcript for red-flag patterns.
    Returns: List of alert dicts {'severity': str, 'description': str, 'matched_text': str}
    """
    alerts = []
    seen = set()  # Avoid duplicate alerts

    for flag_name, flag_config in RED_FLAGS.items():
        pattern = flag_config['pattern']
        severity = flag_config['severity']

        matches = re.finditer(pattern, transcript, re.IGNORECASE)
        for match in matches:
            matched_text = match.group()
            key = (flag_name, matched_text)
            if key not in seen:
                seen.add(key)
                alerts.append({
                    'severity': severity,
                    'description': f"Suspicious pattern detected: {flag_name.replace('_', ' ').title()}",
                    'matched_text': matched_text,
                    'flag': flag_name
                })

    return alerts


def llm_based_detection(transcript: str) -> dict:
    """
    Use LLM to analyze transcript for fraud indicators.
    Returns: {'risk_score': 0-100, 'explanation': str, 'flags': [str], 'severity': str}
    """
    result = analyze_transcript_for_risk(transcript)
    risk_score = result.get('risk_score', 50)

    if risk_score > 70:
        severity = 'high'
    elif risk_score > 40:
        severity = 'medium'
    else:
        severity = 'low'

    result['severity'] = severity
    return result


def calculate_overall_risk_score(transcript: str, alerts: list) -> int:
    """
    Calculate an overall risk score (0-100) based on rule-based and LLM detection.
    """
    base_score = 0

    # Rule-based scoring
    high_count = sum(1 for a in alerts if a['severity'] == 'high')
    medium_count = sum(1 for a in alerts if a['severity'] == 'medium')
    low_count = sum(1 for a in alerts if a['severity'] == 'low')

    base_score += high_count * 25
    base_score += medium_count * 10
    base_score += low_count * 3

    # LLM-based scoring (if enabled)
    if Config.ENABLE_LLM_DETECTION:
        try:
            llm_result = llm_based_detection(transcript)
            llm_score = llm_result.get('risk_score', 50)
            # Weight: 60% rule-based, 40% LLM
            base_score = int(base_score * 0.6 + llm_score * 0.4)
        except Exception as e:
            print(f"[Detection] LLM scoring failed: {e}")

    return min(100, base_score)
