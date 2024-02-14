class Role:
    def __init__(self, str_role: str):
        self.name = None
        self.set_role(str_role)

    def set_role(self, str_role: str):
        str_role = str_role.upper()
        if str_role == "ADMIN":
            self.name = "Admin"
        elif str_role == "STUDENT":
            self.name = "Student"
        elif str_role == "TEACHER":
            self.name = "Teacher"
        elif str_role == "TEST":
            self.name = "Test"
        else:
            self.name = None
            print("Unsupported role: " + str_role)


class RolesList:
    def __init__(self, roles_list: [str] or [Role]):
        self.user_roles = []

        for str_role in roles_list:
            if isinstance(str_role, Role):
                added_role = str_role
            else:
                added_role = Role(str_role)
            self.user_roles.append(added_role)

    def add_role(self, role: Role):
        if not self.has_role(role):
            self.user_roles.append(role)

    def has_role(self, checked_role: Role):
        for role in self.user_roles:
            if compare_roles(role, checked_role):
                return True
        return False

    def has_intersection(self, checked_roles_list):
        for checked_role in checked_roles_list.user_roles:
            if self.has_role(checked_role):
                return True
        return False

    def get_roles_strings(self) -> [str]:
        roles_strings = []

        for role in self.user_roles:
            roles_strings.append(role.name)

        return roles_strings


def compare_roles(role_1: Role, role_2: Role):
    if role_1.name is None:
        return False
    return role_1.name == role_2.name


ADMIN_ROLE = Role("admin")
TEST_ROlE = Role("test")
STUDENT_ROLE = Role("student")
TEACHER_ROLE = Role("teacher")
