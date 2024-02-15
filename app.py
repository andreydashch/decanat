import os
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, current_user, login_required, logout_user
from auth import authorization
from auth.authorization import GoogleUser
from entities.user_role import RolesList, TEST_ROlE, ADMIN_ROLE, STUDENT_ROLE, TEACHER_ROLE, Role
from services import studnet_service, grades_service
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
        user = auth_check_for_role([ADMIN_ROLE, STUDENT_ROLE, TEACHER_ROLE])

        if user.has_role_intersection(RolesList([ADMIN_ROLE])):
            return redirect(url_for("search"))
        elif user.has_role_intersection(RolesList([TEACHER_ROLE])):
            return redirect(url_for("teacher_search_credit"))
        elif user.has_role_intersection(RolesList([STUDENT_ROLE])):
            return redirect(url_for("account"))
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
    user = auth_check_for_role([ADMIN_ROLE])

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
    user = auth_check_for_role([ADMIN_ROLE])

    group = request.args.get("group")
    students = studnet_service.get_students_by_group(group)

    return render_template(
        'admin/student/search_student.html',
        data={"user": user},
        students_list=students
    )


@app.route('/update_student', methods=['POST', 'GET'])
def update_student():
    user = auth_check_for_role([ADMIN_ROLE])

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
    user = auth_check_for_role([ADMIN_ROLE])

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
    user = auth_check_for_role([ADMIN_ROLE])

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
    user = auth_check_for_role([ADMIN_ROLE])

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


@app.route('/add_credit', methods=['POST', 'GET'])
def add_credit():
    user = auth_check_for_role([ADMIN_ROLE])

    is_confirm = False
    if request.method == "POST":
        teacher = user_service.get_user_by_email(request.form.get("teacher_email"))
        if teacher.has_role(TEACHER_ROLE):
            new_credit = grades_service.create_credit(request.form, teacher.db_id)
            is_confirm = grades_service.save_credit(new_credit)

            print(is_confirm)

    return render_template(
        'admin/teacher/add_credit.html',
        data={"user": user},
        is_confirm=is_confirm
    )


@app.route('/search_credit', methods=['POST', 'GET'])
def search_credit():
    user = auth_check_for_role([ADMIN_ROLE])
    group = request.args.get("group")

    if group is None:
        credits_list = grades_service.get_all_credits()
    else:
        credits_list = grades_service.get_credits_by_group(group)

    return render_template(
        'admin/teacher/search_credit.html',
        data={"user": user},
        credits_list=credits_list
    )


@app.route('/update_credit', methods=['POST', 'GET'])
def update_credit():
    user = auth_check_for_role([ADMIN_ROLE])

    is_confirm = False
    credit_id = request.args.get("credit_id")
    credit = grades_service.get_credit_by_id(credit_id)
    teacher = user_service.get_user_by_id(credit.teacher_id)

    if credit.is_closed:
        return redirect(url_for("admin_show_closed_credit", credit_id=credit_id))

    if request.args.get("delete") == "true":
        if grades_service.del_credit_by_id(credit_id):
            return redirect(url_for("search_credit"))

    if request.method == "POST":
        if teacher.has_role(TEACHER_ROLE):
            credit = grades_service.create_credit(request.form, teacher.db_id)
            credit.id = credit_id

            is_confirm = grades_service.update_credit(credit)

        print(is_confirm)

    return render_template(
        'admin/teacher/update_credit.html',
        data={"user": user},
        is_confirm=is_confirm,
        credit=credit,
        teacher_email=teacher.email
    )


@app.route('/show_closed_credit', methods=['POST', 'GET'])
def admin_show_closed_credit():
    user = auth_check_for_role([ADMIN_ROLE])

    credit = grades_service.get_credit_by_id(request.args.get("credit_id"))
    teacher = user_service.get_user_by_id(credit.teacher_id)

    students_list = studnet_service.get_students_by_group(credit.group)
    grades_dict = grades_service.get_grades_by_credit(credit)

    return render_template(
        'admin/teacher/show_closed_credit.html',
        data={"user": user},
        students_list=students_list,
        credit=credit,
        grades_dict=grades_dict,
        teacher_email=teacher.email
    )


@app.route('/teacher/search_credit', methods=['POST', 'GET'])
def teacher_search_credit():
    user = auth_check_for_role([TEACHER_ROLE])
    group = request.args.get("group")

    if group is None:
        credits_list = grades_service.get_credits_by_teacher(user.db_id)
    else:
        credits_list = grades_service.get_credits_by_group_and_teacher(group, user.db_id)

    return render_template(
        'teacher/search_credit.html',
        data={"user": user},
        credits_list=credits_list
    )


@app.route('/give_rating', methods=['POST', 'GET'])
def give_rating():
    user = auth_check_for_role([TEACHER_ROLE])
    credit = grades_service.get_credit_by_id(request.args.get("credit_id"))

    if user.db_id != credit.teacher_id:
        abort(404)
    if credit.is_closed:
        return redirect(url_for("show_rating", credit_id=credit.id))

    students_list = studnet_service.get_students_by_group(credit.group)

    is_confirm = False

    if request.method == "POST":
        is_confirm = grades_service.save_grades(request.form, credit, students_list)
        credit.is_closed = True
        print(is_confirm)

    if credit.is_closed:
        return redirect(url_for("show_rating", credit_id=credit.id))

    return render_template(
        'teacher/give_rating.html',
        data={"user": user},
        students_list=students_list,
        credit=credit,
        is_confirm=is_confirm
    )


@app.route('/show_rating', methods=['POST', 'GET'])
def show_rating():
    user = auth_check_for_role([TEACHER_ROLE])
    credit = grades_service.get_credit_by_id(request.args.get("credit_id"))

    students_list = studnet_service.get_students_by_group(credit.group)
    grades_dict = grades_service.get_grades_by_credit(credit)

    return render_template(
        'teacher/show_rating.html',
        data={"user": user},
        students_list=students_list,
        credit=credit,
        grades_dict=grades_dict
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


@app.route('/grades', methods=['POST', 'GET'])
def grades():
    user = auth_check_for_role([STUDENT_ROLE])
    student = studnet_service.get_student_by_email(user.email)

    term_dct = {}
    teacher_dct = {}
    for grade in grades_service.get_grades_by_student_id(student.id):
        if grade.credit.term not in term_dct.keys():
            term_dct[grade.credit.term] = []
        term_dct[grade.credit.term].append(grade)

        teacher = user_service.get_user_by_id(grade.credit.teacher_id)
        teacher_dct[grade.credit.teacher_id] = teacher.name

    term_list = list(term_dct.keys())
    term_list.sort()
    return render_template(
        'student/grades.html',
        data={"user": user},
        term_list=term_list,
        term_dct=term_dct,
        teacher_dct=teacher_dct
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(401)
def page_not_found(error):
    return render_template('errors/unknown_user.html'), 401


if __name__ == '__main__':
    app.run(ssl_context=('static/certificate/cert.pem', 'static/certificate/key.pem'))
