import streamlit as st
from datetime import date
from database.db import get_connection


def generate_revision_suggestion(subject, topics, confidence):
    if confidence <= 2:
        return f"Revise the basics of {subject}. Focus more on: {topics}"
    elif confidence == 3:
        return f"Practice more questions in {subject}. Revise: {topics}"
    else:
        return f"You are confident in {subject}. Do a quick revision of: {topics}"


def save_learning_log(log_date, subject, topics, confidence, revision_suggestion):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO learning_logs 
        (log_date, subject, topics, confidence, revision_suggestion)
        VALUES (?, ?, ?, ?, ?)
    """, (str(log_date), subject, topics, confidence, revision_suggestion))

    conn.commit()
    conn.close()


def get_learning_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM learning_logs ORDER BY id DESC")
    logs = cursor.fetchall()

    conn.close()
    return logs


def show_learning_log():
    st.title("📝 Learning Log")

    st.subheader("Add Today's Learning")

    log_date = st.date_input("Date", date.today())
    subject = st.text_input("Subject")
    topics = st.text_area("Topics Learned Today")
    confidence = st.slider("Confidence Level", 1, 5, 3)

    if st.button("Save Learning Log"):
        if subject and topics:
            revision_suggestion = generate_revision_suggestion(
                subject,
                topics,
                confidence
            )

            save_learning_log(
                log_date,
                subject,
                topics,
                confidence,
                revision_suggestion
            )

            st.success("Learning log saved successfully!")
            st.info(revision_suggestion)
            st.rerun()
        else:
            st.warning("Please enter subject and topics.")

    st.subheader("Saved Learning Logs")

    logs = get_learning_logs()

    if logs:
        for log in logs:
            log_id, log_date, subject, topics, confidence, suggestion = log

            st.write(f"### {subject}")
            st.write(f"**Date:** {log_date}")
            st.write(f"**Topics:** {topics}")
            st.write(f"**Confidence:** {confidence}/5")
            st.info(f"Revision Suggestion: {suggestion}")
            st.divider()
    else:
        st.info("No learning logs added yet.")