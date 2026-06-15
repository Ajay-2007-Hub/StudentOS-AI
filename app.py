import streamlit as st

from database.db import init_db
from modules.dashboard import show_dashboard
from modules.task_manager import show_task_manager
from modules.study_planner import show_study_planner
from modules.document_chat import show_document_chat
from modules.skill_gap import show_skill_gap
from modules.learning_log import show_learning_log

st.set_page_config(page_title="StudentOS-AI", page_icon="🎓", layout="wide")

init_db()

# Load custom CSS
try:
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    # Fallback minimal styles if file missing
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

# Ensure a separate widget key for the radio so we don't overwrite it later
if "nav_radio" not in st.session_state:
    st.session_state.nav_radio = st.session_state.page

with st.sidebar:
    st.markdown("# 🎓 StudentOS-AI")
    st.markdown("Personal student productivity assistant — stay organized, study smarter.")
    st.divider()
    # Theme and font selectors
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

# Apply theme overrides via small inline CSS (updates on re-run)
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
# Apply font choice
font_map = {"Inter": "Inter, sans-serif", "Poppins": "Poppins, sans-serif"}
font_css = f"<style>body, .block-container{{font-family: {font_map.get(st.session_state.get('font_choice','Inter'))};}}</style>"
st.markdown(font_css, unsafe_allow_html=True)

# Keep session state page in sync with radio widget selection
st.session_state.page = st.session_state.get('nav_radio', st.session_state.page)

# Neon cursor toggle
neon_enabled = st.sidebar.checkbox("Enable neon cursor", value=False, key="neon_cursor")
if neon_enabled:
    # Hide native cursor and inject the neon cursor element + JS
    st.markdown(
        """
    <style>body { cursor: none !important; }</style>
    <div id="neon-cursor" class="neon-cursor"></div>
    <script>
    const cursor = document.getElementById('neon-cursor');
    let mx = window.innerWidth/2, my = window.innerHeight/2;
    document.addEventListener('mousemove', (e)=>{
      mx = e.clientX; my = e.clientY;
      cursor.style.left = mx + 'px'; cursor.style.top = my + 'px'; cursor.classList.remove('hidden');
    });
    document.addEventListener('mousedown', ()=>{ cursor.classList.add('big'); });
    document.addEventListener('mouseup', ()=>{ cursor.classList.remove('big'); });
    document.addEventListener('mouseleave', ()=>{ cursor.classList.add('hidden'); });
    document.addEventListener('mouseenter', ()=>{ cursor.classList.remove('hidden'); });
    </script>
    """,
        unsafe_allow_html=True,
    )


page = st.session_state.page


def show_home():
    st.markdown("<div class='banner'><div><div class='title'>StudentOS-AI</div><div class='subtitle'>A polished productivity dashboard for students.</div></div></div>", unsafe_allow_html=True)

    st.markdown("<div class='page-header'><h1>StudentOS-AI</h1><p class='lead'>A polished productivity dashboard to help students manage notes, tasks, study plans and get AI assistance.</p></div>", unsafe_allow_html=True)

    cols = st.columns(3)
    features = [
        ("📚", "Notes", "Keep your study notes and learning log organized.", "Notes"),
        ("✅", "Tasks", "Track assignments, deadlines and priorities.", "Tasks"),
        ("🗓️", "Study Planner", "Plan your study sessions and stay on track.", "Study Planner"),
        ("🤖", "AI Assistant", "Upload documents and ask the AI for help.", "AI Assistant"),
        ("📊", "Dashboard", "Overview of progress and activity.", "Dashboard"),
        ("🔍", "Skill Gap", "Analyze skill gaps and suggested learning resources.", "Skill Gap Analyzer"),
    ]

    # Render cards in a responsive grid
    def set_page(target):
        st.session_state.page = target
        # update radio widget value as well (safe inside callback)
        st.session_state.nav_radio = target

    for i, feat in enumerate(features):
        if i % 3 == 0:
            row = st.columns(3)

        with row[i % 3]:
            icon, title, desc, target = feat
            st.markdown(f"<div class='card'><div class='icon'>{icon}</div><div class='card-title'>{title}</div><div class='card-desc'>{desc}</div></div>", unsafe_allow_html=True)
            if st.button(f"Open {target}", key=f"open-{i}", on_click=set_page, args=(target,)):
                # callback will handle navigation and rerun
                pass


def show_about():
    st.markdown("<h2>About StudentOS-AI</h2>", unsafe_allow_html=True)
    st.markdown(
        "StudentOS-AI is a lightweight productivity app built with Streamlit to help students organize notes, tasks and study plans.\n\nFeatures include:\n- Notes & Learning Log\n- Task Manager\n- Study Planner\n- Document-based AI Assistant\n- Skill Gap Analyzer and Dashboard",
        unsafe_allow_html=True,
    )


if page == "Home":
    show_home()
elif page == "Notes":
    show_learning_log()
elif page == "Tasks":
    show_task_manager()
elif page == "Study Planner":
    show_study_planner()
elif page == "AI Assistant":
    show_document_chat()
elif page == "About":
    show_about()
else:
    # Fallback to dashboard if unknown
    show_dashboard()