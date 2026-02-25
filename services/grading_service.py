def grade_from_mark(mark: int) -> str:
    """
    Convert numeric mark (0–100) into letter grade.
    """
    if not isinstance(mark, (int, float)):
        raise ValueError("Mark must be a number.")

    if mark < 0 or mark > 100:
        raise ValueError("Mark must be between 0 and 100.")

    if mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "E"


def comment_from_grade(grade: str) -> str:
    """
    Return performance comment based on grade.
    """
    comments = {
        "A": "Excellent",
        "B": "Very Good",
        "C": "Good",
        "D": "Fair",
        "E": "Needs Improvement"
    }

    if grade not in comments:
        raise ValueError("Invalid grade.")

    return comments[grade]


def overall_grade_from_average(avg: float) -> str:
    """
    Convert average score to overall letter grade.
    Uses same grading boundaries.
    """
    return grade_from_mark(int(avg))