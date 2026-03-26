"""
Twilio service — handles outbound calls and TwiML generation.
Falls back gracefully when Twilio credentials are not configured.
"""
import os
from config import Config

_client = None

def get_client():
    global _client
    if _client is None and Config.TWILIO_ACCOUNT_SID and Config.TWILIO_AUTH_TOKEN:
        try:
            from twilio.rest import Client
            _client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        except Exception as e:
            print(f"[Twilio] Client init failed: {e}")
    return _client


def make_outbound_call(to_number: str, from_number: str, webhook_url: str) -> str:
    """Initiate an outbound call via Twilio; returns call SID or a mock SID."""
    client = get_client()
    if client:
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url=webhook_url,
            status_callback=webhook_url.replace('/voice', '/voice/status'),
            method='POST'
        )
        return call.sid
    # Demo / no-Twilio mode
    import uuid
    return f"MOCK-{uuid.uuid4().hex[:16].upper()}"


def generate_twiml_for_scammer_response(response_text: str, gather: bool = True) -> str:
    """Generate TwiML that speaks the scammer's text and optionally gathers speech."""
    try:
        from twilio.twiml.voice_response import VoiceResponse, Gather
        resp = VoiceResponse()
        resp.say(response_text, voice='alice', language='en-US')
        if gather:
            g = resp.gather(
                input='speech',
                speech_timeout='auto',
                speech_model='phone_call',
                action='/voice/gather',
                method='POST'
            )
            g.say("Please respond after the beep.")
        else:
            resp.hangup()
        return str(resp)
    except ImportError:
        return f'<?xml version="1.0" encoding="UTF-8"?><Response><Say>{response_text}</Say></Response>'


def get_recording_url(call_sid: str):
    """Fetch recording URL from Twilio (if any)."""
    client = get_client()
    if not client:
        return None
    try:
        recordings = client.recordings.list(call_sid=call_sid)
        if recordings:
            return f"https://api.twilio.com{recordings[0].uri.replace('.json', '.mp3')}"
    except Exception:
        pass
    return None
