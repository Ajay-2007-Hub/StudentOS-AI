"""
StudentOS AI Assistant - A beginner-friendly mini ChatGPT for students
Built with Streamlit, Python, and optional Ollama local AI
"""

import json
import os
import streamlit as st
from datetime import datetime

# Try to import Ollama for local AI support
try:
    import ollama
    OLLAMA_PACKAGE_AVAILABLE = True
except ImportError:
    OLLAMA_PACKAGE_AVAILABLE = False

from database.db import init_db
from modules.dashboard import show_dashboard
from modules.task_manager import show_task_manager
from modules.study_planner import show_study_planner
from modules.skill_gap import show_skill_gap
from modules.learning_log import show_learning_log

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="StudentOS AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()

# ===== CONFIGURATION =====
DATA_DIR = "data"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")

# ===== SAMPLE DATA FOR B.TECH AI STUDENT =====
SAMPLE_PROFILE = {
    "name": "Ajay",
    "department": "Artificial Intelligence and Data Science",
    "semester": 3,
    "goal": "Build strong projects, improve coding, prepare for internships"
}

SAMPLE_SUBJECTS = [
    {
        "name": "Database Management Systems",
        "teacher": "Prof. Rajesh",
        "notes": "Focus on keys, normalization, SQL, ER model"
    },
    {
        "name": "Advanced Java Programming",
        "teacher": "Prof. Sharma",
        "notes": "Classes, objects, inheritance, exception handling"
    },
    {
        "name": "Artificial Intelligence and Decision Making",
        "teacher": "Prof. Priya",
        "notes": "Search algorithms, machine learning basics, decision making"
    },
    {
        "name": "Discrete Mathematics",
        "teacher": "Prof. Kumar",
        "notes": "Sets, graphs, combinatorics, propositional logic"
    },
    {
        "name": "Computer Organization and Architecture",
        "teacher": "Prof. Yadav",
        "notes": "CPU design, memory hierarchy, assembly language"
    }
]

SAMPLE_TASKS = [
    {
        "title": "Complete DBMS assignment",
        "status": "Pending",
        "deadline": "2026-06-30",
        "priority": "High",
        "category": "Study"
    },
    {
        "title": "Revise Java OOP concepts",
        "status": "Pending",
        "deadline": "2026-07-05",
        "priority": "High",
        "category": "Study"
    },
    {
        "title": "Prepare AI notes",
        "status": "Pending",
        "deadline": "2026-07-08",
        "priority": "Medium",
        "category": "Study"
    },
    {
        "title": "Update GitHub project",
        "status": "Pending",
        "deadline": "2026-07-10",
        "priority": "High",
        "category": "Project"
    },
    {
        "title": "Practice coding problems",
        "status": "Pending",
        "deadline": "2026-06-25",
        "priority": "Medium",
        "category": "Practice"
    }
]

SAMPLE_NOTES = [
    {
        "subject": "DBMS",
        "content": "Keys: Primary (unique identifier), Foreign (reference), Candidate, Super, Composite. Normalization: 1NF, 2NF, 3NF prevent anomalies. ER Model: Entities and relationships with attributes."
    },
    {
        "subject": "Java",
        "content": "Classes are blueprints for objects. Inheritance allows code reuse. Exception handling with try-catch prevents crashes. Polymorphism enables flexible code."
    },
    {
        "subject": "AI",
        "content": "Search algorithms: BFS (breadth-first), DFS (depth-first), A* (optimal). Machine learning: supervised (classification, regression), unsupervised (clustering)."
    }
]

SAMPLE_STUDY_PLAN = [
    {
        "date": "2026-06-20",
        "subject": "DBMS",
        "hours": 1.5,
        "task": "Revise normalization and complete assignment"
    },
    {
        "date": "2026-06-20",
        "subject": "Java",
        "hours": 1.0,
        "task": "Practice inheritance and polymorphism"
    },
    {
        "date": "2026-06-20",
        "subject": "AI",
        "hours": 1.0,
        "task": "Understand search algorithms"
    }
]

# ===== DATA MANAGEMENT FUNCTIONS =====

