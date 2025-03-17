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

    sets = db.relationship("Set", back_populates="user", cascade="all, delete")

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
    img_url = db.Column(db.Text)

    execution = db.relationship(
        "Execution", back_populates="exercise", cascade="all, delete"
    )
    equipment = db.relationship(
        "ExerciseEquipment", back_populates="exercise", cascade="all, delete"
    )
    sets = db.relationship("Set", back_populates="exercise", cascade="all, delete")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_position": self.start_position,
            "main_muscle": self.main_muscle,
            "img": self.img_url,
            "equipment": [eq.to_json() for eq in self.equipment]
        }


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

    def to_json(self):
        return self.equipment.to_json()


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    exercise_equipment = db.relationship(
        "ExerciseEquipment", back_populates="equipment", cascade="all, delete"
    )

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }


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


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), nullable=False, default="kg")
    order = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey("user.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=False)

    user = db.relationship("User", back_populates="sets")
    exercise = db.relationship("Exercise", back_populates="sets")

    def to_json(self):
        return {
            "id": self.id,
            "reps": self.reps,
            "weight": self.weight,
            "unit": self.unit,
            "order": self.order,
            "date": self.date,
            "exercise_id": self.exercise_id
        }
