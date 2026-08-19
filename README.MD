# Student Performance Analytics

An interactive student performance analytics dashboard built with **Python, SQL, Pandas, Plotly, and Streamlit**.

The application allows users to store student marks in a SQL database, calculate academic performance, filter student records, and visualize performance through an interactive dashboard.

## Live Demo

[Launch Student Performance Analytics] (https://student-performance-analytics-system-bngxfkwazsnxtmw9mnaxrh.streamlit.app/)

## Features

* Add and store student performance records
* SQLite database integration
* Automatic total and average calculation
* Automatic grade classification
* Pass/fail status calculation
* Interactive performance dashboard
* Subject-wise performance visualization
* Grade distribution visualization
* Top performer analysis
* Student search functionality
* Grade and status filters
* Individual student performance analysis
* Interactive Plotly charts
* Responsive Streamlit interface

## Tech Stack

| Technology | Purpose                               |
| ---------- | ------------------------------------- |
| Python     | Application logic and data processing |
| SQLite     | Student data storage                  |
| SQL        | Database operations                   |
| Pandas     | Data analysis and manipulation        |
| Plotly     | Interactive data visualization        |
| Streamlit  | Web application interface             |

## Project Structure

```text
student-performance-analytics/
│
├── app.py
├── analytics.py
├── database.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How It Works

The application follows a simple data flow:

```text
User
  ↓
Streamlit Interface
  ↓
Python Application Logic
  ↓
SQLite Database
  ↓
Performance Analytics
  ↓
Interactive Dashboard
```

Student records contain:

* Student ID
* Student Name
* Python Marks
* SQL Marks
* Aptitude Marks

The application calculates:

```text
Total = Python + SQL + Aptitude

Average = Total / 3
```

Grades are assigned based on the calculated average, and students are classified as either **Pass** or **Fail**.

## Dashboard

The dashboard provides an overview of student performance through:

* Total number of students
* Class average
* Highest total score
* Overall pass rate
* Subject performance comparison
* Grade distribution
* Top performers
* Student performance comparison

## Student Management

The Students section allows users to:

* Search students by name
* Filter students by grade
* Filter students by pass/fail status
* View complete student records
* Select individual students
* Analyze subject-wise performance

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/student-performance-analytics.git
```

Navigate to the project directory:

```bash
cd student-performance-analytics
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## Database

The project uses **SQLite** for persistent local data storage.

The database file is automatically created when the application runs.

The database is excluded from version control using `.gitignore`.

## Future Improvements

Planned improvements include:

* Update student records
* Delete student records
* CSV import and export
* Student authentication
* Advanced analytics
* Performance trend analysis
* Admin dashboard
* Cloud database integration
* Deployment on Streamlit Community Cloud

## Learning Outcomes

This project demonstrates practical experience with:

* Python application development
* SQL and relational databases
* CRUD database operations
* Data analysis with Pandas
* Interactive visualization with Plotly
* Streamlit application development
* Git and GitHub workflow
* Dashboard development

## Author

**Sai Vivek**

Computer Science & Engineering Student

GitHub: https://github.com/viveksai1700-del

## License

This project is available for educational and portfolio purposes.
