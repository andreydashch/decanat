from entities.user import User
from repository.db_conection import get_conn

conn = get_conn()


def save_user(user: User) -> bool:
    sql = ("WITH auth_user as ("
           "INSERT INTO auth_user(name, email)"
           "VALUES ('{name}', '{email}') RETURNING *"
           ")"
           "INSERT INTO auth_user_roles(user_id, role) "
           "VALUES ((select auth_user.id from auth_user), unnest(array[{roles}]));").format(
        name=user.name,
        email=user.email,
        roles=user.get_roles_strings()
    )

    return conn.exec_sql(sql)


def update_user(user: User) -> bool:
    sql = ("WITH auth_user as ("
           "UPDATE  auth_user SET name = '{name}', email = '{email}' WHERE id = {id}"
           "), del as ("
           "DELETE FROM auth_user_roles WHERE user_id = {id}"
           ") "
           "INSERT INTO auth_user_roles(user_id, role) "
           "VALUES ({id}, unnest(array[{roles}]));").format(
        name=user.name,
        id=user.db_id,
        email=user.email,
        roles=user.get_roles_strings()
    )

    return conn.exec_sql(sql)


def get_user_by_email(email) -> User:
    sql = ("SELECT auth_user.*, array_agg(DISTINCT auth_user_roles.role) "
           "FROM auth_user "
           "LEFT JOIN  auth_user_roles "
           "ON auth_user_roles.user_id = auth_user.id "
           "WHERE email = '{email}' "
           "GROUP BY auth_user.id;").format(
        email=email
    )

    res = conn.exec_select_sql(sql)

    if len(res) == 0:
        return None

    return res[0]

