from entities.grade import Grade, Credit
from repository import grades_repo


def get_credit_by_id(id):
    return _create_credit_from_raw(grades_repo.get_credit_by_id(id))


def _create_credit_from_raw(raw):
    credit = Credit(raw[0], raw[1], raw[2], raw[3], raw[4], raw[5], raw[6])

    return credit


def save_grades(form, credit, students_list):
    grades = []
    for student in students_list:
        grade = Grade(credit, student.id, form.get(str(student.id)))
        grades.append(grade)

    return grades_repo.save_grades(grades)


def get_grades_by_credit(credit):
    grades_raw = grades_repo.get_grades_by_credit(credit.id)

    grades_dict = {}

    for raw in grades_raw:
        grade = _create_grade_from_raw_without_credit(raw, credit)
        grades_dict[grade.student_id] = grade

    return grades_dict


def _create_grade_from_raw_without_credit(raw, credit):
    grade = Grade(credit, raw[2], raw[3])
    grade.id = raw[0]

    return grade


def create_credit(form, teacher_id):
    credit = Credit(None, teacher_id, form.get("term"), form.get("date"),
                    form.get("subject"), False, form.get("group"))

    return credit


def save_credit(new_credit):
    return grades_repo.save_credit(new_credit)


def get_all_credits():
    credits_list = []

    for raw in grades_repo.get_all_credits():
        credit = _create_credit_from_raw(raw)
        credits_list.append(credit)

    return credits_list


def get_credits_by_group(group):
    credits_list = []

    for raw in grades_repo.get_credits_by_group(group):
        credit = _create_credit_from_raw(raw)
        credits_list.append(credit)

    return credits_list


def update_credit(credit):
    return grades_repo.update_credit(credit)


def del_credit_by_id(credit_id):
    return grades_repo.del_credit_by_id(credit_id)