def ensure_data_folder():
    """Create data folder if it doesn't exist"""
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def safe_load_json(file_path, default_data):
    """
    Load JSON file safely. If file is missing, empty, or corrupted,
    return default data and recreate the file.
    """
    ensure_data_folder()
    
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    if data is not None:
                        return data
    except (json.JSONDecodeError, ValueError, IOError):
        pass
    
    # If we reach here, file is missing/empty/corrupted - recreate it
    safe_save_json(file_path, default_data)
    return default_data


def safe_save_json(file_path, data):
    """Save data to JSON file safely"""
    ensure_data_folder()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        st.warning(f"Could not save {file_path}: {e}")


def ensure_data_files():
    """Ensure all required data files exist with sample data"""
    ensure_data_folder()
    
    safe_load_json(os.path.join(DATA_DIR, "profile.json"), SAMPLE_PROFILE)
    safe_load_json(os.path.join(DATA_DIR, "subjects.json"), SAMPLE_SUBJECTS)
    safe_load_json(os.path.join(DATA_DIR, "tasks.json"), SAMPLE_TASKS)
    safe_load_json(os.path.join(DATA_DIR, "notes.json"), SAMPLE_NOTES)
    safe_load_json(os.path.join(DATA_DIR, "study_plan.json"), SAMPLE_STUDY_PLAN)


def load_student_context():
    """
    Load all student data and format it into a clean context string.
    This is used by the AI to understand the student's background.
    """
    ensure_data_files()
    
    profile = safe_load_json(os.path.join(DATA_DIR, "profile.json"), SAMPLE_PROFILE)
    subjects = safe_load_json(os.path.join(DATA_DIR, "subjects.json"), SAMPLE_SUBJECTS)
    tasks = safe_load_json(os.path.join(DATA_DIR, "tasks.json"), SAMPLE_TASKS)
    notes = safe_load_json(os.path.join(DATA_DIR, "notes.json"), SAMPLE_NOTES)
    study_plan = safe_load_json(os.path.join(DATA_DIR, "study_plan.json"), SAMPLE_STUDY_PLAN)
    
    # Ensure data types
    if not isinstance(profile, dict):
        profile = SAMPLE_PROFILE
    if not isinstance(subjects, list):
        subjects = SAMPLE_SUBJECTS
    if not isinstance(tasks, list):
        tasks = SAMPLE_TASKS
    if not isinstance(notes, list):
        notes = SAMPLE_NOTES
    if not isinstance(study_plan, list):
        study_plan = SAMPLE_STUDY_PLAN
    
    context_lines = []
    
    # Profile section
    context_lines.append("PROFILE:")
    context_lines.append(f"Name: {profile.get('name', 'Student')}")
    context_lines.append(f"Department: {profile.get('department', 'N/A')}")
    context_lines.append(f"Semester: {profile.get('semester', 'N/A')}")
    context_lines.append(f"Goal: {profile.get('goal', 'N/A')}")
    context_lines.append("")
    
    # Subjects section
    context_lines.append("SUBJECTS:")
    for subject in subjects:
        context_lines.append(f"- {subject.get('name', 'Unknown')}")
        if subject.get('teacher'):
            context_lines.append(f"  Teacher: {subject.get('teacher')}")
        if subject.get('notes'):
            context_lines.append(f"  Notes: {subject.get('notes')}")
    context_lines.append("")
    
    # Tasks section
    context_lines.append("TASKS:")
    for task in tasks:
        status = task.get('status', 'Pending')
        title = task.get('title', 'Untitled')
        deadline = task.get('deadline', 'No deadline')
        priority = task.get('priority', 'Normal')
        context_lines.append(f"- [{status}] {title} (Deadline: {deadline}, Priority: {priority})")
    context_lines.append("")
    
    # Notes section
    context_lines.append("NOTES:")
    for note in notes:
        subject = note.get('subject', 'General')
        content = note.get('content', '')
        context_lines.append(f"- {subject}: {content}")
    context_lines.append("")
    
    # Study Plan section
    context_lines.append("TODAY'S STUDY PLAN:")
    for plan in study_plan:
        subject = plan.get('subject', 'Unknown')
        hours = plan.get('hours', 'N/A')
        task = plan.get('task', '')
        context_lines.append(f"- {subject} ({hours}h): {task}")
    
    return "\n".join(context_lines)

