from flask import Flask, render_template, request
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

    
db.create_all()


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/page', methods=['GET','POST'])
def page():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        birthday = request.form['birthday']
        new_user = User(name=name, surname=surname, birthday=birthday)
        db.session.add(new_user)
        db.session.commit()
        return render_template('thankyou.html', name=name, surname=surname)
    
    return render_template('form.html')

#Create a thank you page after the form is submitted with a dynamic url that shows the name of the user
@app.route('/thankyou')
def thankyou():
    if request.method == 'POST':
        first = request.args.get('name')
        last = request.args.get('surname')
        return render_template('thankyou.html', name=first, surname=last)




if __name__ == '__main__':
    app.run(debug=False)
