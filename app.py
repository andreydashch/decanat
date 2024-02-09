import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required, logout_user
from auth import authorization
from auth.authorization import GoogleUser
from services import studnet_service
from services.user_service import get_user_by_flask_current_user

app = Flask(__name__)


app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

"""
"<p>Hello, {}! You're logged in! Email: {}</p>"
"<div><p>Google Profile Picture:</p>"
'</div>'
'<a class="button" href="/logout">Logout</a>'.format(
    current_user.name, current_user.email, current_user.profile_pic
)
"""
@login_manager.user_loader
def load_user(user_id):
    return GoogleUser.get(user_id)


@app.route('/', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("search"))
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
    is_confirm = False
    if request.method == "POST":
        student = studnet_service.create_student(request.form)
        is_confirm = studnet_service.save_student(student)
        print(is_confirm)

    user = get_user_by_flask_current_user(current_user)
    return render_template(
        'add_student.html',
        data={"user": user},
        is_confirm=is_confirm
    )


@app.route('/search_student', methods=['POST', 'GET'])
def search():
    group = request.args.get("group")
    students = studnet_service.get_students_by_group(group)

    user = get_user_by_flask_current_user(current_user)
    return render_template(
        'search_student.html',
        data={"user": user},
        students_list=students
    )


@app.route('/students_list', methods=['POST', 'GET'])
def students_list():
    group = request.args.get("group")
    students = studnet_service.get_students_by_group(group)

    user = get_user_by_flask_current_user(current_user)
    return render_template(
        'students_list.html',
        data={"user": user},
        students_list=students
    )


@app.route('/update_student', methods=['POST', 'GET'])
def update_student():
    is_confirm = False
    id = request.args.get("id")
    print(id)
    if request.method == "POST":
        student = studnet_service.create_student(request.form)
        student.id = id
        is_confirm = studnet_service.update_student(student)
        print(is_confirm)

    student = studnet_service.get_student_by_id(id)
    print(student.name)

    user = get_user_by_flask_current_user(current_user)
    return render_template(
        'update_student.html',
        data={"user": user},
        is_confirm=is_confirm,
        student=student
    )


@app.route('/account', methods=['POST', 'GET'])
def account():
    is_confirm = False
    id = request.args.get("id")

    if request.method == "POST":
        student = studnet_service.create_student(request.form)
        student.id = id
        is_confirm = studnet_service.update_student(student)
        print(is_confirm)

    user = get_user_by_flask_current_user(current_user)

    student = studnet_service.get_student_by_email(user.email)
    return render_template(
        'update_student.html',
        data={"user": user},
        is_confirm=is_confirm,
        student=student
    )


if __name__ == '__main__':
    app.run(ssl_context=('static/certificate/cert.pem', 'static/certificate/key.pem'))
