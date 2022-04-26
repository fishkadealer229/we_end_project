import sqlite3
import os
from api.restful_api import UserId, EndRegistration, Search, Authorize
from flask import Flask, render_template, request, g, flash, redirect, url_for
from flask_restful import Api
from FDataBase import FDataBase
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin

DATABASE = 'meetings_data_new.db'
DEBUG = True
SECRET_KEY = 'Albert123'

app = Flask(__name__)
app.config.from_object(__name__)
api = Api(app)
api.add_resource(UserId, '/staff_api/user/id/<int:user_id>')
api.add_resource(EndRegistration, '/staff_api/end_register')
api.add_resource(Search, '/staff_api/search/<string:search_text>')
api.add_resource(Authorize, '/staff_api/authorize/<string:username>/<string:password>')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'meetings_data_new.db')))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(username):
    print("load_user")
    return UserLogin().fromDB(username, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    return render_template('index.html', menu=dbase.getMenu())


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = dbase.getUser(request.form['username_'])
        if user and user['password'] == request.form['password']:
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    if request.method == "POST":
        res = dbase.addUserinfo(request.form['name_surname'],
                                request.form['gender'], request.form['profession_'],
                                request.form['username_'], request.form['password_'])
        if res:
            flash("Данные успешно сохранены", "success")
    return render_template("user_info.html")


if __name__ == "__main__":
    app.run(debug=True)
