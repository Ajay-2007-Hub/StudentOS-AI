# 🎓 StudentOS AI

A beginner-friendly mini ChatGPT product for students. StudentOS AI is a Streamlit-based AI assistant that helps students manage their academic life with intelligent assistance powered by optional local AI.

## ✨ Features

- **🤖 AI Assistant** - ChatGPT-like chat interface for students
- **💬 Local AI with Ollama** - Private, fast, runs on your computer
- **📚 Basic Fallback Mode** - Works without Ollama (rule-based responses)
- **✅ Task Manager** - Track assignments and deadlines
- **📝 Study Notes** - Organize knowledge by subject
- **📅 Study Planner** - Plan your learning sessions
- **💾 JSON-based Memory** - Data stored locally, fully private
- **🎨 Modern UI** - Clean, intuitive design with animations

## 🚀 Quick Start

### Minimum Setup (No AI)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

**The app will open in your browser at:** `http://localhost:8501`

### Full Setup (With Local AI - Recommended)

#### Step 1: Install Ollama
Download and install Ollama from: https://ollama.ai

#### Step 2: Run Ollama Server
Open a terminal and run:
```bash
ollama serve
```

#### Step 3: Download AI Model
Open another terminal and run:
```bash
ollama pull gemma3:1b
```

#### Step 4: Run StudentOS AI
Open a third terminal and run:
```bash
streamlit run app.py
```

**The app will now use the local AI model automatically!**

## 📖 How to Use

### Home Page
- Overview of all features
- Quick navigation buttons
- Tips to get started

### AI Assistant Page
- Chat with StudentOS AI about anything
- Ask about your studies, tasks, notes, deadlines, or career
- Clear chat history anytime

### Notes Page
- View your study notes organized by subject
- Add and manage notes for each topic

### Tasks Page
- Track pending and completed tasks
- See deadlines and priorities
- Manage your workload

### Study Planner Page
- Plan study sessions for exams
- Organize learning goals
- Track progress

### About Page
- Learn about the project
- View technologies used
- Instructions for setup

## ⚙️ Configuration

### Change Port
If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

### Change AI Model
Set the `OLLAMA_MODEL` environment variable:

**Linux/Mac:**
```bash
export OLLAMA_MODEL=mistral
streamlit run app.py
```

**Windows:**
```bash
set OLLAMA_MODEL=mistral
streamlit run app.py
```

Available models: `gemma3:1b`, `mistral`, `llama2`, etc.
See more at: https://ollama.ai/library

## 🎯 Student Profile

The app comes with sample data for a B.Tech student:

- **Name:** Ajay
- **Department:** Artificial Intelligence and Data Science
- **Semester:** 3
- **Goal:** Build strong projects, improve coding, prepare for internships

### Sample Subjects
- Database Management Systems
- Advanced Java Programming
- Artificial Intelligence and Decision Making
- Discrete Mathematics
- Computer Organization and Architecture

### Sample Tasks
- Complete DBMS assignment
- Revise Java OOP concepts
- Prepare AI notes
- Update GitHub project
- Practice coding problems

You can edit the sample data in `data/` folder (JSON files).

## 📂 Project Structure

```
StudentOS-AI/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── database/
│   ├── __init__.py
│   └── db.py            # Database initialization
├── modules/
│   ├── dashboard.py      # Dashboard module
│   ├── task_manager.py   # Task management
│   ├── study_planner.py  # Study planning
│   ├── learning_log.py   # Notes/learning log
│   ├── skill_gap.py      # Skill gap analyzer
│   └── document_chat.py  # PDF chat
├── data/                # Student data (JSON)
│   ├── profile.json     # Student profile
│   ├── subjects.json    # Subjects and courses
│   ├── tasks.json       # Tasks and assignments
│   ├── notes.json       # Study notes
│   └── study_plan.json  # Study plans
└── assets/
    └── styles.css       # Custom styles
```

## 🛠️ Technologies

- **Python 3.8+** - Programming language
- **Streamlit** - Web app framework
- **Ollama** - Local AI inference
- **JSON** - Data storage
- **CSS** - Styling and animations

## ❓ Common Issues & Solutions

### Issue: `bash: ollama: command not found`
**Solution:** Install Ollama from https://ollama.ai

### Issue: `could not connect to Ollama server`
**Solution:** Make sure to run `ollama serve` in a separate terminal before starting the app

### Issue: `Port 8501 is already in use`
**Solution:** Use a different port with `streamlit run app.py --server.port 8502`

### Issue: `OLLAMA_MODEL command not found`
**Solution:** Use `export OLLAMA_MODEL=gemma3:1b` (Linux/Mac) or `set OLLAMA_MODEL=gemma3:1b` (Windows)

### Issue: Model is not downloaded
**Solution:** Run `ollama pull gemma3:1b` to download the model

### Issue: The app is slow
**Solution:** 
- Use a smaller model like `gemma3:1b` or `mistral`
- Make sure you have enough RAM (at least 4GB)
- Close other applications

## 🧪 Testing the AI

Try asking these questions in the AI Assistant:

1. **"hello"** - Should greet you
2. **"What are my pending tasks?"** - Shows pending tasks
3. **"Show my subjects"** - Lists your courses
4. **"Summarize my notes"** - Shows your notes
5. **"What should I study today?"** - Shows today's plan
6. **"Give me study advice"** - Provides tips
7. **"Explain DBMS simply"** - (Ollama mode) Detailed explanation

## 📝 Features Explained

### AI Modes

**Full AI Mode (Ollama Active)**
- Answers any question with detailed responses
- Understands context from your student data
- Provides explanations like ChatGPT

**Basic Mode (Ollama Inactive)**
- Answers common student questions
- Uses rule-based responses
- Reads your task/notes data
- No internet required

Both modes are beginner-friendly and don't crash!

### Cursor Effects
- Enable/disable glowing cursor trail
- Click ripple animation
- Doesn't block any buttons or input fields
- Optional - toggle in sidebar

### Auto-Save Features
- All chat messages are saved during session
- Student data auto-saves to JSON files
- Data never leaves your computer
- No cloud, no tracking, fully private

## 🎓 Use Cases

1. **Quick AI Help**
   - Ask AI about difficult topics
   - Get study suggestions
   - Learn in your own pace

2. **Task Management**
   - Keep track of all assignments
   - Never miss deadlines
   - Prioritize work

3. **Note Organization**
   - Organize notes by subject
   - Quick reference during study
   - Review and summarize anytime

4. **Study Planning**
   - Plan study sessions
   - Track learning progress
   - Stay motivated

5. **Career Guidance**
   - Set career goals
   - Get internship advice
   - Build project ideas

## 🐛 Debugging

If the app crashes, check the terminal for error messages. Most errors are handled gracefully with friendly messages in the app.

### Enable Verbose Mode
```bash
streamlit run app.py --logger.level=debug
```

## 📞 Support

If you find a bug or have a suggestion:
1. Check the error message in the app
2. Look at the terminal output
3. Check common issues above
4. Modify `app.py` or JSON files directly (beginner-friendly!)

## 📜 License

This project is open source. Feel free to modify, use, and share!

## 👨‍💼 Author

Built for students, by developers who care about education.

Made with ❤️ for learning.

---

**Pro Tips:**
- Customize your profile in `data/profile.json`
- Add your own subjects and tasks
- Use the AI daily to stay organized
- Experiment with different Ollama models
- Share with classmates!

Happy learning! 🚀

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app uses a Streamlit theme config at `.streamlit/config.toml` and custom styles in `assets/styles.css`.
