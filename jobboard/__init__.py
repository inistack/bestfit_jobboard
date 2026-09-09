from flask import Flask
from flask_smorest import Api
from .extensions import db, migrate, jwt, limiter, mail
from .celery_app import init_celery
from dotenv import load_dotenv

load_dotenv()

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    mail.init_app(app)
    app.celery = init_celery(app)

    with app.app_context():
        from . import models 

    from .views import bp
    from .apis.job import job_bp
    from .apis.auth import auth_bp
    from .apis.application import appl_bp

    api = Api(app)
    api.register_blueprint(bp)
    api.register_blueprint(job_bp)
    api.register_blueprint(auth_bp)
    api.register_blueprint(appl_bp)

    return app
