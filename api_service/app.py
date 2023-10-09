# encoding: utf-8

from flask import Flask
from flask_jwt_extended import JWTManager

from api_service import api
from api_service.extensions import db
from api_service.extensions import migrate


def create_app(testing=False):
    app = Flask("api_service")

    app.config.from_object("api_service.config")
    app.config.from_prefixed_env()

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)
