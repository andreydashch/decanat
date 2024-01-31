from entities.student import Student
from repository.db_conection import Conn

conn = Conn()


def save_student(student: Student) -> bool:

    sql = ("INSERT INTO student(name, email, enable_status, std_group)"
           "VALUES('{name}', '{email}', '{enable_status}', '{group}');").format(
        name=student.name,
        email=student.email,
        enable_status=student.enable_status,
        group=student.group
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
