import streamlit as st

from modules.dashboard import show_dashboard
from modules.task_manager import show_task_manager
from modules.study_planner import show_study_planner
from modules.document_chat import show_document_chat
from modules.skill_gap import show_skill_gap
from modules.learning_log import show_learning_log

st.set_page_config(page_title="StudentOS-AI", layout="wide")

st.sidebar.title("🎓 StudentOS-AI")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Task Manager",
        "Study Planner",
        "Document Chat",
        "Skill Gap Analyzer",
        "Learning Log"
    ]
)

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