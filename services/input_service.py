import re


def input_non_empty(prompt: str) -> str:
    """
    Keeps asking until user enters non-empty input.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def input_int(prompt: str, min_value: int | None = None, max_value: int | None = None) -> int:
    """
    Keeps asking until valid integer (optionally within range).
    """
    while True:
        try:
            value = int(input(prompt).strip())

            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}.")
                continue

            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}.")
                continue

            return value

        except ValueError:
            print("Invalid integer. Please enter a valid number.")


def input_choice(prompt: str, choices: list[str]) -> str:
    """
    Forces user to select from allowed options.
    """
    choices_lower = [c.lower() for c in choices]

    while True:
        value = input(prompt).strip()

        if value.lower() in choices_lower:
            # Return original casing from choices
            return choices[choices_lower.index(value.lower())]

        print(f"Invalid choice. Allowed options: {', '.join(choices)}")


def input_student_id(prompt: str) -> str:
    """
    Ensures student ID is not empty and matches format like S001.
    """
    pattern = r"^S\d{3}$"   # Example: S001, S123

    while True:
        value = input(prompt).strip()

        if not value:
            print("Student ID cannot be empty.")
            continue

        if not re.match(pattern, value):
            print("Invalid format. Student ID must look like S001.")
            continue

        return value


def input_subject_name(prompt: str) -> str:
    """
    Subject must not be empty.
    """
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Subject name cannot be empty.")

# Invalid Input Conversion
def input_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("❌ Invalid number. Please enter a valid numeric value.")