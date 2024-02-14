import os
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, current_user, login_required, logout_user
from auth import authorization
from auth.authorization import GoogleUser
from entities.user_role import RolesList, TEST_ROlE, ADMIN_ROLE, STUDENT_ROLE, TEACHER_ROLE
from services import studnet_service
from services.user_service import get_user_by_flask_current_user

app = Flask(__name__)


app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)


def auth_check_for_role(roles):
    if not current_user.is_authenticated:
        abort(404)

    user = get_user_by_flask_current_user(current_user)

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
        user = get_user_by_flask_current_user(current_user)

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
        'admin/add_student.html',
        data={"user": user},
        is_confirm=is_confirm
    )


@app.route('/search_student', methods=['POST', 'GET'])
def search():
    user = auth_check_for_role([TEST_ROlE])

    group = request.args.get("group")
    students = studnet_service.get_students_by_group(group)

    return render_template(
        'admin/search_student.html',
        data={"user": user},
        students_list=students
    )


@app.route('/students_list', methods=['POST', 'GET'])
def students_list():
    user = auth_check_for_role([TEST_ROlE])

    group = request.args.get("group")
    students = studnet_service.get_students_by_group(group)

    return render_template(
        'admin/students_list.html',
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
        'admin/update_student.html',
        data={"user": user},
        is_confirm=is_confirm,
        student=student
    )


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    user = auth_check_for_role([TEST_ROlE])
    is_confirm = False
    return render_template(
        'admin/add_user.html',
        data={"user": user},
        is_confirm=is_confirm
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
