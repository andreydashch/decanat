from entities.user import User


def get_user_by_flask_current_user(current_user):
    user = get_user_by_email(current_user.email)

    user.name = current_user.name
    user.google_email = current_user.email
    user.google_profile_pic = current_user.profile_pic

    return user


def get_user_by_email(email):
    user = User("Дащик Андрій Сергійович")
    user.email = email

    return user
