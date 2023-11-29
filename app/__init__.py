import os, logging
from flask import Flask
from app.user.apis import user_blueprint
from app.auth.apis import auth_blueprint
from app.task.apis import task_blueprint
from infrastructure.db import db, db_init
from flask_cors import CORS
from flask_talisman import Talisman
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])
logging.getLogger('flask_cors').level = logging.DEBUG

Talisman(
    app,
    content_security_policy={"default-src": "self"},
    force_https=False,
    strict_transport_security=False,
    content_security_policy_nonce_in=["script-src"],
)


database_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db.init_app(app)

app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(task_blueprint, url_prefix="/task")

@app.route("/", methods=["GET"])
def hello_world():
    return {"message": "Hi! Welcome to Sherin Olivia's Project Milestone 4..!"}, 200

# with app.app_context():
#     db_init()