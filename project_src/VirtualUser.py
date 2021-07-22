class VirtualUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def set_admin(self):
        self.username = "admin"
        self.password = "root"

    def set_sample_user(self):
        self.username = "sample_user"
        self.password = "123456abc"

class AllVirtualUsers:
    def __init__(self):
        self.users_ls = []

    def setup_virtual_users(self):
        for i in range(0, 30):
            username = "rot" + str(i)
            password = 'password' + str(i)
            new_user = VirtualUser(username, password)
            self.users_ls.append(new_user)
