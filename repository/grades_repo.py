from repository.db_conection import get_conn

conn = get_conn()


def get_credit_by_id(id):
    sql = "SELECT * FROM credit WHERE id = {id};".format(
        id=id
    )

    res = conn.exec_select_sql(sql)

    if len(res) == 0:
        return None

    return res[0]


def save_grades(grades):
    student_ids = []
    grades_amounts = []
    credit_ids = []

    for grade in grades:
        credit_ids.append(grade.credit_id)
        student_ids.append(grade.student_id)
        grades_amounts.append(int(grade.grade_amount))

    sql = ("WITH grades as (INSERT INTO grades(credit_id, student_id, grade_amount) "
           "SELECT "
           "unnest(array[{credit_ids}]), "
           "unnest(array[{student_ids}]), "
           "unnest(array[{grades_amounts}]))"
           "UPDATE credit SET is_closed=true WHERE id={c_id}"
           ";"
           "").format(
        c_id=credit_ids[0],
        credit_ids=credit_ids,
        student_ids=student_ids,
        grades_amounts=grades_amounts
    )

    return conn.exec_sql(sql)


def get_grades_by_credit(credit_id):
    sql = "SELECT * FROM grades WHERE credit_id = {credit_id};".format(
        credit_id=credit_id
    )

    res = conn.exec_select_sql(sql)

    if len(res) == 0:
        return None

    return res
