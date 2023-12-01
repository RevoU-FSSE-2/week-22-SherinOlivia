import os
import logging
import secrets
from flask import Flask
from app.user.apis import user_blueprint
from app.auth.apis import auth_blueprint
from app.task.apis import task_blueprint
from infrastructure.db import db
from flask_cors import CORS
from flask_talisman import Talisman
from dotenv import load_dotenv
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

load_dotenv()

app = Flask(__name__)
api = Api(app)

# Additional Headers Middleware
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), midi=(), sync-xhr=(), microphone=(), camera=(), magnetometer=(), gyroscope=(), accelerometer=(), fullscreen=(self), payment=()"

    return response

# Swagger UI Blueprint
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "W22 Project Milestone 5 - Todo App"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# CORS
CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "https://week22-44a31.web.app"])
logging.getLogger('flask_cors').level = logging.DEBUG

# Talisman and Additional Headers Configuration
# nonce = secrets.token_hex(16)
# csp = {
#     "default-src": "'self'",
#     "style-src": ["'self'", f"'nonce-{nonce}'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
#     "script-src": ["'self'", f"'nonce-{nonce}'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
# }
# Talisman(
#     app,
#     content_security_policy=csp,
#     force_https=False,
#     strict_transport_security=False
# )

# Database
database_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db.init_app(app)

# Blueprints
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(task_blueprint, url_prefix="/task")


# Landing Page
@app.route("/", methods=["GET"])
def landing_page():
    return {"message": "Hi! Welcome to Sherin Olivia's Project Milestone 4..!"}, 200


if __name__ == '__main__':
    app.run(debug=True)
