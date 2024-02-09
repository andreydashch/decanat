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
        else:
            self.name = None


class UserRoles:
    def __init__(self, roles_list: [str]):
        self.user_roles = []

        for str_role in roles_list:
            self.user_roles.append(Role(str_role))

    def has_role(self, checked_role: Role):
        for role in self.user_roles:
            if compare_roles(role, checked_role):
                return True
        return False

    def has_intersection(self, checked_roles_list: [Role]):
        for checked_role in checked_roles_list:
            if self.has_role(checked_role):
                return True
        return False


def compare_roles(role_1: Role, role_2: Role):
    return role_1.name == role_2.name
