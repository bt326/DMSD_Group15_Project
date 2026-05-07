# Research Lab Manager

## Overview
Research Lab Manager is a Python Tkinter desktop application connected with PostgreSQL database.  
It helps manage:

- Projects
- Lab Members
- Equipment
- Usage Tracking
- Reports & Analytics

The application also includes:
- Animated GIF background
- Interactive UI
- Popup-based reports
- Database integration using psycopg2

---

## Technologies Used

- Python
- Tkinter
- PostgreSQL
- psycopg2
- Pillow (PIL)

---

## Features

### Projects & Members
- Add Project
- Update Project
- Delete Project
- View Projects
- Add Members
- Update Members
- Delete Members
- Project Status
- Grant-based Member Search
- Mentorship Details

### Equipment
- Add Equipment
- Update Equipment
- Delete Equipment
- Track Equipment Usage
- Equipment Status

### Reports
- Top Funded Projects
- Top Mentor
- Publications by Major
- Projects Before Given Date
- Top Publication Years

---

## Installation

### 1. Clone Repository

```bash
git clone <your-github-repo-link>
cd <repo-name>


2. Install Dependencies
pip install pillow psycopg2-binary


3. Configure PostgreSQL

Create database:

CREATE DATABASE lab_management;

Update PostgreSQL credentials inside app.py:

conn = psycopg2.connect(
    host="localhost",
    database="lab_management",
    user="postgres",
    password="Postgres"
)
Run Application
python app.py
GitHub Actions

This project uses GitHub Actions for automatic workflow checks.

Workflow file location:

.github/workflows/main.yml
Project Structure
project-folder/
│
├── app.py
├── lab.gif
├── README.md
└── .github/
    └── workflows/
        └── main.yml