# ===== OLLAMA AI SUPPORT =====

def is_ollama_running():
    """
    Check if Ollama is available and running safely.
    Returns True only if everything is working.
    """
    if not OLLAMA_PACKAGE_AVAILABLE:
        return False
    
    try:
        # Try to ping Ollama
        response = ollama.list()
        return True
    except Exception:
        return False


def get_ollama_response(user_question, student_context, chat_history):
    """
    Get response from Ollama local AI model.
    Returns None if Ollama fails - caller will use fallback.
    """
    if not OLLAMA_PACKAGE_AVAILABLE or not is_ollama_running():
        return None
    
    try:
        # Create system prompt with student context
        system_prompt = f"""You are StudentOS AI, a helpful mini ChatGPT for students. You help students with their studies, tasks, deadlines, and career goals.

Student Information:
{student_context}

Instructions:
- Answer naturally and clearly
- Use the student data when questions are about tasks, notes, subjects, study plan, deadlines, or career goals
- For general questions, answer like ChatGPT would
- Keep answers simple, friendly, and useful for a beginner student
- Don't dump raw JSON or data unless specifically asked
- Be supportive and encouraging"""
        
        # Prepare messages for chat history (last 6 messages to avoid large prompts)
        messages = []
        for msg in chat_history[-6:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current question
        messages.append({
            "role": "user",
            "content": user_question
        })
        
        # Get response from Ollama
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            system=system_prompt
        )
        
        return response.get("message", {}).get("content", None)
    
    except Exception:
        return None

# ===== FALLBACK RULE-BASED SYSTEM =====

