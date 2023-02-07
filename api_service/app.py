# encoding: utf-8

from flask import Flask
from api_service import api
from api_service.extensions import db
from api_service.extensions import migrate

def create_app(testing=False):
    app = Flask("api_service")
    app.config.from_object("api_service.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)

    # lst = [str(p) for p in app.url_map.iter_rules()]
    # print(lst)

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)


if __name__ == '__main__':
    app = create_app(False)
    app.run(host='0.0.0.0', port=5000)