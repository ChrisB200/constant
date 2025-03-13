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


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_position = db.Column(db.Text, nullable=False)
    main_muscle = db.Column(db.String(100))

    execution = db.relationship(
        "Execution", back_populates="exercise", cascade="all, delete"
    )
    equipment = db.relationship(
        "ExerciseEquipment", back_populates="exercise", cascade="all, delete"
    )


class ExerciseEquipment(db.Model):
    __tablename__ = "exercise_equipment"
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)

    exercise = db.relationship(
        "Exercise", back_populates="equipment", cascade="all, delete"
    )
    equipment = db.relationship(
        "Equipment", back_populates="exercise_equipment", cascade="all, delete"
    )


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    exercise_equipment = db.relationship(
        "ExerciseEquipment", back_populates="equipment", cascade="all, delete"
    )


class Execution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=False)

    steps = db.relationship("Step", back_populates="execution", cascade="all, delete")
    exercise = db.relationship(
        "Exercise", back_populates="execution", cascade="all, delete"
    )


class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    execution_id = db.Column(db.Integer, db.ForeignKey("execution.id"), nullable=False)

    execution = db.relationship(
        "Execution", back_populates="steps", cascade="all, delete"
    )
