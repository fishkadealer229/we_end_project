from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, username, db):
        self.__user = db.getUser(username)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['username'])

    def get_name(self):
        return str(self.__user['name_surname'])

    def get_pass(self):
        return str(self.__user['password'])

    def get_gender(self):
        return str(self.__user['gender'])

    def get_prof(self):
        return str(self.__user['profession'])

    def get_user_id(self):
        return str(self.__user['user_id'])
