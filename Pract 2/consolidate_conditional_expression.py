# Код до рефакторингу
class User:
    def __init__(self, login, status,valid):
        self.name = login
        self.status = status
        self.valid = valid

class UserManager:
    def notify_user(self, user):
        if user.valid:
            if user.status == 'admin':
                print(f"Notify {user.login}: You are admin.")
            elif user.status == 'editor':
                print(f"Notify {user.login}: You can edit posts.")
            elif user.status == 'viewer':
                print(f"Notify {user.login}: You are viewer.")
        else:
            print(f"Notify {user.login}: Your account is inactive.")

class User:
    def __init__(self, login, status, valid):
        self.name = login
        self.status = status
        self.valid = valid

# Код після рефакторингу
class UserManager:
    def notify_user(self, user):
        if user.valid:
            message = self.get_role_message(user)
            print(f"Notify {user.login}: {message}")
        else:
            print(f"Notify {user.login}: Your account is inactive.")

    def get_role_message(self, user):
        role_messages = {
            'admin': "You are admin.",
            'editor': "You can edit posts.",
            'viewer': "You are viewer."
        }
        return role_messages.get(user.status, "Role not recognized.")