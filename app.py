import streamlit as st

st.set_page_config(page_title="StudentOS-AI")

st.title("🎓 StudentOS-AI")

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

st.write(f"You selected: {menu}")