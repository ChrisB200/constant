from flask import Blueprint
from .auth import auth
from .exercise import exercise

routes = Blueprint("routes", "__name__")
routes.register_blueprint(auth)
routes.register_blueprint(exercise)
