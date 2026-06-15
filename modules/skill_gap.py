import streamlit as st
from database.db import get_connection


role_skills = {
    "AI Developer": ["Python", "Machine Learning", "Deep Learning", "NLP", "Data Analysis"],
    "Data Analyst": ["Excel", "SQL", "Python", "Power BI", "Statistics"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "GitHub"],
    "Java Developer": ["Java", "OOP", "SQL", "Spring Boot", "GitHub"],
    "Software Developer": ["Python", "Java", "DSA", "SQL", "GitHub"]
}


def analyze_skills(target_role, current_skills):
    required_skills = role_skills.get(target_role, [])

    current_skills_list = [
        skill.strip().lower()
        for skill in current_skills.split(",")
    ]

    strong_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in current_skills_list:
            strong_skills.append(skill)
        else:
            missing_skills.append(skill)

    if missing_skills:
        suggestions = "Learn these skills next: " + ", ".join(missing_skills)
    else:
        suggestions = "Great! You have the basic skills for this role."

    return strong_skills, missing_skills, suggestions


def save_skill_gap(target_role, current_skills, missing_skills, strong_skills, suggestions):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO skill_gaps 
        (target_role, current_skills, missing_skills, strong_skills, suggestions)
        VALUES (?, ?, ?, ?, ?)
    """, (
        target_role,
        current_skills,
        ", ".join(missing_skills),
        ", ".join(strong_skills),
        suggestions
    ))

    conn.commit()
    conn.close()


def get_skill_gaps():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM skill_gaps ORDER BY id DESC")
    gaps = cursor.fetchall()

    conn.close()
    return gaps


def show_skill_gap():
    st.title("🎯 Skill Gap Analyzer")

    st.subheader("Analyze Your Skills")

    target_role = st.selectbox(
        "Target Role",
        [
            "AI Developer",
            "Data Analyst",
            "Web Developer",
            "Java Developer",
            "Software Developer"
        ]
    )

    current_skills = st.text_area(
        "Enter Your Current Skills",
        placeholder="Example: Python, SQL, GitHub"
    )

    if st.button("Analyze Skill Gap"):
        if current_skills:
            strong_skills, missing_skills, suggestions = analyze_skills(
                target_role,
                current_skills
            )

            save_skill_gap(
                target_role,
                current_skills,
                missing_skills,
                strong_skills,
                suggestions
            )

            st.success("Skill gap analysis completed!")

            st.write("### Strong Skills")
            st.write(", ".join(strong_skills) if strong_skills else "No matching skills found.")

            st.write("### Missing Skills")
            st.write(", ".join(missing_skills) if missing_skills else "No missing skills.")

            st.info(suggestions)
            st.rerun()
        else:
            st.warning("Please enter your current skills.")

    st.subheader("Saved Skill Gap Results")

    gaps = get_skill_gaps()

    if gaps:
        for gap in gaps:
            gap_id, target_role, current_skills, missing_skills, strong_skills, suggestions = gap

            st.write(f"### {target_role}")
            st.write(f"**Current Skills:** {current_skills}")
            st.write(f"**Strong Skills:** {strong_skills}")
            st.write(f"**Missing Skills:** {missing_skills}")
            st.info(suggestions)
            st.divider()
    else:
        st.info("No skill gap analysis saved yet.")