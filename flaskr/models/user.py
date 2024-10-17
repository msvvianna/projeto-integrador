from email.policy import default

from werkzeug.security import generate_password_hash, check_password_hash
from flaskr import db
from enum import Enum

class Status(Enum):
    ADM = "adm"
    USER = "user"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    id_user = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.USER)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_name(self, name):
        self.name = name

    def set_email(self, email):
        self.email = email

    def set_id_user(self, id_user):
        self.id_user = id_user

    def set_status(self, status):
        if status == Status.ADM:
            self.status = Status.ADM
        else:
            self.status = Status.USER

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"