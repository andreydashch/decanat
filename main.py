from flask import Flask, render_template, request
from services import studnet_service
from entities.user import User

app = Flask(__name__)
user = User("Дащик Андрій Сергійович")


@app.route('/', methods=['POST', 'GET'])
def main():

    return render_template(
        'index.html',
        data={"user": user}
    )


@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    is_confirm = False
    if request.method == "POST":
        student = studnet_service.create_student(request.form)
        is_confirm = studnet_service.save_student(student)
        print(is_confirm)

    return render_template(
        'add_student.html',
        data={"user": user},
        is_confirm=is_confirm
    )


@app.route('/search_student', methods=['POST', 'GET'])
def search():
    group = request.args.get("group")
    students = studnet_service.get_students_by_group(group)

    return render_template(
        'search_student.html',
        data={"user": user},
        students_list=students
    )


@app.route('/students_list', methods=['POST', 'GET'])
def students_list():
    group = request.args.get("group")
    students = studnet_service.get_students_by_group(group)

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

    return render_template(
        'update_student.html',
        data={"user": user},
        is_confirm=is_confirm,
        student=student
    )


if __name__ == '__main__':
    app.run()
