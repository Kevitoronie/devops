from flask import Flask
from padaria.ext import site


def create_app():
    app = Flask(__name__)
    app.secret_key = 'padaria'
    site.init_app(app)
    return app
