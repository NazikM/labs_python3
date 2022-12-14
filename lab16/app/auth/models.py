from flask_login import UserMixin
from sqlalchemy.sql.functions import now

from app import db, login_manager, bcrypt


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(255), nullable=False)
    tasks_owned = db.relationship('Task', backref='owner', lazy='dynamic')
    comments = db.relationship('Comment', backref='users', lazy='dynamic')
    is_admin = db.Column(db.Boolean, default=False, unique=False)
    about_me = db.Column(db.String(120), nullable=True)
    last_seen = db.Column(db.DateTime, default=now())

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password.decode('utf-8'), password)
