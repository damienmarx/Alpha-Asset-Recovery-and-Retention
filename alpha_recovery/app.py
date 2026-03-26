"""
Alpha Asset Recovery and Retention - Companion Website
from flask import redirect
Provides information about fraud prevention and recovery services
"""
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-prod')

@app.route('/')
def index():
    """Home page with services and information"""
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    data = request.get_json()
    
    # Validate input
    if not all(k in data for k in ['name', 'email', 'message']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Here you would typically save to database or send email
    # For now, just return success
    return jsonify({
        'status': 'success',
        'message': 'Thank you for your message. We will contact you soon.'
    })

@app.route('/fraudsim')
def fraudsim_redirect():
    """Redirect to FraudSim Lab"""
    return redirect('http://localhost:8000')

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
