from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import db, Exercise, Set
from datetime import datetime

exercise = Blueprint("exercises", __name__)


@exercise.route("/exercises", methods=["GET"])
def exercises():
    exercises = Exercise.query.all()
    return jsonify([ex.to_json() for ex in exercises]), 200


@exercise.route("/sets", methods=["POST"])
@login_required
def create_set():
    sets = request.json.get("sets")
    exercise_id = request.json.get("exercise_id")
    print(sets)
    print(exercise_id)

    if not sets:
        return jsonify({"error": "no sets provided"}), 400

    new_sets = []

    for i, s in sets.items():
        new_set = Set()
        new_set.reps = s.get("reps")
        new_set.weight = s.get("weight")
        new_set.unit = s.get("unit", "kg")
        date = s.get("date").split("T")[0]
        date = datetime.strptime(date, "%Y-%m-%d").date()
        new_set.date = date
        new_set.order = i
        new_set.user_id = current_user.id
        new_set.exercise_id = exercise_id
        new_sets.append(new_set)

    db.session.add_all(new_sets)
    db.session.commit()

    return jsonify("success"), 201


@exercise.route("/sets", methods=["GET"])
@login_required
def get_sets():
    date = request.args.get("date")

    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        jsonify({"error": "date is incorrect format"}), 400

    sets = Set.query.filter_by(user=current_user, date=date)

    return jsonify([s.to_json() for s in sets])


