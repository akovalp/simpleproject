#Code where I  play with data base ,0

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db, User
from faker import Faker

fake = Faker()
for i in range(100):
    new_user = User(name=fake.name(), surname=fake.name(), birthday=fake.date(), email=fake.email(), password=fake.password())
    db.session.add(new_user)
    db.session.commit()

print(User.query.all())



