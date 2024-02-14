import os
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, current_user, login_required, logout_user
from auth import authorization
from auth.authorization import GoogleUser
from entities.user_role import RolesList, TEST_ROlE, ADMIN_ROLE, STUDENT_ROLE, TEACHER_ROLE, Role
from services import studnet_service
from services import user_service

app = Flask(__name__)


app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)


def auth_check_for_role(roles):
    if not current_user.is_authenticated:
        abort(404)

    user = user_service.get_user_by_flask_current_user(current_user)

    if user.name is None:
        logout_user()
        abort(401)

    roles = RolesList(roles)
    if not user.has_role_intersection(roles):
        abort(404)

    return user


@login_manager.user_loader
def load_user(user_id):
    return GoogleUser.get(user_id)


@app.route('/', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated:
        user = user_service.get_user_by_flask_current_user(current_user)

        if user.has_role_intersection(RolesList([ADMIN_ROLE])):
            return redirect(url_for("search"))
        elif user.has_role_intersection(RolesList([STUDENT_ROLE])):
            return redirect(url_for("account"))
        else:
            return "TODO"
    else:
        return render_template('login.html')


@app.route("/login")
def login():
    return authorization.login()


@app.route("/login/callback")
def callback():
    return authorization.login_callback()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    user = auth_check_for_role([TEST_ROlE])

    is_confirm = False
    if request.method == "POST":
        student = studnet_service.create_student(request.form)
        is_confirm = studnet_service.save_student(student)
        print(is_confirm)

    return render_template(
        'admin/student/add_student.html',
        data={"user": user},
        is_confirm=is_confirm
    )


@app.route('/search_student', methods=['POST', 'GET'])
def search():
    user = auth_check_for_role([TEST_ROlE])

    group = request.args.get("group")
    students = studnet_service.get_students_by_group(group)

    return render_template(
        'admin/student/search_student.html',
        data={"user": user},
        students_list=students
    )


@app.route('/update_student', methods=['POST', 'GET'])
def update_student():
    user = auth_check_for_role([TEST_ROlE])

    is_confirm = False
    std_id = request.args.get("id")

    if request.method == "POST":
        student = studnet_service.create_student(request.form)
        student.id = std_id
        is_confirm = studnet_service.update_student(student)
        print(is_confirm)

    student = studnet_service.get_student_by_id(std_id)

    return render_template(
        'admin/student/update_student.html',
        data={"user": user},
        is_confirm=is_confirm,
        student=student
    )


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    user = auth_check_for_role([TEST_ROlE])

    is_confirm = False
    if request.method == "POST":
        new_user = user_service.create_user(request.form)
        is_confirm = user_service.save_user(new_user)

        print(is_confirm)

    return render_template(
        'admin/user/add_user.html',
        data={"user": user},
        is_confirm=is_confirm
    )


@app.route('/search_user', methods=['POST', 'GET'])
def search_user():
    user = auth_check_for_role([TEST_ROlE])

    users = []
    role = request.args.get("role")
    if role is not None:
        role = Role(role)
        if role.name is not None:
            users = user_service.get_users_by_role(role)

    return render_template(
        'admin/user/search_user.html',
        data={"user": user},
        users_list=users
    )


@app.route('/update_user', methods=['POST', 'GET'])
def update_user():
    user = auth_check_for_role([TEST_ROlE])

    is_confirm = False
    user_id = request.args.get("id")
    old_user = user_service.get_user_by_id(user_id)

    if request.method == "POST":
        upd_user = user_service.create_user(request.form)
        upd_user.db_id = user_id

        if old_user.has_role(STUDENT_ROLE):
            upd_user.roles.add_role(STUDENT_ROLE)
            upd_user.email = old_user.email

        is_confirm = user_service.update_user(upd_user)

        print(is_confirm)

    upd_user = user_service.get_user_by_id(user_id)

    return render_template(
        'admin/user/update_user.html',
        data={"user": user},
        is_confirm=is_confirm,
        upd_user=upd_user,
        str_roles=' '.join(upd_user.roles.get_roles_strings())
    )


@app.route('/give_rating', methods=['POST', 'GET'])
def give_rating():
    user = auth_check_for_role([TEST_ROlE])
    students_list = studnet_service.get_students_by_group("211")
    return render_template(
        'admin/teacher/give_rating.html',
        data={"user": user},
        students_list=students_list
    )


@app.route('/account', methods=['POST', 'GET'])
def account():
    user = auth_check_for_role([STUDENT_ROLE])

    student = studnet_service.get_student_by_email(user.email)
    return render_template(
        'student/student_account.html',
        data={"user": user},
        student=student
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(401)
def page_not_found(error):
    return render_template('errors/unknown_user.html'), 401


if __name__ == '__main__':
    app.run(ssl_context=('static/certificate/cert.pem', 'static/certificate/key.pem'))
