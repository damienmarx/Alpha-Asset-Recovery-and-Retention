# Deployment Guide

## FraudSim Lab + Alpha Asset Recovery Platform

This repository contains two integrated applications:

1. **FraudSim Lab** (Port 8000) — PPP Fraud Simulation & Detection Platform
2. **Alpha Asset Recovery Website** (Port 5000) — Information & Marketing Site

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/damienmarx/Alpha-Asset-Recovery-and-Retention.git
cd Alpha-Asset-Recovery-and-Retention
```

### 2. Run Automated Setup

```bash
bash scripts/setup.sh
```

This will:
- Create virtual environment
- Install dependencies
- Prompt for configuration
- Generate `.env` file

### 3. Start Both Applications

**Terminal 1 - FraudSim Lab:**
```bash
source venv/bin/activate
python app.py
# Runs on http://localhost:8000
```

**Terminal 2 - Alpha Recovery Website:**
```bash
source venv/bin/activate
cd alpha_recovery
python app.py
# Runs on http://localhost:5000
```

## Configuration

### FraudSim Lab (.env)

```env
# LLM Provider
LLM_PROVIDER=ollama          # or 'openai'
OPENAI_API_KEY=sk-...        # if using OpenAI

# Twilio (optional)
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1234567890

# Dashboard Theme
DASHBOARD_PRIMARY_COLOR=#0d6efd
DASHBOARD_ACCENT_COLOR=#198754
```

### Alpha Recovery Website (alpha_recovery/.env)

```env
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
CONTACT_EMAIL=info@alphaassetrecovery.com
```

## Tunnel Setup (Optional)

To expose FraudSim Lab to the internet for Twilio webhooks:

```bash
bash scripts/setup_tunnel.sh
```

This will display a public URL like: `https://xxxx.trycloudflare.com`

Configure in Twilio Console:
- Voice webhook: `https://xxxx.trycloudflare.com/voice`
- Status callback: `https://xxxx.trycloudflare.com/voice/status`

## Production Deployment

### Using Gunicorn + Nginx

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Start FraudSim Lab:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. **Start Alpha Recovery:**
   ```bash
   cd alpha_recovery
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

4. **Configure Nginx** as reverse proxy (see nginx.conf example below)

### Nginx Configuration

```nginx
upstream fraudsim {
    server 127.0.0.1:8000;
}

upstream alpha_recovery {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    # FraudSim Lab
    location /fraudsim {
        proxy_pass http://fraudsim;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Alpha Recovery Website
    location / {
        proxy_pass http://alpha_recovery;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
   ```

2. **Build and run:**
   ```bash
   docker build -t fraudsim-lab .
   docker run -p 8000:8000 --env-file .env fraudsim-lab
   ```

## Database Setup

### Initialize Database

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Backup Database

```bash
cp fraudlab.db fraudlab.db.backup
```

## Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS (SSL/TLS certificate)
- [ ] Restrict database access
- [ ] Enable firewall rules
- [ ] Use strong passwords
- [ ] Regularly update dependencies
- [ ] Monitor logs for suspicious activity
- [ ] Implement rate limiting
- [ ] Enable CORS only for trusted domains

## Monitoring

### Check Application Status

```bash
# Check if FraudSim Lab is running
curl http://localhost:8000/

# Check if Alpha Recovery is running
curl http://localhost:5000/
```

### View Logs

```bash
# FraudSim Lab logs
tail -f fraudsim.log

# Nginx logs
tail -f /var/log/nginx/error.log
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database Locked

```bash
# Reset database
rm fraudlab.db
python app.py  # Will recreate
```

### LLM Not Responding

- Verify Ollama is running: `ollama serve`
- Check API key if using OpenAI
- Review logs for errors

## Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review logs for error messages
3. Open GitHub issue with details
4. Contact support team

## License

MIT License - See LICENSE file
