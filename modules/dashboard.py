import streamlit as st
import pandas as pd
import datetime
from database.db import get_connection


def get_dashboard_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
    completed_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Pending'")
    pending_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM study_plans")
    total_study_plans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM learning_logs")
    total_learning_logs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM skill_gaps")
    total_skill_gaps = cursor.fetchone()[0]

    cursor.execute("SELECT task_name, deadline, priority, status FROM tasks ORDER BY id DESC LIMIT 5")
    recent_tasks = cursor.fetchall()

    cursor.execute("SELECT subject, exam_date, difficulty FROM study_plans ORDER BY id DESC LIMIT 5")
    recent_study_plans = cursor.fetchall()

    cursor.execute("SELECT subject, confidence FROM learning_logs ORDER BY id DESC LIMIT 5")
    recent_learning_logs = cursor.fetchall()

    conn.close()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_study_plans": total_study_plans,
        "total_learning_logs": total_learning_logs,
        "total_skill_gaps": total_skill_gaps,
        "recent_tasks": recent_tasks,
        "recent_study_plans": recent_study_plans,
        "recent_learning_logs": recent_learning_logs
    }


def show_dashboard():
    st.title("📊 StudentOS-AI Dashboard")
    st.write("Overview of your tasks, study plans, skills, and learning progress.")

    data = get_dashboard_data()

    # KPI summary cards
    try:
        # Tasks due in the next 7 days
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT deadline FROM tasks WHERE deadline IS NOT NULL AND deadline != ''")
        deadlines = [row[0] for row in cursor.fetchall()]
        conn.close()

        today = datetime.date.today()
        due_soon = 0
        for d in deadlines:
            try:
                dt = datetime.date.fromisoformat(d)
                if 0 <= (dt - today).days <= 7:
                    due_soon += 1
            except Exception:
                continue

        # Average planned study hours per plan
        if data := get_dashboard_data():
            total_plans = data.get("total_study_plans", 0)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT AVG(study_hours) FROM study_plans")
            avg_hours = cursor.fetchone()[0] or 0
            conn.close()
        else:
            due_soon = 0
            avg_hours = 0

    except Exception:
        due_soon = 0
        avg_hours = 0

    k1, k2, k3, k4 = st.columns([1,1,1,1])
    k1.markdown(f"<div class='card'><div class='card-title'>Total Tasks</div><div class='card-desc'>{data['total_tasks']}</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='card'><div class='card-title'>Due Soon (7d)</div><div class='card-desc'>{due_soon}</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='card'><div class='card-title'>Avg Study Hours</div><div class='card-desc'>{round(avg_hours,1)} / day</div></div>", unsafe_allow_html=True)
    completion_pct = 0
    try:
        completion_pct = round((data['completed_tasks'] / data['total_tasks'] * 100) if data['total_tasks']>0 else 0,1)
    except Exception:
        completion_pct = 0
    k4.markdown(f"<div class='card'><div class='card-title'>Completion</div><div class='card-desc'>{completion_pct}%</div></div>", unsafe_allow_html=True)

    data = get_dashboard_data()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tasks", data["total_tasks"])
    col2.metric("Completed Tasks", data["completed_tasks"])
    col3.metric("Pending Tasks", data["pending_tasks"])

    col4, col5, col6 = st.columns(3)

    col4.metric("Study Plans", data["total_study_plans"])
    col5.metric("Learning Logs", data["total_learning_logs"])
    col6.metric("Skill Gap Results", data["total_skill_gaps"])

    st.divider()

    st.subheader("Task Progress")

    if data["total_tasks"] > 0:
        progress = data["completed_tasks"] / data["total_tasks"]
        st.progress(progress)
        st.write(f"Task Completion: {round(progress * 100, 2)}%")

        chart_data = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Count": [data["completed_tasks"], data["pending_tasks"]]
        })

        st.bar_chart(chart_data, x="Status", y="Count")
    else:
        st.info("No tasks added yet.")

    st.divider()

    st.subheader("Recent Tasks")

    if data["recent_tasks"]:
        for task in data["recent_tasks"]:
            task_name, deadline, priority, status = task

            st.write(f"### {task_name}")
            st.write(f"**Deadline:** {deadline}")
            st.write(f"**Priority:** {priority}")
            st.write(f"**Status:** {status}")
            st.divider()
    else:
        st.info("No recent tasks found.")

    st.subheader("Recent Study Plans")

    if data["recent_study_plans"]:
        for plan in data["recent_study_plans"]:
            subject, exam_date, difficulty = plan

            st.write(f"### {subject}")
            st.write(f"**Exam Date:** {exam_date}")
            st.write(f"**Difficulty:** {difficulty}")
            st.divider()
    else:
        st.info("No study plans found.")

    st.subheader("Recent Learning Logs")

    if data["recent_learning_logs"]:
        for log in data["recent_learning_logs"]:
            subject, confidence = log

            st.write(f"### {subject}")
            st.write(f"**Confidence:** {confidence}/5")
            st.divider()
    else:
        st.info("No learning logs found.")