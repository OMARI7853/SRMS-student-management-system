class Student:
    def __init__(self, student_id: str, full_name: str, class_name: str, year: int) -> None:
        self.student_id = student_id
        self.full_name = full_name
        self.class_name = class_name
        self.year = year

    def to_dict(self) -> dict:
        """
        Convert Student object into JSON-safe dictionary.
        """
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "class_name": self.class_name,
            "year": self.year
        }

    @staticmethod
    def from_dict(data: dict) -> "Student":
        """
        Reconstruct Student object from dictionary (JSON data).
        """
        return Student(
            student_id=data["student_id"],
            full_name=data["full_name"],
            class_name=data["class_name"],
            year=data["year"]
        )

    def __str__(self) -> str:
        """
        Human-readable representation of Student.
        """
        return (
            f"ID: {self.student_id} | "
            f"Name: {self.full_name} | "
            f"Class: {self.class_name} | "
            f"Year: {self.year}"
        )