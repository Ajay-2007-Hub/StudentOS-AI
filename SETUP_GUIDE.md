# 🎓 StudentOS AI - Quick Setup Guide

## Installation (5 minutes)

### Step 1: Clone/Navigate to Project
```bash
cd /workspaces/StudentOS-AI
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
streamlit run app.py
```

**That's it!** The app will open at `http://localhost:8501`

---

## Enable Full AI (Optional - 5 minutes)

### Option A: Windows

1. **Download Ollama** from https://ollama.ai
2. **Install** and restart your computer
3. **Open PowerShell** and run:
   ```powershell
   ollama serve
   ```
4. **Open another PowerShell** and run:
   ```powershell
   ollama pull gemma3:1b
   ```
5. **Keep first PowerShell running**, then in another window:
   ```powershell
   streamlit run app.py
   ```

### Option B: Mac

1. **Download Ollama** from https://ollama.ai
2. **Install and run**
3. **In Terminal 1:**
   ```bash
   ollama serve
   ```
4. **In Terminal 2:**
   ```bash
   ollama pull gemma3:1b
   ```
5. **In Terminal 3:**
   ```bash
   cd /path/to/StudentOS-AI
   streamlit run app.py
   ```

### Option C: Linux

1. **Install Ollama:**
   ```bash
   curl https://ollama.ai/install.sh | sh
   ```
2. **In Terminal 1:**
   ```bash
   ollama serve
   ```
3. **In Terminal 2:**
   ```bash
   ollama pull gemma3:1b
   ```
4. **In Terminal 3:**
   ```bash
   streamlit run app.py
   ```

---

## Test the App

### Try These Questions in AI Assistant:

1. **"hello"**
   - Expected: Friendly greeting

2. **"What are my pending tasks?"**
   - Expected: Lists DBMS, Java, AI tasks, etc.

3. **"Show my subjects"**
   - Expected: Lists all 5 courses

4. **"Summarize my notes"**
   - Expected: Shows DBMS, Java, AI notes

5. **"What should I study today?"**
   - Expected: Today's study schedule

6. **"Give me study tips"**
   - Expected: Helpful advice (works in Basic mode!)

7. **"Explain machine learning"** (Ollama mode only)
   - Expected: Detailed explanation like ChatGPT

---

## Troubleshooting

### Problem: Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

### Problem: "command not found: ollama"
- Make sure you installed Ollama and restarted your computer
- Or download from https://ollama.ai

### Problem: "could not connect to Ollama"
- Make sure you ran `ollama serve` before starting the app

### Problem: Slow responses
- Use a faster model: `ollama pull mistral` instead of gemma3:1b
- Or just use basic mode (works great!)

---

## Customize Your Profile

Edit `data/profile.json`:
```json
{
  "name": "Your Name",
  "department": "Your Department",
  "semester": 5,
  "goal": "Your Career Goal"
}
```

Edit `data/subjects.json` to add your courses
Edit `data/tasks.json` to add your assignments
Edit `data/notes.json` to add your study notes
Edit `data/study_plan.json` to set your study schedule

---

## What's Included

✅ **AI Assistant** - Chat interface (with or without Ollama)
✅ **Task Manager** - Track assignments
✅ **Notes** - Organize study materials
✅ **Study Planner** - Plan learning sessions
✅ **Cursor Effects** - Cool animations (optional)
✅ **Fallback Mode** - Works without Ollama
✅ **Private Data** - All files stored locally

---

## Tips

- Clear chat anytime - it won't delete your data
- All data is in `data/` folder - fully editable
- Enable cursor effects in sidebar for cool animations
- Use Basic Mode while Ollama downloads
- Share with classmates!

---

## Commands Cheat Sheet

```bash
# Basic mode
streamlit run app.py

# Custom port
streamlit run app.py --server.port 8502

# Verbose output
streamlit run app.py --logger.level=debug

# Install Ollama (Linux)
curl https://ollama.ai/install.sh | sh

# Download model
ollama pull gemma3:1b

# Start Ollama server
ollama serve

# List available models
ollama list

# Change model (optional)
export OLLAMA_MODEL=mistral
streamlit run app.py
```

---

**Enjoy StudentOS AI! Happy learning! 🚀**
