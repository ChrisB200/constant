from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from uuid import uuid4

import bcrypt

db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


class User(UserMixin, db.Model):
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(300), nullable=False)
    password = db.Column(db.Text)

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(
            "utf-8"
        )

    def check_password(self, password):
        hashed_password = self.password.encode("utf-8")
        return bcrypt.checkpw(password.encode(), hashed_password)