def fallback_rule_based_response(user_question, student_context):
    """
    Fallback AI response when Ollama is not available.
    Handles common student-related questions with predefined responses.
    """
    text = user_question.lower().strip()
    
    # Greetings
    greetings = ["hi", "hello", "hey", "hallo", "hai", "vanakkam", "good morning", "good evening", "good night", "namaste"]
    if any(greeting in text for greeting in greetings):
        return "Hello! 👋 I'm your StudentOS AI Assistant. I can help you with your tasks, subjects, notes, study plan, deadlines, and career goals. What would you like to know?"
    
    # Check for pending tasks
    if any(keyword in text for keyword in ["pending", "task", "deadline", "due", "incomplete"]):
        pending_lines = []
        if "TASKS:" in student_context:
            tasks_section = student_context.split("TASKS:")[1].split("\n\n")[0]
            for line in tasks_section.split("\n"):
                if "[Pending]" in line:
                    pending_lines.append(line.strip())
        
        if pending_lines:
            return "Here are your pending tasks:\n\n" + "\n".join(pending_lines[:5])
        else:
            return "You have no pending tasks right now. Great job! 🎉"
    
    # Check for priority tasks
    if any(keyword in text for keyword in ["priority", "important", "urgent", "high priority"]):
        priority_lines = []
        if "TASKS:" in student_context:
            tasks_section = student_context.split("TASKS:")[1].split("\n\n")[0]
            for line in tasks_section.split("\n"):
                if "High" in line:
                    priority_lines.append(line.strip())
        
        if priority_lines:
            return "Here are your high-priority tasks:\n\n" + "\n".join(priority_lines[:5])
        else:
            return "No high-priority tasks at the moment."
    
    # Check for subjects
    if any(keyword in text for keyword in ["subject", "subjects", "course", "courses", "class", "classes"]):
        subject_lines = []
        if "SUBJECTS:" in student_context:
            subjects_section = student_context.split("SUBJECTS:")[1].split("\n\n")[0]
            for line in subjects_section.split("\n"):
                if line.strip().startswith("-"):
                    subject_lines.append(line.strip())
        
        if subject_lines:
            return "Here are your subjects:\n\n" + "\n".join(subject_lines[:5])
        else:
            return "No subjects found in your profile."
    
    # Check for notes
    if any(keyword in text for keyword in ["note", "notes", "summary", "revise", "review"]):
        note_lines = []
        if "NOTES:" in student_context:
            notes_section = student_context.split("NOTES:")[1].split("\n\n")[0]
            for line in notes_section.split("\n"):
                if line.strip().startswith("-"):
                    note_lines.append(line.strip())
        
        if note_lines:
            return "Here are your study notes:\n\n" + "\n".join(note_lines[:5])
        else:
            return "You don't have any notes yet. Start adding notes to organize your learning!"
    
    # Check for today's study plan
    if any(keyword in text for keyword in ["today", "study plan", "schedule", "timetable", "plan"]):
        if "TODAY'S STUDY PLAN:" in student_context:
            plan_section = student_context.split("TODAY'S STUDY PLAN:")[1].strip()
            plan_lines = [line.strip() for line in plan_section.split("\n") if line.strip().startswith("-")]
            if plan_lines:
                return "Here's your study plan for today:\n\n" + "\n".join(plan_lines)
        return "No study plan set for today. Try creating one in the Study Planner section!"
    
    # Check for career/goals
    if any(keyword in text for keyword in ["career", "goal", "goals", "internship", "resume", "project", "github"]):
        if "PROFILE:" in student_context:
            profile_section = student_context.split("PROFILE:")[1].split("\n\n")[0]
            for line in profile_section.split("\n"):
                if "Goal:" in line:
                    return f"Your career goal: {line.replace('Goal:', '').strip()}\n\nFocus on building projects, improving your coding skills, and gaining practical experience!"
        return "Set career goals in your profile to get better guidance!"
    
    # Check for study advice
    if any(keyword in text for keyword in ["advice", "tips", "how to study", "focus", "productivity", "concentrate"]):
        advice = [
            "1. Break your tasks into smaller chunks and tackle them one by one",
            "2. Follow your study plan and allocate specific time for each subject",
            "3. Review your notes regularly to strengthen your memory",
            "4. Practice coding problems daily to improve your skills",
            "5. Take short breaks between study sessions to stay fresh",
            "6. Set realistic goals and celebrate your progress",
            "7. Stay organized and manage your deadlines carefully"
        ]
        return "Here are some study tips:\n\n" + "\n".join(advice)
    
    # Default response when running in basic mode
    return "I'm running in basic mode without full AI. I can answer questions about your tasks, subjects, notes, study plan, and career goals. For more advanced help, please set up Ollama to enable full ChatGPT-like capabilities!"

# ===== MAIN AI RESPONSE FUNCTION =====

def get_ai_response(user_question, student_context, chat_history):
    """
    Main function to get AI response.
    Tries Ollama first, falls back to rule-based system if needed.
    """
    question = user_question.strip()
    
    # Handle empty input
    if not question:
        return "Please ask me something about your studies, tasks, notes, or goals!"
    
    # Try Ollama first
    if OLLAMA_PACKAGE_AVAILABLE and is_ollama_running():
        try:
            ollama_response = get_ollama_response(question, student_context, chat_history)
            if ollama_response:
                return ollama_response
        except Exception:
            pass
    
    # Fall back to rule-based system
    return fallback_rule_based_response(question, student_context)

# ===== CURSOR EFFECTS =====

