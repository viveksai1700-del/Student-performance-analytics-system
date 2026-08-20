def calculate_performance(students):
    results = []

    for student in students:
        student_id = student["id"]
        name = student["name"]
        marks = student.get("marks", {})

        if marks:
            total = sum(marks.values())
            average = total / len(marks)
        else:
            total = 0
            average = 0

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

        result = {
            "ID": student_id,
            "Name": name,
            "Total": total,
            "Average": round(average, 2),
            "Grade": grade,
            "Status": status,
            "Marks": marks,
        }

        for subject, score in marks.items():
            result[subject] = score

        results.append(result)

    return results