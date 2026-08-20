import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    create_database,
    add_student,
    get_students,
    update_student,
    delete_student,
    get_subjects,
    add_subject,
    delete_subject,
)
from analytics import calculate_performance


st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

create_database()

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


subjects = get_subjects()
students = get_students()
results = calculate_performance(students)

subject_names = [subject[1] for subject in subjects]

if results:
    df = pd.DataFrame(results)
else:
    df = pd.DataFrame(
        columns=["ID", "Name", *subject_names, "Total", "Average", "Grade", "Status"]
    )


with st.sidebar:
    st.title("Student Analytics")
    st.caption("Customizable Academic Dashboard")

    st.divider()

    page = st.radio(
        "Navigation",
        ["Dashboard", "Students", "Add Student", "Manage Subjects"],
    )

    st.divider()

    st.caption("Academic Performance System")
    st.write(
        "Manage subjects, student records, and academic performance."
    )


st.title("Student Performance Analytics")
st.caption(
    "A professional academic analytics dashboard powered by Python and SQL."
)

st.divider()


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
                    "Subject": subject_names,
                    "Average": [
                        df[subject].mean() if subject in df.columns else 0
                        for subject in subject_names
                    ],
                }
            )

            fig = px.bar(
                subject_data,
                x="Subject",
                y="Average",
                text_auto=".1f",
                title="Average Marks by Subject",
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
            )

            fig.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font=dict(color="#1E293B"),
            )

            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.subheader("Top Performers")

        top_students = df.sort_values(
            "Average", ascending=False
        ).head(5)

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
                subject
                for subject in subject_names
                if subject in df.columns
            ] + ["Status"],
            title="Average Score by Student",
        )

        fig.update_layout(
            yaxis_range=[0, 100],
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(color="#1E293B"),
        )

        st.plotly_chart(fig, use_container_width=True)


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

        st.write(f"Showing **{len(filtered_df)}** student(s)")

        display_columns = [
            "ID",
            "Name",
            *subject_names,
            "Total",
            "Average",
            "Grade",
            "Status",
        ]

        st.dataframe(
            filtered_df[
                [column for column in display_columns if column in filtered_df.columns]
            ],
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
                st.metric("Average", f"{student['Average']:.1f}")

            with col2:
                st.metric("Grade", student["Grade"])

            with col3:
                st.metric("Status", student["Status"])

            st.write("### Subject Scores")

            for subject in subject_names:
                score = student.get(subject, 0)
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

            selected_record = next(
                item for item in students
                if item["id"] == int(student["ID"])
            )

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

                    edited_marks = {}

                    for subject_id, subject_name in subjects:
                        edited_marks[subject_id] = st.number_input(
                            f"{subject_name} Marks",
                            min_value=0,
                            max_value=100,
                            value=int(
                                selected_record["marks"].get(
                                    subject_name, 0
                                )
                            ),
                            step=1,
                        )

                    update_button = st.form_submit_button(
                        "Save Changes",
                        use_container_width=True,
                    )

                    if update_button:

                        if not edited_name.strip():
                            st.error("Student name cannot be empty.")
                        else:
                            update_student(
                                int(student["ID"]),
                                edited_name.strip(),
                                edited_marks,
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


elif page == "Add Student":

    st.header("Add New Student")

    if not subjects:
        st.warning(
            "No subjects are configured. "
            "Go to 'Manage Subjects' and add at least one subject."
        )
    else:
        st.caption(
            "Enter the student's academic performance below."
        )

        with st.form("student_form"):

            name = st.text_input(
                "Student Name",
                placeholder="Enter student name",
            )

            marks = {}

            for subject_id, subject_name in subjects:
                marks[subject_id] = st.number_input(
                    f"{subject_name} Marks",
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
                    add_student(name.strip(), marks)

                    st.success(
                        f"{name.strip()} added successfully!"
                    )

                    st.rerun()


elif page == "Manage Subjects":

    st.header("Manage Subjects")

    st.caption(
        "Schools can create and manage the subjects used in their "
        "student performance records."
    )

    st.subheader("Add Subject")

    with st.form("add_subject_form"):
        new_subject = st.text_input(
            "Subject Name",
            placeholder="e.g. Mathematics",
        )

        add_subject_button = st.form_submit_button(
            "Add Subject",
            use_container_width=True,
        )

        if add_subject_button:
            if not new_subject.strip():
                st.error("Subject name cannot be empty.")
            elif add_subject(new_subject.strip()):
                st.success(
                    f"Subject '{new_subject.strip()}' added successfully."
                )
                st.rerun()
            else:
                st.error(
                    "That subject already exists."
                )

    st.divider()

    st.subheader("Saved Subjects")

    current_subjects = get_subjects()

    if not current_subjects:
        st.info("No subjects have been added yet.")
    else:
        for subject_id, subject_name in current_subjects:
            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"**{subject_name}**")

            with col2:
                if len(current_subjects) == 1:
                    st.caption("Keep 1+")
                else:
                    if st.button(
                        "Delete",
                        key=f"delete_subject_{subject_id}",
                        use_container_width=True,
                    ):
                        delete_subject(subject_id)
                        st.success(
                            f"Subject '{subject_name}' deleted."
                        )
                        st.rerun()

        st.info(
            "Deleting a subject removes its marks from student records. "
            "This action cannot be undone."
        )
