import os

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user

from app.config import ApplicationConfig
from app.routes import routes
from app.models import db, User


app = Flask(__name__, static_folder="static")
app.config.from_object(ApplicationConfig)
CORS(app, supports_credentials=True,
     resources={r"/*": {"origins": "*"}})

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(routes)

#with app.app_context():
#    db.drop_all()
#    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/images/illustrations/<muscle>/<exercise>", methods=["GET"])
def serve_image(muscle, exercise):
    image_path = f"static/images/illustrations/{muscle}"
    
    path = os.path.join(image_path, f"{exercise}.png")

    return send_file(path), 200

