import streamlit as st

from database.db import init_db
from modules.dashboard import show_dashboard
from modules.task_manager import show_task_manager
from modules.study_planner import show_study_planner
from modules.document_chat import show_document_chat
from modules.skill_gap import show_skill_gap
from modules.learning_log import show_learning_log

st.set_page_config(
    page_title="StudentOS-AI",
    page_icon="🎓",
    layout="wide"
)

init_db()

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

.stButton>button {
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: 600;
}

[data-testid="stSidebar"] {
    background-color: #eef2ff;
}

h1, h2, h3 {
    color: #1e293b;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🎓 StudentOS-AI")
st.sidebar.write("Personal Student Productivity Assistant")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Task Manager",
        "Study Planner",
        "Document Chat",
        "Skill Gap Analyzer",
        "Learning Log"
    ]
)

st.sidebar.divider()
st.sidebar.info("Built by Ajay using Python, Streamlit and SQLite.")

if menu == "Dashboard":
    show_dashboard()
elif menu == "Task Manager":
    show_task_manager()
elif menu == "Study Planner":
    show_study_planner()
elif menu == "Document Chat":
    show_document_chat()
elif menu == "Skill Gap Analyzer":
    show_skill_gap()
elif menu == "Learning Log":
    show_learning_log()