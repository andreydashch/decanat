from entities.student import Student
from repository.db_conection import Conn
from repository.encripter.encripter import encrypt, decrypt

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

        birth_date=encrypt(student.birth_date),
        birth_place=encrypt(student.birth_place),
        citizenship=encrypt(student.citizenship),
        family_state=encrypt(student.family_state),
        idcard=encrypt(student.idcard),

        phone_number=encrypt(student.phone_number),
        home_address=encrypt(student.home_address),
        registration_address=encrypt(student.registration_address),

        faculty=encrypt(student.faculty),
        education_level=encrypt(student.education_level),
        education_form=encrypt(student.education_form),
        speciality=encrypt(student.speciality),
        education_program=encrypt(student.education_program),

        admission_benefits=encrypt(student.admission_benefits),
        enrolment_order_number=encrypt(student.enrolment_order_number),
        enrolment_order_date=encrypt(student.enrolment_order_date),

        school_name=encrypt(student.school_name),
        school_graduation_date=encrypt(student.school_graduation_date)
    )

    return conn.exec_sql(sql)


def get_students_by_group(group):
    sql = ("SELECT id, name, email, enable_status, std_group FROM student "
           "WHERE std_group = '{group}';").format(
        group=group
    )

    res = conn.exec_select_sql(sql)

    decrypt_res_list = []
    for student_index in range(len(res)):
        decrypt_res = list(res[student_index][0:5])
        for el_index in range(len(res[student_index]) - 5):
            decrypt_res.append(decrypt(res[student_index][el_index + 5]))
        decrypt_res_list.append(decrypt_res)

    return decrypt_res_list


def get_student_by_id(id):
    sql = ("SELECT * FROM student "
           "WHERE id = '{id}';").format(
        id=id
    )

    res = conn.exec_select_sql(sql)[0]

    decrypt_res = list(res[0:5])
    for el_index in range(len(res) - 5):
        decrypt_res.append(decrypt(res[el_index + 5]))

    return decrypt_res


def update_student(student):
    sql = ("UPDATE student SET name='{name}', email='{email}', enable_status='{enable_status}', std_group='{group}',"
           "birth_date='{birth_date}', birth_place='{birth_place}', citizenship='{citizenship}', family_state='{family_state}', idcard='{idcard}',"
           "phone_number='{phone_number}', home_address='{home_address}', registration_address='{registration_address}',"
           "faculty='{faculty}', education_level='{education_level}', education_form='{education_form}', speciality='{speciality}', education_program='{education_program}',"
           "admission_benefits='{admission_benefits}', enrolment_order_number='{enrolment_order_number}', enrolment_order_date='{enrolment_order_date}',"
           "school_name='{school_name}', school_graduation_date='{school_graduation_date}'"
           " WHERE id={id}").format(
        name=student.name,
        email=student.email,
        enable_status=student.enable_status,
        group=student.group,
        id=student.id,

        birth_date=encrypt(student.birth_date),
        birth_place=encrypt(student.birth_place),
        citizenship=encrypt(student.citizenship),
        family_state=encrypt(student.family_state),
        idcard=encrypt(student.idcard),

        phone_number=encrypt(student.phone_number),
        home_address=encrypt(student.home_address),
        registration_address=encrypt(student.registration_address),

        faculty=encrypt(student.faculty),
        education_level=encrypt(student.education_level),
        education_form=encrypt(student.education_form),
        speciality=encrypt(student.speciality),
        education_program=encrypt(student.education_program),

        admission_benefits=encrypt(student.admission_benefits),
        enrolment_order_number=encrypt(student.enrolment_order_number),
        enrolment_order_date=encrypt(student.enrolment_order_date),

        school_name=encrypt(student.school_name),
        school_graduation_date=encrypt(student.school_graduation_date)
    )

    return conn.exec_sql(sql)


def get_student_by_email(email):
    sql = ("SELECT * FROM student "
           "WHERE email = '{email}';").format(
        email=email
    )

    res = conn.exec_select_sql(sql)[0]

    decrypt_res = list(res[0:5])
    for el_index in range(len(res) - 5):
        decrypt_res.append(decrypt(res[el_index + 5]))

    return decrypt_res
