import json
import os
import streamlit as st

from database.db import init_db
from modules.dashboard import show_dashboard
from modules.task_manager import show_task_manager
from modules.study_planner import show_study_planner
from modules.skill_gap import show_skill_gap
from modules.learning_log import show_learning_log

st.set_page_config(page_title="StudentOS AI Assistant", page_icon="🎓", layout="wide")

init_db()

DATA_DIR = "data"
SAMPLE_PROFILE = {
    "name": "Aanya Sharma",
    "major": "Computer Science",
    "year": "2nd Year",
    "university": "Global Tech University",
    "career_goals": [
        "Build a strong portfolio for software engineering internships",
        "Learn machine learning and data science",
        "Develop better time management for exam preparation"
    ]
}
SAMPLE_SUBJECTS = [
    {
        "name": "Data Structures",
        "teacher": "Mr. Khan",
        "notes": "Focus on trees, graphs, and recursion."
    },
    {
        "name": "Calculus",
        "teacher": "Ms. Patel",
        "notes": "Practice integrals, derivatives, and limits."
    },
    {
        "name": "English Literature",
        "teacher": "Mrs. Singh",
        "notes": "Review poems, short stories, and essay structure."
    }
]
SAMPLE_TASKS = [
    {
        "title": "Math assignment on integrals",
        "status": "Pending",
        "deadline": "2026-06-30",
        "priority": "High",
        "category": "Study"
    },
    {
        "title": "Research internship opportunities",
        "status": "Pending",
        "deadline": "2026-07-10",
        "priority": "Medium",
        "category": "Career"
    },
    {
        "title": "Submit computer science project",
        "status": "Completed",
        "deadline": "2026-06-20",
        "priority": "High",
        "category": "Project"
    }
]
SAMPLE_NOTES = [
    {
        "subject": "Data Structures",
        "note": "Trees have root, children, and leaf nodes. Use recursion for traversal.",
        "date": "2026-06-12"
    },
    {
        "subject": "Calculus",
        "note": "Derivative of sin(x) is cos(x). Integrate with substitution when needed.",
        "date": "2026-06-14"
    }
]
SAMPLE_STUDY_PLAN = [
    {
        "subject": "Calculus",
        "exam_date": "2026-07-05",
        "study_hours": "2",
        "difficulty": "Medium",
        "plan": "Review key chapters, solve sample questions, and revise concepts daily."
    },
    {
        "subject": "Data Structures",
        "exam_date": "2026-07-10",
        "study_hours": "3",
        "difficulty": "Hard",
        "plan": "Practice tree and graph problems; summarize each chapter."
    }
]


def ensure_data_folder():
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def ensure_json_file(filename, sample_data):
    ensure_data_folder()
    path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, indent=2)
        return sample_data

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                raise ValueError("Empty JSON file")
            data = json.loads(content)
            if data is None:
                raise ValueError("Invalid JSON structure")
            return data
    except Exception:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, indent=2)
        return sample_data


def format_student_list(items, fields):
    lines = []
    for item in items:
        values = [f"{field.capitalize()}: {item.get(field, 'N/A')}" for field in fields if item.get(field)]
        lines.append(" - " + ", ".join(values))
    return "\n".join(lines)


def load_student_context():
    profile = ensure_json_file("profile.json", SAMPLE_PROFILE)
    subjects = ensure_json_file("subjects.json", SAMPLE_SUBJECTS)
    tasks = ensure_json_file("tasks.json", SAMPLE_TASKS)
    notes = ensure_json_file("notes.json", SAMPLE_NOTES)
    study_plan = ensure_json_file("study_plan.json", SAMPLE_STUDY_PLAN)

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

    profile_lines = [
        f"Name: {profile.get('name', 'Student')}",
        f"Major: {profile.get('major', 'N/A')}",
        f"Year: {profile.get('year', 'N/A')}",
        f"University: {profile.get('university', 'N/A')}"
    ]

    career_goals = profile.get("career_goals", [])
    if career_goals:
        profile_lines.append("Career Goals: " + "; ".join(career_goals))

    context_lines = ["Profile:", *profile_lines, "", "Subjects:", format_student_list(subjects, ["name", "teacher", "notes"]), "", "Tasks:"]
    for task in tasks:
        context_lines.append(
            f" - [{task.get('status', 'Pending')}] {task.get('title', 'Untitled task')} - Deadline: {task.get('deadline', 'No deadline')} - Priority: {task.get('priority', 'Normal')} - Category: {task.get('category', 'General')}"
        )

    context_lines.extend(["", "Notes:"])
    for note in notes:
        context_lines.append(
            f" - {note.get('date', 'Unknown date')}: {note.get('subject', 'General')} - {note.get('note', '')}"
        )

    context_lines.extend(["", "Study Plan:"])
    for plan in study_plan:
        context_lines.append(
            f" - {plan.get('subject', 'Unknown subject')} (Exam: {plan.get('exam_date', 'TBD')}) - Hours/day: {plan.get('study_hours', 'N/A')} - Difficulty: {plan.get('difficulty', 'N/A')}"
        )
        if plan.get("plan"):
            context_lines.append(f"   Plan: {plan.get('plan')}")

    if career_goals:
        context_lines.extend(["", "Career Goals:"])
        for goal in career_goals:
            context_lines.append(f" - {goal}")

    return "\n".join(context_lines)


