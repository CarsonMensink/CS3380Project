import streamlit as st
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME", "university_database.db")

# Connect to SQLite database
conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
cursor = conn.cursor()

# Page title
st.title("University Course Enrollment System")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Choose a Function",
    [
        "Home",
        "Search Course Sections",
        "Register for Course",
        "View Enrollments and Grades"
    ]
)

# Home page
if menu == "Home":

    st.header("Welcome")

    st.write("""
    This application allows users to:

    - Search course sections
    - Register students for courses
    - View enrollments and grades
    """)

# Search Course Sections
elif menu == "Search Course Sections":

    st.header("Search Course Sections")

    course_id = st.number_input("Course ID", min_value=1, step=1)

    semester = st.selectbox(
        "Semester",
        ["Spring", "Fall"]
    )

    year = st.number_input(
        "Year",
        min_value=2025,
        max_value=2026,
        step=1
    )

    if st.button("Search"):
        # MY SEARCH COURSE SECTIONS QUERY
        query = """
        SELECT
            s.section_id,
            c.course_number,
            c.course_title,
            s.section_number,
            s.semester,
            s.year,
            i.first_name || ' ' || i.last_name AS instructor
        FROM Section s
        JOIN Course c
            ON s.course_id = c.course_id
        JOIN Instructor i
            ON s.instructor_id = i.instructor_id
        WHERE s.course_id = ?
          AND s.semester = ?
          AND s.year = ?;
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(course_id, semester, year)
        )

        st.dataframe(df)

# Register for Course
elif menu == "Register for Course":

    st.header("Register Student")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    section_id = st.number_input(
        "Section ID",
        min_value=1,
        step=1
    )

    if st.button("Register"):

        try:
          
            cursor.execute("""
            INSERT INTO Enrollment (
                student_id,
                section_id,
                grade
            )
            VALUES (?, ?, NULL);
            """, (student_id, section_id))

            conn.commit()

            st.success("Student registered successfully.")

        except Exception as error:

            st.error(f"Error: {error}")

# View Enrollments and Grades
elif menu == "View Enrollments and Grades":

    st.header("View Enrollments and Grades")

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    if st.button("View"):

        query = """
        SELECT
            st.student_id,
            st.first_name || ' ' || st.last_name AS student_name,
            c.course_number,
            c.course_title,
            c.credits,
            sec.semester,
            sec.year,
            e.grade
        FROM Enrollment e
        JOIN Student st
            ON e.student_id = st.student_id
        JOIN Section sec
            ON e.section_id = sec.section_id
        JOIN Course c
            ON sec.course_id = c.course_id
        WHERE st.student_id = ?;
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(student_id,)
        )

        st.dataframe(df)