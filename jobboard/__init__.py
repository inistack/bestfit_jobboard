from flask import Flask
from flask_smorest import Api
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import models 

    from .views import bp

    api = Api(app)
    api.register_blueprint(bp)

    return app
