def calculate_performance(students):
    results = []

    for student in students:
        student_id, name, python, sql, aptitude = student

        total = python + sql + aptitude
        average = total / 3

        if average >= 90:
            grade = "A+"
        elif average >= 80:
            grade = "A"
        elif average >= 70:
            grade = "B"
        elif average >= 60:
            grade = "C"
        elif average >= 50:
            grade = "D"
        else:
            grade = "F"

        status = "Pass" if average >= 40 else "Fail"

        results.append({
            "ID": student_id,
            "Name": name,
            "Python": python,
            "SQL": sql,
            "Aptitude": aptitude,
            "Total": total,
            "Average": round(average, 2),
            "Grade": grade,
            "Status": status
        })

    return results