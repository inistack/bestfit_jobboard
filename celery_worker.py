from jobboard import create_app
from jobboard.celery_app import celery

app = create_app()

if __name__ == '__main__':
    celery.start()