def extract_section_text(context, section_name):
    lines = [line.rstrip() for line in context.splitlines()]
    start = None
    for index, line in enumerate(lines):
        if line.strip().lower() == section_name.lower() + ":":
            start = index + 1
            break

    if start is None:
        return ""

    section_lines = []
    for line in lines[start:]:
        if not line.strip():
            if section_lines:
                break
            continue
        if line.endswith(":") and section_lines:
            break
        section_lines.append(line)

    return "\n".join(section_lines).strip()


def filter_lines(lines, keywords):
    return [line for line in lines if any(keyword in line.lower() for keyword in keywords)]


def get_ai_response(user_question, student_context, chat_history):
    question = user_question.strip()
    if not question:
        return "Please type a question so I can help with your studies, tasks, notes, deadlines, or goals."

    text = question.lower()
    task_lines = extract_section_text(student_context, "Tasks").splitlines()
    notes_lines = extract_section_text(student_context, "Notes").splitlines()
    study_lines = extract_section_text(student_context, "Study Plan").splitlines()
    subject_lines = extract_section_text(student_context, "Subjects").splitlines()
    career_lines = extract_section_text(student_context, "Career Goals").splitlines()

    if any(keyword in text for keyword in ["pending", "pending tasks", "incomplete", "not done"]):
        matched = filter_lines(task_lines, ["pending"])
        return "\n".join(matched) if matched else "You have no pending tasks in your current student profile."

    if any(keyword in text for keyword in ["completed", "done", "finished"]):
        matched = filter_lines(task_lines, ["completed"])
        return "\n".join(matched) if matched else "You have no completed tasks recorded yet."

    if any(keyword in text for keyword in ["deadline", "due", "due date", "due dates"]):
        return "\n".join(task_lines) if task_lines else "There are no tasks with deadlines in your profile yet."

    if any(keyword in text for keyword in ["priority", "important", "urgent"]):
        matched = filter_lines(task_lines, ["high", "medium", "low"])
        return "\n".join(matched) if matched else "Your task list does not include priority details yet."

    if any(keyword in text for keyword in ["study plan", "plan", "today", "schedule", "study schedule"]):
        return "\n".join(study_lines) if study_lines else "Your study plan is currently empty. Add a study plan to get better suggestions."

    if any(keyword in text for keyword in ["subject", "course", "class"]):
        return "\n".join(subject_lines) if subject_lines else "No subjects are available in your current student data."

    if any(keyword in text for keyword in ["note", "notes", "summary"]):
        if notes_lines:
            return "Here are your notes:\n" + "\n".join(notes_lines[:5])
        return "You do not have any notes yet. Add notes to summarize your study material."

    if any(keyword in text for keyword in ["goal", "career", "future"]):
        return "\n".join(career_lines) if career_lines else "You have not added career goals yet. Add your goals in the profile data."

    if any(keyword in text for keyword in ["help", "advice", "tips", "study tips", "productivity"]):
        advice = [
            "Review your pending tasks first and use deadlines to plan your day.",
            "Break study plan subject goals into smaller daily steps.",
            "Use notes to review topics before exams and update them regularly.",
            "Focus on high-priority tasks and avoid multitasking when studying."
        ]
        return "\n".join(advice)

    if subject_lines and task_lines:
        return "Here is a quick summary from your student data:\n" + "\n".join(subject_lines[:3]) + "\n" + "\n".join(task_lines[:3])

    return "I can help with questions about your tasks, study plan, subjects, notes, deadlines, and goals. Ask me about any of these areas."


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


