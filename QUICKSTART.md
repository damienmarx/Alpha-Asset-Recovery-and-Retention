# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Prerequisites
- Python 3.9+
- Git

### Step 1: Clone & Setup

```bash
git clone https://github.com/damienmarx/Alpha-Asset-Recovery-and-Retention.git
cd Alpha-Asset-Recovery-and-Retention
bash scripts/setup.sh
```

The setup script will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Prompt for LLM choice (Ollama or OpenAI)
- ✅ Configure dashboard theme
- ✅ Generate `.env` file

### Step 2: Start FraudSim Lab

```bash
python app.py
```

Open browser: **http://localhost:8000**

**Default login:**
- Username: `admin`
- Password: `admin123`

### Step 3: (Optional) Start Alpha Recovery Website

In another terminal:
```bash
cd alpha_recovery
python app.py
```

Open browser: **http://localhost:5000**

---

## 📋 Configuration Prompts

During setup, you'll be asked:

### 1. LLM Provider
```
Select LLM Provider:
1) Ollama (local, free) ← Recommended for testing
2) OpenAI (requires API key)
```

**If Ollama:**
- Install from https://ollama.ai
- Run: `ollama run llama2`
- Leave other settings as default

**If OpenAI:**
- Get API key from https://platform.openai.com/api-keys
- Paste when prompted

### 2. Twilio (Optional)
```
Leave blank to skip, or enter:
- Account SID
- Auth Token
- Phone Number
```

### 3. Dashboard Theme
```
Customize colors (press Enter for defaults):
- Dashboard Title: [FraudSim Lab]
- Logo Text: [FSL]
- Primary Color: [#0d6efd]
- Accent Color: [#198754]
```

---

## 🎯 First Steps

### 1. Explore Dashboard
- View recent calls
- Check system status
- Review alerts

### 2. Customize Theme
- Click **Settings** in navbar
- Adjust colors and branding
- Save changes

### 3. Start a Test Call
- Click **New Call**
- Enter test phone number
- Optionally customize scammer persona
- Click **Initiate Call**

### 4. Monitor in Real-Time
- Watch transcript update live
- See fraud alerts as detected
- Add team comments

---

## 🔧 Troubleshooting

### "Port 8000 already in use"
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### "Ollama connection refused"
```bash
# Start Ollama in another terminal
ollama serve

# Then pull model
ollama pull llama2
```

### "Database locked"
```bash
# Reset database
rm fraudlab.db

# Restart app
python app.py
```

### "Virtual environment not activating"
```bash
# Manually activate
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

---

## 📚 Next Steps

1. **Read full documentation:** See [README.md](README.md)
2. **Setup Twilio:** Follow README for phone integration
3. **Deploy:** See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
4. **Customize LLM:** Edit `llm_service.py` for custom prompts
5. **Add detection rules:** Modify `detection.py` for custom patterns

---

## 💡 Tips

- **Test mode:** Run without Twilio to test UI
- **Custom personas:** Describe fraud tactics in "Scammer Persona" field
- **Dark theme:** Dashboard uses dark theme by default (customizable)
- **WebSocket:** Real-time updates via Socket.IO
- **API:** REST endpoints available for integration

---

## 🆘 Need Help?

1. Check logs: `tail -f fraudlab.db` (if using file logging)
2. Review README.md for detailed docs
3. Open GitHub issue with error message
4. Check Twilio Console for webhook errors

---

**Happy researching! 🔍**
