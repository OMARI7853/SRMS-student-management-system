import json
import csv
import os
from typing import List, Dict

from models.student import Student
from models.record import Record


def ensure_data_files_exist(students_path: str, marks_path: str) -> None:
    """
    Creates empty students.json and marks.csv if they do not exist.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(students_path), exist_ok=True)

    # Create empty JSON file if missing
    if not os.path.exists(students_path):
        with open(students_path, "w") as f:
            json.dump([], f)

    # Create empty CSV file with header if missing
    if not os.path.exists(marks_path):
        with open(marks_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "subject", "mark"])

#Load Students (JSON → Objects)
def load_students(path: str) -> List[Student]:
    """
    Reads JSON and returns list of Student objects.
    If file missing or empty → returns [].
    """
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r") as f:
            data = json.load(f)

            if not data:
                return []

            return [Student.from_dict(item) for item in data]

    except (json.JSONDecodeError, FileNotFoundError):
        return []
    

# Save Students (Objects → JSON)
def save_students(path: str, students: List[Student]) -> None:
    """
    Writes list of students to JSON using to_dict().
    """
    with open(path, "w") as f:
        json.dump([s.to_dict() for s in students], f, indent=4)


# Load Records (CSV → Record Mapping)
def load_records(path: str) -> Dict[str, Record]:
    """
    Reads CSV and returns mapping:
        key: student_id
        value: Record
    """
    records: Dict[str, Record] = {}

    if not os.path.exists(path):
        return records

    try:
        with open(path, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                student_id = row["student_id"]
                subject = row["subject"]
                mark = int(row["mark"])

                if student_id not in records:
                    records[student_id] = Record(student_id)

                records[student_id].set_mark(subject, mark)

    except Exception:
        return {}

    return records

# Save Records (Record Mapping → CSV)
def save_records(path: str, records: Dict[str, Record]) -> None:
    """
    Writes CSV rows in exact format:
    student_id,subject,mark
    """
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)

        # Required header
        writer.writerow(["student_id", "subject", "mark"])

        for student_id, record in records.items():
            for subject, mark in record.marks.items():
                writer.writerow([student_id, subject, mark])

# File Read Errors (students.json, marks.csv)
# Safe JSON Loader (students.json) 
import json
import os

def load_students(filepath: str) -> dict:
    if not os.path.exists(filepath):
        print("⚠ students.json not found. Creating empty file.")
        return {}

    try:
        with open(filepath, "r") as f:
            if os.stat(filepath).st_size == 0:
                return {}  # file exists but empty

            return json.load(f)

    except json.JSONDecodeError:
        print("⚠ JSON file is corrupted. Starting with empty data.")
        return {}

    except Exception as e:
        print("⚠ Error reading students file:", e)
        return {}
    
# Safe JSON Saver
def save_students(filepath: str, data: dict):
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("⚠ Error saving students:", e)

# Invalid CSV Rows Handling
import csv

def load_marks(filepath: str) -> dict:
    records = {}

    if not os.path.exists(filepath):
        print("⚠ marks.csv not found.")
        return records

    try:
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    student_id = row["student_id"]
                    math = float(row["math"])
                    english = float(row["english"])
                    science = float(row["science"])

                    records[student_id] = {
                        "math": math,
                        "english": english,
                        "science": science
                    }

                except (ValueError, KeyError):
                    print("⚠ Skipping invalid CSV row:", row)
                    continue

    except Exception as e:
        print("⚠ Error reading CSV file:", e)

    return records