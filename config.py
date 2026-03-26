import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///fraudlab.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Twilio
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')

    # LLM
    LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'ollama')  # 'openai' or 'ollama'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'llama2')

    # Detection
    ENABLE_LLM_DETECTION = os.environ.get('ENABLE_LLM_DETECTION', 'True').lower() == 'true'

    # Dashboard Theming (prompt-configurable)
    DASHBOARD_PRIMARY_COLOR = os.environ.get('DASHBOARD_PRIMARY_COLOR', '#0d6efd')
    DASHBOARD_ACCENT_COLOR  = os.environ.get('DASHBOARD_ACCENT_COLOR', '#198754')
    DASHBOARD_BG_COLOR      = os.environ.get('DASHBOARD_BG_COLOR', '#121212')
    DASHBOARD_CARD_COLOR    = os.environ.get('DASHBOARD_CARD_COLOR', '#1e1e2e')
    DASHBOARD_TEXT_COLOR    = os.environ.get('DASHBOARD_TEXT_COLOR', '#e0e0e0')
    DASHBOARD_TITLE         = os.environ.get('DASHBOARD_TITLE', 'FraudSim Lab')
    DASHBOARD_LOGO_TEXT     = os.environ.get('DASHBOARD_LOGO_TEXT', 'FSL')

    # Tunnel
    TUNNEL_URL = os.environ.get('TUNNEL_URL', '')
    APP_PORT   = int(os.environ.get('APP_PORT', 8000))