# Load custom CSS
try:
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    st.markdown(
        """
        <style>
        body {background-color: #f8fafc}
        .stButton>button {border-radius:10px}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Initialize navigation state
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "nav_radio" not in st.session_state:
    st.session_state.nav_radio = st.session_state.page

with st.sidebar:
    st.markdown("# 🎓 StudentOS-AI")
    st.markdown("Personal student productivity assistant — stay organized, study smarter.")
    st.divider()
    theme_choice = st.selectbox("Theme", ["Default", "Warm", "Teal", "Dark"], index=0, key="theme_choice")
    font_choice = st.selectbox("Font", ["Inter", "Poppins"], index=0, key="font_choice")
    compact_sidebar = st.checkbox("Compact sidebar", value=False, key="compact_sidebar")

    nav = st.radio(
        "Navigate",
        ["Home", "Notes", "Tasks", "Study Planner", "AI Assistant", "About"],
        index=(0 if st.session_state.nav_radio not in ["Home", "Notes", "Tasks", "Study Planner", "AI Assistant", "About"] else ["Home", "Notes", "Tasks", "Study Planner", "AI Assistant", "About"].index(st.session_state.nav_radio)),
        key="nav_radio",
    )
    st.divider()
    st.markdown("Built by Ajay — Python · Streamlit · SQLite")

theme_map = {
    "Default": "",
    "Warm": "theme-warm",
    "Teal": "theme-teal",
    "Dark": "theme-dark",
}

theme_class = theme_map.get(st.session_state.get("theme_choice", "Default"), "")
compact_css = "" if not st.session_state.get("compact_sidebar", False) else "<style>[data-testid=\"stSidebar\"]{padding:8px 8px 12px 8px}</style>"
st.markdown(f"<div class='{theme_class}'></div>", unsafe_allow_html=True)
if compact_css:
    st.markdown(compact_css, unsafe_allow_html=True)
font_map = {"Inter": "Inter, sans-serif", "Poppins": "Poppins, sans-serif"}
font_css = f"<style>body, .block-container{{font-family: {font_map.get(st.session_state.get('font_choice','Inter'))};}}</style>"
st.markdown(font_css, unsafe_allow_html=True)

st.session_state.page = st.session_state.get("nav_radio", st.session_state.page)
page = st.session_state.page


def show_home():
    st.markdown("<div class='banner'><div><div class='title'>StudentOS-AI</div><div class='subtitle'>A polished productivity dashboard for students.</div></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='page-header'><h1>StudentOS-AI</h1><p class='lead'>A polished productivity dashboard to help students manage notes, tasks, study plans and get AI assistance.</p></div>", unsafe_allow_html=True)

    features = [
        ("📚", "Notes", "Keep your study notes and learning log organized.", "Notes"),
        ("✅", "Tasks", "Track assignments, deadlines and priorities.", "Tasks"),
        ("🗓️", "Study Planner", "Plan your study sessions and stay on track.", "Study Planner"),
        ("🤖", "AI Assistant", "Chat with your student AI assistant.", "AI Assistant"),
        ("📊", "Dashboard", "Overview of progress and activity.", "Dashboard"),
        ("🔍", "Skill Gap", "Analyze skill gaps and suggested learning resources.", "Skill Gap")
    ]

    def set_page(target):
        st.session_state.page = target
        st.session_state.nav_radio = target

    rows = [st.columns(3), st.columns(3)]
    for i, feat in enumerate(features):
        with rows[i // 3][i % 3]:
            icon, title, desc, target = feat
            st.markdown(f"<div class='card'><div class='icon'>{icon}</div><div class='card-title'>{title}</div><div class='card-desc'>{desc}</div></div>", unsafe_allow_html=True)
            if st.button(f"Open {target}", key=f"open-{i}", on_click=set_page, args=(target,)):
                pass


def show_about():
    st.markdown("<h2>About StudentOS-AI</h2>", unsafe_allow_html=True)
    st.markdown(
        "StudentOS-AI is a lightweight productivity app built with Streamlit to help students organize notes, tasks and study plans.\n\nFeatures include:\n- Notes & Learning Log\n- Task Manager\n- Study Planner\n- AI Assistant for student questions\n- Skill Gap Analyzer and Dashboard",
        unsafe_allow_html=True,
    )


def show_ai_assistant():
    st.title("🤖 StudentOS AI Assistant")
    st.caption("Ask about your studies, tasks, notes, deadlines, and goals.")

    student_context = load_student_context()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I’m your StudentOS AI Assistant. Ask me anything about your studies, tasks, notes, deadlines, and goals."
            }
        ]

    clear_col, _ = st.columns([1, 6])
    with clear_col:
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hello! I’m your StudentOS AI Assistant. Ask me anything about your studies, tasks, notes, deadlines, and goals."
                }
            ]
            rerun_app()

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
        else:
            st.chat_message("user").write(message["content"])

    user_input = st.chat_input("Type your student question here...", key="ai_input")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = get_ai_response(user_input, student_context, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        rerun_app()


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
    show_dashboard()
