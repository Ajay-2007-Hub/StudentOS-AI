# StudentOS-AI

StudentOS-AI is a personal student productivity assistant built using Python, Streamlit, and SQLite.

It helps students manage tasks, create study plans, chat with PDF notes, track learning progress, and analyze skill gaps.

## Features

- Dashboard for progress overview
- Task Manager with deadline, category, priority, and status tracking
- Study Planner for exam preparation
- Document Chat for PDF-based question answering
- Skill Gap Analyzer for career preparation
- Learning Log for daily study tracking

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- PyPDF

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
Project Goal

The goal of StudentOS-AI is to help students organize their academic work, improve productivity, and track learning progress in one simple application.

## Live Demo

[Click here to view StudentOS-AI](https://studentos-ai-jjz6pw7naavacre5gwptts.streamlit.app/)

Author

Ajay R V
B.Tech Artificial Intelligence and Data Science
 
## UI Update (June 2026)

- Modern, clean dashboard UI with a Home page and sidebar navigation.
- Custom CSS, theme selector, font options, responsive layout, and feature cards.
- KPI summary cards on the Dashboard (tasks due soon, avg study hours, completion).

## Running (recommended)

Create a virtual environment, install dependencies and run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app uses a Streamlit theme config at `.streamlit/config.toml` and custom styles in `assets/styles.css`.
