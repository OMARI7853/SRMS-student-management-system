class Record:
    def __init__(self, student_id: str) -> None:
        self.student_id = student_id
        self.marks: dict[str, int] = {}

    def set_mark(self, subject: str, mark: int) -> None:
        """
        Set or overwrite mark for a subject.
        """
        if not isinstance(mark, int):
            raise ValueError("Mark must be an integer.")

        if mark < 0 or mark > 100:
            raise ValueError("Mark must be between 0 and 100.")

        self.marks[subject] = mark  # Overwrites if exists

    def get_mark(self, subject: str) -> int | None:
        """
        Get mark for a subject. Returns None if subject not found.
        """
        return self.marks.get(subject)

    def get_subjects(self) -> list[str]:
        """
        Return list of subjects.
        """
        return list(self.marks.keys())

    def total(self) -> int:
        """
        Return total of all marks.
        """
        return sum(self.marks.values())

    def average(self) -> float:
        """
        Return average mark.
        Returns 0.0 if no marks exist.
        """
        if not self.marks:
            return 0.0

        return self.total() / len(self.marks)
    
# Test it
record = Record("S001")

record.set_mark("Math", 78)
record.set_mark("English", 66)

print(record.get_mark("Math"))        # 78
print(record.get_mark("English"))        # 66
print(record.get_subjects())          # ['Math', 'English']
print(record.total())                 # 144
print(record.average())               # 72.0

# If no marks
empty = Record("S002")
print(empty.average())  # 0.0