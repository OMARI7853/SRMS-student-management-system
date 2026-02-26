import json
import csv
import os
from typing import List, Dict

from models.student import Student
from models.record import Record


def ensure_data_files_exist(students_path: str, marks_path: str) -> None:
    os.makedirs(os.path.dirname(students_path), exist_ok=True)

    if not os.path.exists(students_path):
        with open(students_path, "w") as f:
            json.dump([], f)

    if not os.path.exists(marks_path):
        with open(marks_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject", "mark"])


# =========================
# LOAD STUDENTS
# =========================

def load_students(path: str) -> List[Student]:
    if not os.path.exists(path):
        return []

    try:
        if os.stat(path).st_size == 0:
            return []

        with open(path, "r") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return []

        return [Student.from_dict(item) for item in data]

    except json.JSONDecodeError:
        print("⚠ JSON corrupted. Resetting students.")
        return []

    except Exception as e:
        print("⚠ Error loading students:", e)
        return []


# =========================
# SAVE STUDENTS
# =========================

def save_students(path: str, students: List[Student]) -> None:
    try:
        with open(path, "w") as f:
            json.dump([s.to_dict() for s in students], f, indent=4)
    except Exception as e:
        print("⚠ Error saving students:", e)


# =========================
# LOAD RECORDS
# =========================

def load_records(path: str) -> Dict[str, Record]:
    records: Dict[str, Record] = {}

    if not os.path.exists(path):
        return records

    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    student_id = row["student_id"]
                    subject = row["subject"]
                    mark = float(row["mark"])

                    if student_id not in records:
                        records[student_id] = Record(student_id)

                    records[student_id].set_mark(subject, mark)

                except (ValueError, KeyError):
                    print("⚠ Skipping invalid CSV row:", row)
                    continue

    except Exception as e:
        print("⚠ Error loading records:", e)

    return records


# =========================
# SAVE RECORDS
# =========================

def save_records(path: str, records: Dict[str, Record]) -> None:
    try:
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject", "mark"])

            for student_id, record in records.items():
                for subject, mark in record.marks.items():
                    writer.writerow([student_id, subject, mark])

    except Exception as e:
        print("⚠ Error saving records:", e)