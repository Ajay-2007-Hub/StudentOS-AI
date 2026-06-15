import streamlit as st
from datetime import date
from database.db import get_connection


def generate_plan(subject, exam_date, study_hours, difficulty):
    today = date.today()
    days_left = (exam_date - today).days

    if days_left <= 0:
        days_left = 1

    if difficulty == "Hard":
        focus = "Spend more time on concepts, practice problems, and revision."
    elif difficulty == "Medium":
        focus = "Study concepts first, then practice important questions."
    else:
        focus = "Revise basics and solve simple questions."

    plan = f"""
Subject: {subject}

Days Left: {days_left}
Daily Study Hours: {study_hours}
Difficulty: {difficulty}

Study Plan:
1. Study {subject} for {study_hours} hour(s) every day.
2. First complete important topics.
3. Make short notes while studying.
4. Practice questions daily.
5. Revise all topics before the exam.

Focus:
{focus}
"""
    return plan


def save_study_plan(subject, exam_date, study_hours, difficulty, plan):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO study_plans (subject, exam_date, study_hours, difficulty, plan)
        VALUES (?, ?, ?, ?, ?)
    """, (subject, str(exam_date), study_hours, difficulty, plan))

    conn.commit()
    conn.close()


def get_study_plans():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM study_plans")
    plans = cursor.fetchall()

    conn.close()
    return plans


def show_study_planner():
    st.title("📚 Study Planner")

    st.subheader("Create New Study Plan")

    subject = st.text_input("Subject Name")
    exam_date = st.date_input("Exam Date")
    study_hours = st.number_input("Available Study Hours Per Day", min_value=1, max_value=12)
    difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

    if st.button("Generate Study Plan"):
        if subject:
            plan = generate_plan(subject, exam_date, study_hours, difficulty)
            save_study_plan(subject, exam_date, study_hours, difficulty, plan)
            st.success("Study plan generated and saved successfully!")
            st.text_area("Generated Study Plan", plan, height=300)
        else:
            st.warning("Please enter a subject name.")

    st.subheader("Saved Study Plans")

    plans = get_study_plans()

    if plans:
        for plan_data in plans:
            plan_id, subject, exam_date, study_hours, difficulty, plan = plan_data

            st.write(f"### {subject}")
            st.write(f"**Exam Date:** {exam_date}")
            st.write(f"**Study Hours:** {study_hours}")
            st.write(f"**Difficulty:** {difficulty}")
            st.text_area("Plan", plan, height=250, key=f"plan_{plan_id}")
            st.divider()
    else:
        st.info("No study plans created yet.")