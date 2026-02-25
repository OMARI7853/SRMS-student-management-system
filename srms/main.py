from models.student import Student
from models.record import Record

from services.input_service import (
    input_non_empty,
    input_int,
    input_student_id,
    input_subject_name,
    input_choice
)

from services.storage_service import (
    load_students,
    save_students,
    load_records,
    save_records,
    ensure_data_files_exist
)

from services.analytics_service import rank_students
from services.report_service import (
    build_student_report_text,
    export_student_report,
    export_class_summary
)

# File paths
STUDENTS_PATH = "data/students.json"
MARKS_PATH = "data/marks.csv"
REPORTS_DIR = "reports"

# Print Menu
def print_menu() -> None:
    print("\n====== SRMS MENU ======")
    print("1. Add Student")
    print("2. Add or Update Marks")
    print("3. View Student Report")
    print("4. View Ranking")
    print("5. Export Student Report")
    print("6. Export Class Summary")
    print("7. Search Student")
    print("0. Exit")

# Add Student
def handle_add_student(students: list[Student]) -> None:
    student_id = input_student_id("Enter Student ID (e.g., S001): ")

    # Prevent duplicate ID
    if any(s.student_id == student_id for s in students):
        print("Student ID already exists!")
        return

    full_name = input_non_empty("Enter Full Name: ")
    class_name = input_non_empty("Enter Class Name: ")
    year = input_int("Enter Year: ", 1900, 2100)

    student = Student(student_id, full_name, class_name, year)
    students.append(student)

    print("Student added successfully.")

# Add or Update Marks
def handle_add_or_update_marks(
    students: list[Student],
    records: dict[str, Record]
) -> None:

    student_id = input_student_id("Enter Student ID: ")

    if not any(s.student_id == student_id for s in students):
        print("Student not found.")
        return

    subject = input_subject_name("Enter Subject: ")
    mark = input_int("Enter Mark (0-100): ", 0, 100)

    if student_id not in records:
        records[student_id] = Record(student_id)

    records[student_id].set_mark(subject, mark)

    print("Mark saved successfully.")

# View Student Report
def handle_view_student_report(
    students: list[Student],
    records: dict[str, Record]
) -> None:

    student_id = input_student_id("Enter Student ID: ")

    student = next((s for s in students if s.student_id == student_id), None)

    if not student:
        print("Student not found.")
        return

    record = records.get(student_id)

    report_text = build_student_report_text(student, record)
    print("\n" + report_text)

# View Ranking
def handle_view_ranking(
    students: list[Student],
    records: dict[str, Record]
) -> None:

    ranked = rank_students(students, records)

    if not ranked:
        print("No ranking data available.")
        return

    print("\n--- Class Ranking ---")
    for idx, (student, avg) in enumerate(ranked, start=1):
        print(f"{idx}. {student.full_name} "
              f"(ID: {student.student_id}) - Avg: {avg:.2f}")
        
# Export Student Report
def handle_export_student_report(
    students: list[Student],
    records: dict[str, Record]
) -> None:

    student_id = input_student_id("Enter Student ID: ")

    student = next((s for s in students if s.student_id == student_id), None)

    if not student:
        print("Student not found.")
        return

    record = records.get(student_id)

    filepath = export_student_report(student, record, REPORTS_DIR)
    print(f"Report exported to: {filepath}")

# Export Class Summary
def handle_export_class_summary(
    students: list[Student],
    records: dict[str, Record]
) -> None:

    filepath = export_class_summary(students, records, REPORTS_DIR)
    print(f"Class summary exported to: {filepath}")

# Search Student
def handle_search_student(students: list[Student]) -> None:
    keyword = input_non_empty("Enter name keyword: ").lower()

    matches = [
        s for s in students
        if keyword in s.full_name.lower()
    ]

    if not matches:
        print("No matching students found.")
        return

    print("\nMatches:")
    for student in matches:
        print(student)

# Main Function

# Startup Requirements:
# Ensure files exist
# Load students
# Load records
# Run loop
# Save on exit

def main() -> None:

    # Ensure files exist
    ensure_data_files_exist(STUDENTS_PATH, MARKS_PATH)

    # Load data
    students = load_students(STUDENTS_PATH)
    records = load_records(MARKS_PATH)

    while True:
        print_menu()
        choice = input("Select option: ").strip()

        if choice == "1":
            handle_add_student(students)

        elif choice == "2":
            handle_add_or_update_marks(students, records)

        elif choice == "3":
            handle_view_student_report(students, records)

        elif choice == "4":
            handle_view_ranking(students, records)

        elif choice == "5":
            handle_export_student_report(students, records)

        elif choice == "6":
            handle_export_class_summary(students, records)

        elif choice == "7":
            handle_search_student(students)

        elif choice == "0":
            # Save before exit
            save_students(STUDENTS_PATH, students)
            save_records(MARKS_PATH, records)
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid choice.")

# Entry Point
if __name__ == "__main__":
    main()

# Safe Main Entry (Never Crash)
# def main():
#     try:
#         run_program()
#     except Exception as e:
#         print("⚠ Unexpected system error:", e)
#         print("System will continue running.")