def inject_cursor_effects():
    """
    Inject CSS and JavaScript for cursor glow and click ripple effects.
    Effects are lightweight and don't interfere with Streamlit UI.
    """
    cursor_css_js = """
    <style>
        /* Cursor glow trail */
        .cursor-trail {
            position: fixed;
            pointer-events: none;
            border-radius: 50%;
            z-index: 9998;
            box-shadow: 0 0 8px rgba(59, 130, 246, 0.6), 0 0 20px rgba(59, 130, 246, 0.3);
        }
        
        /* Click ripple effect */
        .ripple {
            position: fixed;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.6) 0%, rgba(59, 130, 246, 0.2) 70%, transparent 100%);
            pointer-events: none;
            z-index: 9998;
            animation: ripple-animation 0.6s ease-out forwards;
        }
        
        @keyframes ripple-animation {
            0% {
                transform: scale(0);
                opacity: 1;
            }
            100% {
                transform: scale(1);
                opacity: 0;
            }
        }
    </style>
    
    <script>
        // Cursor trail effect
        const trailMaxLength = 20;
        let trailPoints = [];
        
        document.addEventListener('mousemove', (e) => {
            // Create trail point
            const trail = document.createElement('div');
            trail.className = 'cursor-trail';
            trail.style.width = '6px';
            trail.style.height = '6px';
            trail.style.left = (e.clientX - 3) + 'px';
            trail.style.top = (e.clientY - 3) + 'px';
            document.body.appendChild(trail);
            
            trailPoints.push(trail);
            
            // Remove old trail points
            if (trailPoints.length > trailMaxLength) {
                const oldTrail = trailPoints.shift();
                oldTrail.remove();
            }
            
            // Fade out old trails
            trailPoints.forEach((point, index) => {
                const alpha = (index / trailPoints.length) * 0.7;
                point.style.opacity = alpha;
            });
        });
        
        // Click ripple effect
        document.addEventListener('click', (e) => {
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            ripple.style.width = '2px';
            ripple.style.height = '2px';
            ripple.style.left = e.clientX + 'px';
            ripple.style.top = e.clientY + 'px';
            document.body.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    </script>
    """
    
    st.markdown(cursor_css_js, unsafe_allow_html=True)

# ===== LOAD CUSTOM CSS =====

try:
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    pass

# ===== INITIALIZE SESSION STATE =====
# Initialize all session state values BEFORE creating widgets
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I'm StudentOS AI Assistant. Ask me about your studies, tasks, notes, deadlines, and career goals!"
        }
    ]

if "cursor_effects_enabled" not in st.session_state:
    st.session_state.cursor_effects_enabled = True

# Ensure all data files exist
ensure_data_files()

# ===== SIDEBAR NAVIGATION AND STATUS =====
with st.sidebar:
    st.markdown("# 🎓 StudentOS AI")
    st.markdown("Your personal AI assistant for learning, tasks, and growth.")
    st.divider()
    
    # AI Status
    st.markdown("### AI Status")
    if OLLAMA_PACKAGE_AVAILABLE and is_ollama_running():
        st.success("✅ Ollama: Active")
        st.caption(f"Model: {OLLAMA_MODEL}")
    else:
        st.info("📚 Basic Mode")
        st.caption("Ollama not active - using fallback")
    
    st.divider()
    
    # Cursor effects toggle
    st.session_state.cursor_effects_enabled = st.checkbox(
        "Enable cursor effects",
        value=st.session_state.cursor_effects_enabled,
        key="cursor_toggle"
    )
    
    # Navigation radio
    pages = ["Home", "Notes", "Tasks", "Study Planner", "AI Assistant", "About"]
    selected_page = st.radio(
        "Navigate",
        pages,
        index=pages.index(st.session_state.page),
        key="nav_radio",
    )
    
    # Update page when navigation changes
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
    
    st.divider()
    
    # Instructions
    st.markdown("### Enable Full AI")
    st.caption("""
    1. Open terminal
    2. Run: `ollama serve`
    3. In another terminal: `ollama pull gemma3:1b`
    4. Run: `streamlit run app.py`
    """)
    
    st.divider()
    st.markdown("Built with ❤️ — Python, Streamlit, Ollama")

# ===== PAGE FUNCTIONS =====

