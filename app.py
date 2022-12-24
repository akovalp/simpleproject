from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False,)
    password = db.Column(db.String(50), nullable=False,)

    def __init__(self, name, surname, birthday, email, password):
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.email = email
        self.password = password

    def __repr__(self):
        return f"id={self.id} \n name={self.name} \n surname={self.surname} \n birthday={self.birthday} \n email={self.email} \n password={self.password} \n"


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/page', methods=['GET', 'POST'])
def page():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        birthday = request.form['birthday']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name=name, surname=surname,
                        birthday=birthday, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('thankyou.html', name=name, surname=surname, birthday=birthday, email=email, password=password)

    return render_template('form.html')


@app.route('/thankyou', methods=['GET', 'POST'])
def thankyou():
    all_users = User.query.all()

    if request.method == 'POST' and request.form['name'] != '' and request.form['surname'] != '':
        all_users = request.args.get('all_users')
        name = request.args.get('name')
        surname = request.args.get('surname')
        email = request.args.get('email')
        password = request.args.get('password')

        return render_template('thankyou.html', name=name, surname=surname, all_users=all_users, email=email, password=password)


@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('userlists.html', all_users=all_users)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            return redirect(url_for('users'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


@app.route('/buttons', methods=['GET', 'POST'])
def buttons():
    name = request.form.get('name')
    if name:
        query = db.session.query(User)
        query = query.filter(User.name.like('%' + name + '%'))
        users = query.all()
        html = ''
        for user in users:
            query = db.session.query(User)
            query = query.filter(User.name.like('%' + name + '%'))
            users = query.all()
            html = ''
            html += '<table class="table">'
            html += '<tr>'
            html += '<th>ID</th>'
            html += '<th>Name</th>'
            html += '<th>Surname</th>'
            html += '<th>Birthday</th>'
            html += '<th>Email</th>'
            html += '<th>Password</th>'
            html += '</tr>'
        for user in users:
            html += '<tr>'
            html += '<td>' + str(user.id) + '</td>'
            html += '<td>' + user.name + '</td>'
            html += '<td>' + user.surname + '</td>'
            html += '<td>' + user.birthday + '</td>'
            html += '<td>' + user.email + '</td>'
            html += '<td>' + user.password + '</td>'
            html += '<td>'
            html += '<a href="/delete/' + str(user.id) + '" class="btn btn-danger">Delete</a>'
            html += '</td>'
            html += '</tr>'
        html += '</table>'
        return html

    return render_template('buttons.html')


@app.route('/delete/<int:id>')
def delete(id):
  user = User.query.get(id)
  db.session.delete(user)
  db.session.commit()
  return redirect('/buttons')







if __name__ == '__main__':
    app.run(debug=True)
