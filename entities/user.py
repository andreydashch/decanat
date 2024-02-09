from entities.user_role import RolesList, Role


class User:
    def __init__(self, name):
        self.name = name
        self.roles = RolesList(["test"])

        self.email = None
        self.google_name = None
        self.google_profile_pic = None

    def has_role(self, checked_role: Role):
        return self.roles.has_role(checked_role)

    def has_role_intersection(self, checked_roles_list: RolesList):
        return self.roles.has_intersection(checked_roles_list)
