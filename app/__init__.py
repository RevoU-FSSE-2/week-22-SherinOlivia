import os
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return {"message": "Hi! Welcome to Sherin Olivia's Project Milestone 4..!"}, 200