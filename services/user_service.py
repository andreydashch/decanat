from entities.user import User
from entities.user_role import RolesList
from repository import user_repo


def get_user_by_flask_current_user(current_user):
    user = get_user_by_email(current_user.email)

    user.google_email = current_user.email
    user.google_profile_pic = current_user.profile_pic

    return user


def get_user_by_email(email):
    raw = user_repo.get_user_by_email(email)

    if raw is None:
        return User(None)

    return _create_user_from_raw(raw)


def _create_user_from_raw(raw):
    user = User(raw[1])

    user.db_id = raw[0]
    user.email = raw[2]
    user.roles = RolesList(raw[3])

    return user


def create_user(form) -> User:
    name = form.get("name")
    email = form.get("email")
    roles = form.get("roles")
    roles = roles.split(" ")

    user = User(name)
    user.email = email
    user.roles = RolesList(roles)

    return user


def save_user(new_user):
    return user_repo.save_user(new_user)


def get_users_by_role(role):
    user_list = []
    for user_raw in user_repo.get_users_by_role(role.name):
        user_list.append(_create_user_from_raw(user_raw))

    return user_list


def update_user(upd_user):
    return user_repo.update_user(upd_user)


def get_user_by_id(id):
    raw = user_repo.get_user_by_id(id)

    if raw is None:
        return User(None)

    return _create_user_from_raw(raw)
