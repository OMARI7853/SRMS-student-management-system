from typing import List, Dict, Tuple
from models.student import Student
from models.record import Record

# Calculate One Student Average
def calculate_student_average(student_id: str, records: Dict[str, Record]) -> float:
    """
    Returns average for a specific student.
    If student has no record or no marks → 0.0
    """
    record = records.get(student_id)

    if not record or not record.marks:
        return 0.0

    return record.average()

# Rank Students (With Tie-Breakers)

# Rules:

# Higher average wins

# If equal → higher total wins

# If still equal → alphabetical by full_name

def rank_students(
    students: List[Student],
    records: Dict[str, Record]
) -> List[Tuple[Student, float]]:
    """
    Returns list sorted from highest average to lowest.
    Tie-breakers:
        1. Higher total marks
        2. Alphabetical by full_name
    """

    ranking_data = []

    for student in students:
        record = records.get(student.student_id)

        if record and record.marks:
            avg = record.average()
            total = record.total()
        else:
            avg = 0.0
            total = 0

        ranking_data.append((student, avg, total))

    # Sort with multiple criteria
    ranking_data.sort(
        key=lambda item: (
            -item[1],        # highest average first
            -item[2],        # highest total first
            item[0].full_name.lower()  # alphabetical
        )
    )

    # Return only (Student, average)
    return [(student, avg) for student, avg, _ in ranking_data]

# Subject Averages (Across Class)
def subject_averages(records: Dict[str, Record]) -> Dict[str, float]:
    """
    Returns average mark per subject across all students.
    """

    subject_totals: Dict[str, int] = {}
    subject_counts: Dict[str, int] = {}

    for record in records.values():
        for subject, mark in record.marks.items():
            subject_totals[subject] = subject_totals.get(subject, 0) + mark
            subject_counts[subject] = subject_counts.get(subject, 0) + 1

    subject_avg: Dict[str, float] = {}

    for subject in subject_totals:
        subject_avg[subject] = subject_totals[subject] / subject_counts[subject]

    return subject_avg

# Class Average
def class_average(
    students: List[Student],
    records: Dict[str, Record]
) -> float:
    """
    Returns average of student averages.
    Only includes students with at least one mark.
    """

    averages = []

    for student in students:
        record = records.get(student.student_id)

        if record and record.marks:
            averages.append(record.average())

    if not averages:
        return 0.0

    return sum(averages) / len(averages)