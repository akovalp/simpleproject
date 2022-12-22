from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db, User

#print all of the data
for user in User.query.all():
    print(user.id, user.name, user.surname, user.birthday)