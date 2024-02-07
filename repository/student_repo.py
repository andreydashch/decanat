from entities.student import Student
from repository.db_conection import Conn

conn = Conn()


def save_student(student: Student) -> bool:

    sql = ("INSERT INTO student(name, email, enable_status, std_group,"
           "birth_date, birth_place, citizenship, family_state, idcard,"
           "phone_number, home_address, registration_address,"
           "faculty, education_level, education_form, speciality, education_program,"
           "admission_benefits, enrolment_order_number, enrolment_order_date,"
           "school_name, school_graduation_date)"
           "VALUES('{name}', '{email}', '{enable_status}', '{group}',"
           "'{birth_date}', '{birth_place}', '{citizenship}', '{family_state}', '{idcard}',"
           "'{phone_number}', '{home_address}', '{registration_address}',"
           "'{faculty}', '{education_level}', '{education_form}', '{speciality}', '{education_program}',"
           "'{admission_benefits}', '{enrolment_order_number}', '{enrolment_order_date}',"
           "'{school_name}', '{school_graduation_date}');").format(
        name=student.name,
        email=student.email,
        enable_status=student.enable_status,
        group=student.group,

        birth_date=student.birth_date,
        birth_place=student.birth_place,
        citizenship=student.citizenship,
        family_state=student.family_state,
        idcard=student.idcard,

        phone_number=student.phone_number,
        home_address=student.home_address,
        registration_address=student.registration_address,

        faculty=student.faculty,
        education_level=student.education_level,
        education_form=student.education_form,
        speciality=student.speciality,
        education_program=student.education_program,

        admission_benefits=student.admission_benefits,
        enrolment_order_number=student.enrolment_order_number,
        enrolment_order_date=student.enrolment_order_date,

        school_name=student.school_name,
        school_graduation_date=student.school_graduation_date
    )

    return conn.exec_sql(sql)


def get_students_by_group(group):
    sql = ("SELECT id, name, email, enable_status, std_group FROM student "
           "WHERE std_group = '{group}';").format(
        group=group
    )

    return conn.exec_select_sql(sql)


def get_student_by_id(id):
    sql = ("SELECT id, name, email, enable_status, std_group FROM student "
           "WHERE id = '{id}';").format(
        id=id
    )

    return conn.exec_select_sql(sql)[0]


def update_student(student):
    sql = ("UPDATE student SET name='{name}', email='{email}',"
           " enable_status='{enable_status}', std_group='{group}' WHERE id={id}").format(
        name=student.name,
        email=student.email,
        enable_status=student.enable_status,
        group=student.group,
        id=student.id
    )

    return conn.exec_sql(sql)