def show_home():
    """Display home page with overview and quick links"""
    st.markdown("# 🎓 Welcome to StudentOS AI")
    st.markdown("Your complete student productivity + AI assistant platform")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### What You Can Do
        - 💬 **Chat with AI** about your studies
        - 📝 **Manage notes** from all subjects
        - ✅ **Track tasks** and deadlines
        - 📅 **Plan study sessions** for exams
        - 🤖 **Get smart advice** from AI
        - 📊 **See your progress**
        """)
    
    with col2:
        st.markdown("""
        ### AI Assistant Features
        - Answer general questions
        - Summarize your notes
        - List pending tasks
        - Suggest study plans
        - Provide study tips
        - Support career planning
        """)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝 Go to Notes", use_container_width=True):
            st.session_state.page = "Notes"
            st.rerun()
    
    with col2:
        if st.button("✅ Go to Tasks", use_container_width=True):
            st.session_state.page = "Tasks"
            st.rerun()
    
    with col3:
        if st.button("🤖 Go to AI Assistant", use_container_width=True):
            st.session_state.page = "AI Assistant"
            st.rerun()
    
    st.divider()
    st.info("💡 **Pro Tip:** Open the AI Assistant and say \"Hello\" to start chatting!")


def show_about():
    """Display about page with project information"""
    st.markdown("# 📖 About StudentOS AI")
    
    st.markdown("""
    ## What is StudentOS AI?
    
    StudentOS AI is a beginner-friendly mini ChatGPT designed specifically for students. 
    It helps you manage your academic life while providing intelligent assistance powered by local AI.
    
    ## Features
    
    - **ChatGPT-like AI Assistant** - Ask questions about anything!
    - **Local AI with Ollama** - Private, fast, runs on your computer
    - **Fallback Mode** - Works even without Ollama installed
    - **Student Task Manager** - Track assignments and deadlines
    - **Study Notes** - Organize knowledge by subject
    - **Study Planner** - Plan your learning sessions
    - **JSON-based Memory** - Data stored locally, no cloud needed
    - **Modern UI** - Clean, intuitive design
    
    ## Technologies Used
    
    - **Python** - Programming language
    - **Streamlit** - Web app framework
    - **Ollama** - Local AI models
    - **JSON** - Data storage
    - **CSS** - Styling and effects
    
    ## How to Run
    
    ### Basic Mode (without AI)
    ```bash
    pip install -r requirements.txt
    streamlit run app.py
    ```
    
    ### Full AI Mode (with Ollama)
    1. Install Ollama from https://ollama.ai
    2. In terminal 1: `ollama serve`
    3. In terminal 2: `ollama pull gemma3:1b`
    4. In terminal 3: `streamlit run app.py`
    
    ### Custom Port
    ```bash
    streamlit run app.py --server.port 8502
    ```
    
    ## Student Profile Used
    
    - **Name:** Ajay
    - **Department:** Artificial Intelligence and Data Science
    - **Semester:** 3
    - **Goal:** Build strong projects, improve coding, prepare for internships
    
    ## Author
    
    Built by and for students who want to learn better! 🎓
    
    ## License
    
    Open source - Feel free to modify and use!
    """)


def show_ai_assistant():
    """Display AI Assistant chat interface"""
    st.title("🤖 StudentOS AI Assistant")
    st.caption("Ask about your studies, tasks, notes, deadlines, and goals.")
    
    # Load student context
    student_context = load_student_context()
    
    # Display clear chat button
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("🗑️ Clear Chat", key="clear_chat_btn"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "👋 Hello! I'm StudentOS AI Assistant. Ask me about your studies, tasks, notes, deadlines, and career goals!"
                }
            ]
            st.rerun()
    
    with col3:
        # Show AI mode
        if OLLAMA_PACKAGE_AVAILABLE and is_ollama_running():
            st.caption("✅ Full AI Mode")
        else:
            st.caption("📚 Basic Mode")
    
    st.divider()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your question here...", key="ai_chat_input")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        response = get_ai_response(user_input, student_context, st.session_state.messages)
        
        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Rerun to display new messages
        st.rerun()

# ===== PAGE ROUTER =====

page = st.session_state.page

try:
    if page == "Home":
        show_home()
    elif page == "Notes":
        show_learning_log()
    elif page == "Tasks":
        show_task_manager()
    elif page == "Study Planner":
        show_study_planner()
    elif page == "AI Assistant":
        show_ai_assistant()
    elif page == "About":
        show_about()
    else:
        # Default to home if page is invalid
        show_home()
except Exception as e:
    st.error(f"Error loading page: {str(e)}")
    st.info("The page encountered an error. Try refreshing or navigating to Home.")

# ===== INJECT CURSOR EFFECTS =====
if st.session_state.cursor_effects_enabled:
    inject_cursor_effects()
