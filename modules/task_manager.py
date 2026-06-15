import streamlit as st
import streamlit as st
from database.db import get_connection


def add_task(task_name, deadline, category, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (task_name, deadline, category, priority, status)
        VALUES (?, ?, ?, ?, ?)
    """, (task_name, deadline, category, priority, "Pending"))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()
    return tasks


def update_status(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )

    conn.commit()
    conn.close()


def show_task_manager():
    st.title("✅ Task Manager")

    st.subheader("Add New Task")

    task_name = st.text_input("Task Name")
    deadline = st.date_input("Deadline")
    category = st.selectbox(
        "Category",
        ["Study", "Project", "Internship", "Personal"]
    )
    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"]
    )

    if st.button("Add Task"):
        if task_name:
            add_task(task_name, str(deadline), category, priority)
            st.success("Task added successfully!")
            st.rerun()
        else:
            st.warning("Please enter a task name.")

    st.subheader("Your Tasks")

    tasks = get_tasks()

    if tasks:
        for task in tasks:
            task_id, task_name, deadline, category, priority, status = task

            st.write(f"### {task_name}")
            st.write(f"**Deadline:** {deadline}")
            st.write(f"**Category:** {category}")
            st.write(f"**Priority:** {priority}")
            st.write(f"**Status:** {status}")

            new_status = st.selectbox(
                "Update Status",
                ["Pending", "Completed"],
                index=0 if status == "Pending" else 1,
                key=f"status_{task_id}"
            )

            if new_status != status:
                update_status(task_id, new_status)
                st.rerun()

            st.divider()
    else:
        st.info("No tasks added yet.")
