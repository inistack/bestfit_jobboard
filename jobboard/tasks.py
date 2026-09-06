from jobboard import create_app

flask_app = create_app()
celery = flask_app.celery

@celery.task
def ping():
    return "pong"