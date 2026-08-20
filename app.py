import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    create_database,
    add_student,
    get_students,
    update_student,
    delete_student,
)
from analytics import calculate_performance


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

create_database()


# =========================================================
# PROFESSIONAL UI STYLING
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    [data-testid="stSidebar"] {
        background-color: #0F172A;
    }

    [data-testid="stSidebar"] * {
        color: #E2E8F0;
    }

    [data-testid="stSidebar"] h1 {
        color: #FFFFFF;
        font-weight: 700;
    }

    [data-testid="stSidebar"] hr {
        border-color: #334155;
    }

    h1 {
        color: #0F172A;
        font-size: 2.5rem;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #0F172A;
        font-weight: 700;
    }

    h3 {
        color: #1E293B;
        font-weight: 650;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.10);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 500;
    }

    [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 750;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        padding: 0.65rem 1.2rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #1D4ED8;
        color: #FFFFFF;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    .stProgress > div > div > div > div {
        background-color: #2563EB;
    }

    hr {
        border-color: #E2E8F0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOAD DATA
# =========================================================

students = get_students()
results = calculate_performance(students)

if results:
    df = pd.DataFrame(results)
else:
    df = pd.DataFrame(
        columns=[
            "ID",
            "Name",
            "Python",
            "SQL",
            "Aptitude",
            "Total",
            "Average",
            "Grade",
            "Status",
        ]
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("Student Analytics")
    st.caption("Python + SQL Dashboard")

    st.divider()

    page = st.radio(
        "Navigation",
        ["Dashboard", "Students", "Add Student"],
    )

    st.divider()

    st.caption("Academic Performance System")
    st.write(
        "Manage student records and analyze "
        "academic performance."
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.title("Student Performance Analytics")
st.caption(
    "A professional academic analytics dashboard "
    "powered by Python and SQL."
)

st.divider()


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    if df.empty:
        st.info(
            "No student records available. "
            "Go to 'Add Student' to create your first record."
        )
    else:
        total_students = len(df)
        class_average = df["Average"].mean()
        highest_score = df["Total"].max()
        pass_rate = (df["Status"] == "Pass").mean() * 100

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Students", total_students)

        with col2:
            st.metric("Class Average", f"{class_average:.1f}")

        with col3:
            st.metric("Highest Total", highest_score)

        with col4:
            st.metric("Pass Rate", f"{pass_rate:.1f}%")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Subject Performance")

            subject_data = pd.DataFrame(
                {
                    "Subject": ["Python", "SQL", "Aptitude"],
                    "Average": [
                        df["Python"].mean(),
                        df["SQL"].mean(),
                        df["Aptitude"].mean(),
                    ],
                }
            )

            fig = px.bar(
                subject_data,
                x="Subject",
                y="Average",
                text_auto=".1f",
                title="Average Marks by Subject",
                color="Subject",
                color_discrete_sequence=[
                    "#2563EB",
                    "#0F766E",
                    "#7C3AED",
                ],
            )

            fig.update_layout(
                yaxis_range=[0, 100],
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font=dict(color="#1E293B"),
                showlegend=False,
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Grade Distribution")

            grade_data = df["Grade"].value_counts().reset_index()
            grade_data.columns = ["Grade", "Students"]

            fig = px.pie(
                grade_data,
                names="Grade",
                values="Students",
                hole=0.48,
                title="Student Grade Distribution",
                color_discrete_sequence=[
                    "#2563EB",
                    "#0F766E",
                    "#7C3AED",
                    "#F59E0B",
                    "#EF4444",
                ],
            )

            fig.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font=dict(color="#1E293B"),
            )

            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.subheader("Top Performers")

        top_students = (
            df.sort_values("Average", ascending=False)
            .head(5)
        )

        st.dataframe(
            top_students[
                ["Name", "Total", "Average", "Grade", "Status"]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        st.subheader("Student Performance Comparison")

        fig = px.scatter(
            df,
            x="Name",
            y="Average",
            size="Total",
            color="Grade",
            hover_data=[
                "Python",
                "SQL",
                "Aptitude",
                "Status",
            ],
            title="Average Score by Student",
            color_discrete_sequence=[
                "#2563EB",
                "#0F766E",
                "#7C3AED",
                "#F59E0B",
                "#EF4444",
            ],
        )

        fig.update_layout(
            yaxis_range=[0, 100],
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(color="#1E293B"),
        )

        st.plotly_chart(fig, use_container_width=True)


# =========================================================
# STUDENTS PAGE
# =========================================================

elif page == "Students":

    st.header("Student Records")

    if df.empty:
        st.info("No students have been added yet.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            search = st.text_input(
                "Search Student",
                placeholder="Enter student name...",
            )

        with col2:
            grade_filter = st.selectbox(
                "Filter by Grade",
                ["All"] + sorted(df["Grade"].unique().tolist()),
            )

        with col3:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Pass", "Fail"],
            )

        filtered_df = df.copy()

        if search:
            filtered_df = filtered_df[
                filtered_df["Name"].str.contains(
                    search,
                    case=False,
                    na=False,
                )
            ]

        if grade_filter != "All":
            filtered_df = filtered_df[
                filtered_df["Grade"] == grade_filter
            ]

        if status_filter != "All":
            filtered_df = filtered_df[
                filtered_df["Status"] == status_filter
            ]

        st.write(
            f"Showing **{len(filtered_df)}** student(s)"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )

        st.divider()

        st.subheader("Student Performance")

        if filtered_df.empty:
            st.warning("No students match your filters.")
        else:
            selected_student = st.selectbox(
                "Select a student",
                filtered_df["Name"].tolist(),
            )

            student = filtered_df[
                filtered_df["Name"] == selected_student
            ].iloc[0]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Average",
                    f"{student['Average']:.1f}",
                )

            with col2:
                st.metric("Grade", student["Grade"])

            with col3:
                st.metric("Status", student["Status"])

            st.write("### Subject Scores")

            subjects = {
                "Python": student["Python"],
                "SQL": student["SQL"],
                "Aptitude": student["Aptitude"],
            }

            for subject, score in subjects.items():
                st.write(f"**{subject}: {score}/100**")
                st.progress(int(score))

            st.divider()

            st.subheader("Manage Student")

            action = st.radio(
                "Choose an action",
                ["Update Student", "Delete Student"],
                horizontal=True,
            )

            st.divider()

            if action == "Update Student":

                st.write(
                    f"Editing **{student['Name']}** "
                    f"(Student ID: **{int(student['ID'])}**)"
                )

                with st.form("edit_student_form"):

                    edited_name = st.text_input(
                        "Student Name",
                        value=student["Name"],
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        edited_python = st.number_input(
                            "Python Marks",
                            min_value=0,
                            max_value=100,
                            value=int(student["Python"]),
                            step=1,
                        )

                    with col2:
                        edited_sql = st.number_input(
                            "SQL Marks",
                            min_value=0,
                            max_value=100,
                            value=int(student["SQL"]),
                            step=1,
                        )

                    with col3:
                        edited_aptitude = st.number_input(
                            "Aptitude Marks",
                            min_value=0,
                            max_value=100,
                            value=int(student["Aptitude"]),
                            step=1,
                        )

                    update_button = st.form_submit_button(
                        "Save Changes",
                        use_container_width=True,
                    )

                    if update_button:

                        if not edited_name.strip():
                            st.error(
                                "Student name cannot be empty."
                            )

                        elif (
                            edited_name.strip() == student["Name"]
                            and edited_python == int(student["Python"])
                            and edited_sql == int(student["SQL"])
                            and edited_aptitude == int(student["Aptitude"])
                        ):
                            st.info(
                                "No changes were made to this student."
                            )

                        else:
                            update_student(
                                int(student["ID"]),
                                edited_name.strip(),
                                edited_python,
                                edited_sql,
                                edited_aptitude,
                            )

                            st.success(
                                f"Student '{edited_name.strip()}' "
                                "updated successfully."
                            )

                            st.rerun()

            else:

                st.warning(
                    f"You are about to permanently delete "
                    f"**{student['Name']}** "
                    f"(Student ID: **{int(student['ID'])}**)."
                )

                st.write(
                    "This action cannot be undone and the student's "
                    "record will be removed from the database."
                )

                confirm_delete = st.checkbox(
                    "I understand that this action cannot be undone."
                )

                delete_button = st.button(
                    "Delete Student Permanently",
                    type="primary",
                    use_container_width=True,
                    disabled=not confirm_delete,
                )

                if delete_button:

                    delete_student(int(student["ID"]))

                    st.success(
                        f"Student '{student['Name']}' "
                        "was deleted successfully."
                    )

                    st.rerun()


# =========================================================
# ADD STUDENT PAGE
# =========================================================

elif page == "Add Student":

    st.header("Add New Student")

    st.caption(
        "Enter the student's academic performance below."
    )

    with st.form("student_form"):

        name = st.text_input(
            "Student Name",
            placeholder="Enter student name",
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            python_marks = st.number_input(
                "Python Marks",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
            )

        with col2:
            sql_marks = st.number_input(
                "SQL Marks",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
            )

        with col3:
            aptitude_marks = st.number_input(
                "Aptitude Marks",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
            )

        st.divider()

        submitted = st.form_submit_button(
            "Add Student",
            use_container_width=True,
        )

        if submitted:
            if not name.strip():
                st.error("Please enter a student name.")
            else:
                add_student(
                    name.strip(),
                    python_marks,
                    sql_marks,
                    aptitude_marks,
                )

                st.success(
                    f"{name} added successfully!"
                )

                st.rerun()