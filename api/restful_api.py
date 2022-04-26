from flask import jsonify
from flask_restful import Resource, reqparse
import sqlite3
con = sqlite3.connect(r'api\meetings_data.db', check_same_thread=False)
cur = con.cursor()


class UserId(Resource):
    def get(self, user_id):
        ans = {}
        if (user_id,) in list(cur.execute('select user_id from users')):
            ans['status'] = False
            ans['is_admin'] = list(cur.execute(f'select is_admin from users where user_id={user_id}'))[0][0]
        else:
            ans['status'] = False
            ans['is_admin'] = False
        return jsonify(ans)


class EndRegistration(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name_surname', required=True)
        parser.add_argument('gender', required=True)
        parser.add_argument('username', required=True)
        parser.add_argument('profession', required=True)
        parser.add_argument('user_id', required=True, type=int)
        parser.add_argument('is_admin', required=True, type=bool)
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        name_surname = args['name_surname']
        gender = args['gender']
        username = args['username']
        profession = args['profession']
        user_id = args['user_id']
        is_admin = args['is_admin']
        password = args['password']
        cur.execute(f'insert into users (name_surname, gender, username, profession, user_id, is_admin, password)'
                    f' values("{name_surname}", "{gender}", "{username}", "{profession}", "{user_id}", "{is_admin}",'
                    f' "{password}")')
        con.commit()
        return jsonify({'success': True})


class Search(Resource):
    def get(self, search_text):
        if search_text in list(list(cur.execute('select name_surname from users'))[0])[0]:
            value = 'name_surname'
        else:
            value = 'profession'
        ask = f'select name_surname, gender, username, profession, user_id from users where {value}="{search_text}"'
        lst = list(cur.execute(ask))
        if len(lst) != 0:
            for people in lst:
                people = list(people)
                print(people)
                data = {
                    'name_surname': people[0],
                    'gender': people[1],
                    'username': people[2],
                    'profession': people[3],
                    'user_id': people[4],
                    'success': 'ok'}
                return jsonify(data)
        else:
            return jsonify({'success': 'no'})


class Authorize(Resource):
    def get(self, username, password):
        username2 = list(cur.execute(f'select username from users'))
        if (username,) in username2:
            password2 = list(cur.execute(f'select password from users where username = "{username}"'))
            print(password2)
            if password == list(password2[0])[0]:
                return {'success': True}
            else:
                return {'success': False}
        else:
            return {'success': False}

