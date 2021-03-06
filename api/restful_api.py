from flask import jsonify
from flask_restful import Resource, reqparse
from sqlite3 import connect, Error

con = connect(r'api\meetings_data1.db', check_same_thread=False)
cur = con.cursor()


class UserId(Resource):
    def get(self, user_id):
        ans = {}
        if (user_id,) in list(cur.execute('select user_id from users')):
            ans['status'] = True
            ans['is_admin'] = list(cur.execute(f'select is_admin from users where user_id={user_id}'))[0][0]
        else:
            ans['status'] = False
            ans['is_admin'] = False
        return jsonify(ans)


class EndRegistration(Resource):
    def get(self, name_surname, gender, username, profession, user_id, is_admin, password):
        if is_admin == 'True':
            is_admin = True
        else:
            is_admin = False
        cur.execute(f'insert into users (name_surname, gender, username, profession, user_id, is_admin,'
                    f' password) values("{name_surname}", "{gender}", "{username}", "{profession}", "{user_id}",'
                    f' "{is_admin}", "{password}")')
        con.commit()
        return jsonify({'success': True, 'error': 'ok'})
        # except Error:
        # return jsonify({'success': False})


class Search(Resource):
    def get(self, search_text):
        lst1 = list(cur.execute('select name_surname from users'))
        value = 'profession'
        for i in lst1:
            if search_text[5:-1] in i[0].strip():
                value = 'name_surname'
                break
        s = search_text[5:-1]
        ask = f'select name_surname, gender, username, profession, user_id from users where {value} like "%{s}%"'
        lst = list(cur.execute(ask))
        if len(lst) != 0:
            big_data = {}
            num = 0
            for people in lst:
                data = {
                    'name_surname': people[0],
                    'gender': people[1],
                    'username': people[2],
                    'profession': people[3],
                    'user_id': people[4]}
                num += 1
                big_data[str(num)] = data
            big_data['success'] = True
            return jsonify(big_data)
        else:
            return jsonify({'success': False, 'value': value, 'search_text': search_text, 'lst': lst1})


class Authorize(Resource):
    def get(self, username, password):
        username2 = list(cur.execute(f'select username from users'))
        if (username,) in username2:
            password2 = list(cur.execute(f'select password from users where username="{username}"'))
            print(password2)
            if password == list(password2[0])[0]:
                return {'success': True}
            else:
                return {'success': False}
        else:
            return {'success': False}

