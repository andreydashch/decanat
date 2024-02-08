from entities.student import Student
from repository import student_repo


def create_student(form) -> Student:
    name = form.get("name")
    email = form.get("email")
    group = form.get("group")
    student = Student(name, email, True, group)

    student.birth_date = form.get("birth_date")
    student.birth_place = form.get("birth_place")
    student.citizenship = form.get("citizenship")
    student.family_state = form.get("family_state")
    student.idcard = form.get("idcard")

    student.phone_number = form.get("phone_number")
    student.home_address = form.get("home_address")
    student.registration_address = form.get("registration_address")

    student.faculty = form.get("faculty")
    student.education_level = form.get("education_level")
    student.education_form = form.get("education_form")
    student.speciality = form.get("speciality")
    student.education_program = form.get("education_program")

    student.admission_benefits = form.get("admission_benefits")
    student.enrolment_order_number = form.get("enrolment_order_number")
    student.enrolment_order_date = form.get("enrolment_order_date")

    student.school_name = form.get("school_name")
    student.school_graduation_date = form.get("school_graduation_date")

    return student


def save_student(student: Student) -> bool:
    return student_repo.save_student(student)


def get_students_by_group(group) -> [Student]:
    students = []
    if group is not None:
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
