"""
PPP Fraud Simulation Lab - Main Flask Application
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import threading
import uuid

from config import Config
from models import db, User, Call, ConversationTurn, Alert, Comment, DashboardSettings
from forms import LoginForm, RegisterForm, NewCallForm, DashboardSettingsForm
from twilio_service import make_outbound_call, generate_twiml_for_scammer_response, get_recording_url
from llm_service import get_llm_response
from detection import rule_based_detection, llm_based_detection, calculate_overall_risk_score

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============================================================================
# AUTH ROUTES
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            form.username.errors.append('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(username=form.username.data).first()
        if existing:
            form.username.errors.append('Username already taken')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ============================================================================
# DASHBOARD & SETTINGS
# ============================================================================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing recent calls and alerts."""
    calls = Call.query.order_by(Call.started_at.desc()).limit(50).all()
    alerts = Alert.query.order_by(Alert.detected_at.desc()).limit(15).all()
    
    # Get user's theme settings
    settings = DashboardSettings.query.filter_by(user_id=current_user.id).first()
    if not settings:
        settings = DashboardSettings(user_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    return render_template('dashboard.html', calls=calls, alerts=alerts, settings=settings)


@app.route('/dashboard/settings', methods=['GET', 'POST'])
@login_required
def dashboard_settings():
    """Customize dashboard colors and branding."""
    settings = DashboardSettings.query.filter_by(user_id=current_user.id).first()
    if not settings:
        settings = DashboardSettings(user_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    form = DashboardSettingsForm()
    if form.validate_on_submit():
        settings.dashboard_title = form.dashboard_title.data or settings.dashboard_title
        settings.logo_text = form.logo_text.data or settings.logo_text
        settings.primary_color = form.primary_color.data or settings.primary_color
        settings.accent_color = form.accent_color.data or settings.accent_color
        settings.bg_color = form.bg_color.data or settings.bg_color
        settings.card_color = form.card_color.data or settings.card_color
        settings.text_color = form.text_color.data or settings.text_color
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    # Pre-populate form
    form.dashboard_title.data = settings.dashboard_title
    form.logo_text.data = settings.logo_text
    form.primary_color.data = settings.primary_color
    form.accent_color.data = settings.accent_color
    form.bg_color.data = settings.bg_color
    form.card_color.data = settings.card_color
    form.text_color.data = settings.text_color
    
    return render_template('dashboard_settings.html', form=form, settings=settings)


# ============================================================================
# CALL MANAGEMENT
# ============================================================================

@app.route('/new_call', methods=['GET', 'POST'])
@login_required
def new_call():
    """Initiate a new outbound call."""
    form = NewCallForm()
    if form.validate_on_submit():
        target = form.target_number.data
        persona = form.scammer_persona.data or None
        
        # Generate webhook URL
        webhook_url = url_for('voice_webhook', _external=True)
        if Config.TUNNEL_URL:
            webhook_url = webhook_url.replace(request.host_url.rstrip('/'), Config.TUNNEL_URL.rstrip('/'))
        
        # Make the call
        call_sid = make_outbound_call(target, Config.TWILIO_PHONE_NUMBER, webhook_url)
        
        # Create call record
        call = Call(
            call_sid=call_sid,
            direction='outbound',
            from_number=Config.TWILIO_PHONE_NUMBER,
            to_number=target,
            status='initiated',
            persona_used=persona
        )
        db.session.add(call)
        db.session.commit()
        
        return redirect(url_for('call_detail', call_id=call.id))
    
    return render_template('new_call.html', form=form)


@app.route('/call/<int:call_id>')
@login_required
def call_detail(call_id):
    """View detailed call transcript, alerts, and comments."""
    call = Call.query.get_or_404(call_id)
    turns = ConversationTurn.query.filter_by(call_id=call.id).order_by(ConversationTurn.timestamp).all()
    alerts = Alert.query.filter_by(call_id=call.id).order_by(Alert.detected_at.desc()).all()
    comments = Comment.query.filter_by(call_id=call.id).order_by(Comment.created_at.desc()).all()
    
    # Get user's theme settings
    settings = DashboardSettings.query.filter_by(user_id=current_user.id).first()
    
    return render_template('call_detail.html', call=call, turns=turns, alerts=alerts, 
                          comments=comments, settings=settings)


@app.route('/calls')
@login_required
def calls_list():
    """List all calls with filtering."""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', None)
    
    query = Call.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    calls = query.order_by(Call.started_at.desc()).paginate(page=page, per_page=20)
    return render_template('calls_list.html', calls=calls)


# ============================================================================
# TWILIO WEBHOOKS
# ============================================================================

@app.route('/voice', methods=['POST'])
def voice_webhook():
    """Twilio webhook: call initiated."""
    call_sid = request.values.get('CallSid')
    from_number = request.values.get('From')
    to_number = request.values.get('To')
    direction = 'inbound' if from_number != Config.TWILIO_PHONE_NUMBER else 'outbound'
    
    # Find or create call record
    call = Call.query.filter_by(call_sid=call_sid).first()
    if not call:
        call = Call(
            call_sid=call_sid,
            direction=direction,
            from_number=from_number,
            to_number=to_number,
            status='in-progress'
        )
        db.session.add(call)
        db.session.commit()
    else:
        call.status = 'in-progress'
        db.session.commit()
    
    # Get scammer's opening line
    history = [{"role": "assistant", "content": "Hello, I'm calling about your PPP loan forgiveness application."}]
    response_text = get_llm_response(history, call.persona_used)
    
    # Store the turn
    turn = ConversationTurn(call_id=call.id, speaker='scammer', text=response_text)
    db.session.add(turn)
    db.session.commit()
    
    # Broadcast via WebSocket
    socketio.emit('new_turn', {
        'call_id': call.id,
        'speaker': 'scammer',
        'text': response_text,
        'timestamp': turn.timestamp.isoformat()
    }, room=f'call_{call.id}')
    
    # Generate TwiML
    twiml = generate_twiml_for_scammer_response(response_text, gather=True)
    return twiml, 200, {'Content-Type': 'text/xml'}


@app.route('/voice/gather', methods=['POST'])
def voice_gather():
    """Twilio webhook: user speech received."""
    call_sid = request.values.get('CallSid')
    speech_result = request.values.get('SpeechResult', '')
    
    call = Call.query.filter_by(call_sid=call_sid).first()
    if not call:
        return "Error", 400
    
    # Store victim's turn
    user_turn = ConversationTurn(call_id=call.id, speaker='victim', text=speech_result)
    db.session.add(user_turn)
    db.session.commit()
    
    socketio.emit('new_turn', {
        'call_id': call.id,
        'speaker': 'victim',
        'text': speech_result,
        'timestamp': user_turn.timestamp.isoformat()
    }, room=f'call_{call.id}')
    
    # Run detection on full transcript
    all_turns = ConversationTurn.query.filter_by(call_id=call.id).order_by(ConversationTurn.timestamp).all()
    transcript = "\n".join([f"{t.speaker}: {t.text}" for t in all_turns])
    
    # Rule-based detection
    rule_alerts = rule_based_detection(transcript)
    for alert_data in rule_alerts:
        alert = Alert(
            call_id=call.id,
            severity=alert_data['severity'],
            description=alert_data['description']
        )
        db.session.add(alert)
        db.session.commit()
        socketio.emit('new_alert', {
            'call_id': call.id,
            'alert': alert.to_dict()
        }, room=f'call_{call.id}')
    
    # LLM detection (async)
    if Config.ENABLE_LLM_DETECTION:
        def run_llm_detection():
            try:
                llm_result = llm_based_detection(transcript)
                severity = llm_result.get('severity', 'medium')
                alert = Alert(
                    call_id=call.id,
                    severity=severity,
                    description=f"LLM Analysis: {llm_result.get('explanation', 'Analysis complete')}"
                )
                db.session.add(alert)
                db.session.commit()
                socketio.emit('new_alert', {
                    'call_id': call.id,
                    'alert': alert.to_dict()
                }, room=f'call_{call.id}')
            except Exception as e:
                print(f"[LLM Detection] Error: {e}")
        
        threading.Thread(target=run_llm_detection, daemon=True).start()
    
    # Update call risk score
    call.risk_score = calculate_overall_risk_score(transcript, rule_alerts)
    db.session.commit()
    
    # Get scammer's next response
    conversation_history = [
        {"role": "assistant" if t.speaker == 'scammer' else "user", "content": t.text}
        for t in all_turns
    ]
    next_response = get_llm_response(conversation_history, call.persona_used)
    
    # Store scammer's response
    scammer_turn = ConversationTurn(call_id=call.id, speaker='scammer', text=next_response)
    db.session.add(scammer_turn)
    db.session.commit()
    
    socketio.emit('new_turn', {
        'call_id': call.id,
        'speaker': 'scammer',
        'text': next_response,
        'timestamp': scammer_turn.timestamp.isoformat()
    }, room=f'call_{call.id}')
    
    # Continue call
    twiml = generate_twiml_for_scammer_response(next_response, gather=True)
    return twiml, 200, {'Content-Type': 'text/xml'}


@app.route('/voice/status', methods=['POST'])
def voice_status():
    """Twilio webhook: call status update."""
    call_sid = request.values.get('CallSid')
    call_status = request.values.get('CallStatus')
    
    call = Call.query.filter_by(call_sid=call_sid).first()
    if call:
        call.status = call_status
        if call_status in ['completed', 'failed', 'busy', 'no-answer']:
            call.ended_at = datetime.utcnow()
        db.session.commit()
        
        socketio.emit('call_status_update', {
            'call_id': call.id,
            'status': call_status
        }, room=f'call_{call.id}')
    
    return "OK", 200


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/comment', methods=['POST'])
@login_required
def add_comment():
    """Add a comment to a call."""
    data = request.get_json()
    call_id = data.get('call_id')
    text = data.get('text')
    
    if not call_id or not text:
        return jsonify({'error': 'Missing fields'}), 400
    
    comment = Comment(call_id=call_id, user_id=current_user.id, text=text)
    db.session.add(comment)
    db.session.commit()
    
    socketio.emit('new_comment', {
        'call_id': call_id,
        'comment': comment.to_dict()
    }, room=f'call_{call_id}')
    
    return jsonify({'status': 'ok', 'comment': comment.to_dict()})


@app.route('/api/calls', methods=['GET'])
@login_required
def api_calls():
    """Get calls as JSON."""
    calls = Call.query.order_by(Call.started_at.desc()).limit(50).all()
    return jsonify([c.to_dict() for c in calls])


@app.route('/api/call/<int:call_id>', methods=['GET'])
@login_required
def api_call_detail(call_id):
    """Get call details as JSON."""
    call = Call.query.get_or_404(call_id)
    turns = ConversationTurn.query.filter_by(call_id=call.id).all()
    alerts = Alert.query.filter_by(call_id=call.id).all()
    
    return jsonify({
        'call': call.to_dict(),
        'turns': [t.to_dict() for t in turns],
        'alerts': [a.to_dict() for a in alerts]
    })


# ============================================================================
# WEBSOCKET EVENTS
# ============================================================================

@socketio.on('connect')
def handle_connect():
    """Client connected."""
    emit('connected', {'data': 'Connected to FraudSim Lab'})


@socketio.on('join_call')
def on_join_call(data):
    """Join a call's real-time room."""
    call_id = data.get('call_id')
    if call_id:
        join_room(f'call_{call_id}')
        emit('joined_call', {'call_id': call_id})


@socketio.on('leave_call')
def on_leave_call(data):
    """Leave a call's real-time room."""
    call_id = data.get('call_id')
    if call_id:
        leave_room(f'call_{call_id}')


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# ============================================================================
# CLI & INITIALIZATION
# ============================================================================

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Call': Call}


def init_db():
    """Initialize database and create default users."""
    with app.app_context():
        db.create_all()
        
        # Create default admin if none exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@fraudsim.local',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("[Init] Created default admin user: admin / admin123")


if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=Config.APP_PORT, debug=True)
