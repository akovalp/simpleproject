from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')


db.create_all()
@app.route('/page', methods=['GET','POST'])
def page():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        birthday = request.form['birthday']
        new_user = User(name=name, surname=surname, birthday=birthday)
        db.session.add(new_user)
        db.session.commit()
        return render_template('form.html')
    
    return render_template('form.html')

if __name__ == '__main__':
    app.run()
