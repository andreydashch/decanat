class Student:
    id = None

    def __init__(self, name, email, enable_status, group):
        self.name = name
        self.email = email
        self.enable_status = enable_status
        self.group = group

        self.birth_date = None
        self.birth_place = None
        self.citizenship = None
        self.family_state = None
        self.idcard = None

        self.phone_number = None
        self.home_address = None
        self.registration_address = None

        self.faculty = None
        self.education_level = None
        self.education_form = None
        self.speciality = None
        self.education_program = None

        self.admission_benefits = None
        self.enrolment_order_number = None
        self.enrolment_order_date = None

        self.school_name = None
        self.school_graduation_date = None
