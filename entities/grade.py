class Credit:
    def __init__(self, id, teacher_id, term, date, subject, is_closed, group):
        self.id = id
        self.teacher_id = teacher_id
        self.term = term
        self.date = date
        self.subject = subject
        self.is_closed = is_closed
        self.group = group


class Grade:
    def __init__(self, credit: Credit, student_id, grade_amount):
        self.id = None
        self.credit = credit
        self.credit_id = credit.id
        self.student_id = student_id
        self.grade_amount = grade_amount

