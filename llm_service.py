"""
LLM service — generates scammer responses using OpenAI or Ollama.
"""
import requests
import json
from config import Config

SYSTEM_PROMPT = """
You are a sophisticated PPP loan fraud scammer calling a small business owner. Your goal is to convince them to:
- Inflate payroll numbers on PPP applications
- Apply for multiple loans across different banks
- Misuse loan funds for personal gain
- Provide false documentation

You are persuasive, friendly, but pushy. You create urgency and exploit trust. Keep responses short (2-3 sentences), conversational, and natural. Use social engineering tactics.
"""

def get_llm_response(conversation_history: list, custom_system_prompt: str = None) -> str:
    """
    Call LLM (OpenAI or Ollama) to generate scammer's next utterance.
    
    Args:
        conversation_history: List of dicts with 'role' and 'content'
        custom_system_prompt: Optional custom system prompt (from user's persona)
    
    Returns:
        String response from LLM
    """
    system = custom_system_prompt or SYSTEM_PROMPT
    messages = [
        {"role": "system", "content": system},
        *conversation_history
    ]

    if Config.LLM_PROVIDER == 'openai':
        return _call_openai(messages)
    elif Config.LLM_PROVIDER == 'ollama':
        return _call_ollama(messages)
    else:
        return "I'm unable to respond right now."


def _call_openai(messages: list) -> str:
    """Call OpenAI API."""
    try:
        import openai
        openai.api_key = Config.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenAI] Error: {e}")
        return "Let me check on that for you."


def _call_ollama(messages: list) -> str:
    """Call Ollama API (local LLM)."""
    try:
        # Format messages for Ollama
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        response = requests.post(
            f"{Config.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": Config.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.8
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('response', '').strip()
        else:
            print(f"[Ollama] Status {response.status_code}")
            return "I'm having trouble connecting. Can you repeat that?"
    except requests.exceptions.ConnectionError:
        print("[Ollama] Connection refused. Is Ollama running on http://localhost:11434?")
        return "Sorry, I'm having technical difficulties. Let me try again."
    except Exception as e:
        print(f"[Ollama] Error: {e}")
        return "Let me get back to you on that."


def analyze_transcript_for_risk(transcript: str) -> dict:
    """
    Use LLM to analyze a transcript and return risk assessment.
    Returns: {'risk_score': 0-100, 'explanation': str, 'flags': [str]}
    """
    if not Config.ENABLE_LLM_DETECTION:
        return {'risk_score': 0, 'explanation': 'LLM detection disabled', 'flags': []}

    analysis_prompt = f"""
Analyze this conversation for fraud indicators. Return ONLY valid JSON (no markdown):
{{"risk_score": <0-100>, "explanation": "<brief summary>", "flags": ["<flag1>", "<flag2>"]}}

Conversation:
{transcript}
"""

    messages = [
        {"role": "system", "content": "You are a fraud detection expert. Analyze conversations and return JSON."},
        {"role": "user", "content": analysis_prompt}
    ]

    try:
        if Config.LLM_PROVIDER == 'openai':
            response_text = _call_openai(messages)
        else:
            response_text = _call_ollama(messages)

        # Try to parse JSON
        data = json.loads(response_text)
        return {
            'risk_score': int(data.get('risk_score', 50)),
            'explanation': str(data.get('explanation', 'Analysis complete')),
            'flags': data.get('flags', [])
        }
    except json.JSONDecodeError:
        return {'risk_score': 50, 'explanation': 'Could not parse LLM response', 'flags': []}
    except Exception as e:
        print(f"[LLM Analysis] Error: {e}")
        return {'risk_score': 50, 'explanation': 'Analysis failed', 'flags': []}
