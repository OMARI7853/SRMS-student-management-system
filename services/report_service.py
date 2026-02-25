import os
from typing import List, Dict
from models.student import Student
from models.record import Record
from services.analytics_service import (
    calculate_student_average,
    rank_students,
    subject_averages,
    class_average
)
from services.grading_service import (
    grade_from_mark,
    comment_from_grade,
    overall_grade_from_average
)

# Build Student Report Text
def build_student_report_text(student: Student, record: Record | None) -> str:
    """
    Returns formatted multi-line string for a single student.
    """

    lines = []
    lines.append("STUDENT REPORT")
    lines.append("=" * 40)
    lines.append(f"Student ID : {student.student_id}")
    lines.append(f"Name       : {student.full_name}")
    lines.append(f"Class      : {student.class_name}")
    lines.append(f"Year       : {student.year}")
    lines.append("-" * 40)

    if not record or not record.marks:
        lines.append("No marks available.")
        return "\n".join(lines)

    for subject, mark in record.marks.items():
        grade = grade_from_mark(mark)
        comment = comment_from_grade(grade)

        lines.append(
            f"{subject:<15} Mark: {mark:<3} Grade: {grade} ({comment})"
        )

    lines.append("-" * 40)

    avg = record.average()
    overall_grade = overall_grade_from_average(avg)

    lines.append(f"Total   : {record.total()}")
    lines.append(f"Average : {avg:.2f}")
    lines.append(f"Overall Grade : {overall_grade}")

    return "\n".join(lines)

# Export Student Report
def export_student_report(
    student: Student,
    record: Record | None,
    output_dir: str
) -> str:
    """
    Writes report_<student_id>.txt
    Returns filepath created.
    """

    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(
        output_dir,
        f"report_{student.student_id}.txt"
    )

    content = build_student_report_text(student, record)

    with open(filepath, "w") as f:
        f.write(content)

    return filepath

# Build Class Summary Text

# Must include:
# Class average
# Top 3 students
# Subject averages

def build_class_summary_text(
    students: List[Student],
    records: Dict[str, Record]
) -> str:
    """
    Builds class summary report.
    """

    lines = []
    lines.append("CLASS SUMMARY REPORT")
    lines.append("=" * 50)

    # Class Average
    cls_avg = class_average(students, records)
    lines.append(f"Class Average: {cls_avg:.2f}")
    lines.append("-" * 50)

    # Top 3 Students
    lines.append("Top 3 Students:")
    ranked = rank_students(students, records)[:3]

    if not ranked:
        lines.append("No ranking data available.")
    else:
        for idx, (student, avg) in enumerate(ranked, start=1):
            lines.append(
                f"{idx}. {student.full_name} "
                f"(ID: {student.student_id}) "
                f"- Avg: {avg:.2f}"
            )

    lines.append("-" * 50)

    # Subject Averages
    lines.append("Subject Averages:")
    subj_avg = subject_averages(records)

    if not subj_avg:
        lines.append("No subject data available.")
    else:
        for subject, avg in subj_avg.items():
            lines.append(f"{subject:<15} {avg:.2f}")

    return "\n".join(lines)

# Export Class Summary
def export_class_summary(
    students: List[Student],
    records: Dict[str, Record],
    output_dir: str
) -> str:
    """
    Writes class_summary.txt
    Returns filepath created.
    """

    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, "class_summary.txt")

    content = build_class_summary_text(students, records)

    with open(filepath, "w") as f:
        f.write(content)

    return filepath