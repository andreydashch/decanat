from entities.student import Student
from repository import student_repo


def create_student(form) -> Student:
    name = form.get("name")
    email = form.get("email")
    group = form.get("group")

    return Student(name, email, True, group)


def save_student(student: Student) -> bool:
    return student_repo.save_student(student)


def get_students_by_group(group) -> [Student]:
    students = []
    for raw in student_repo.get_students_by_group(group):
        students.append(_create_student_from_raw(raw))

    return students


def _create_student_from_raw(raw):
    student = Student(raw[1], raw[2], raw[3], raw[4])
    student.id = raw[0]

    return student


def get_student_by_id(id) -> Student:
    return _create_student_from_raw(student_repo.get_student_by_id(id))


def update_student(student: Student) -> bool:
    return student_repo.update_student(student)
