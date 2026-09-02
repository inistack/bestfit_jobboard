from flask.views import MethodView
from flask_smorest import Blueprint

bp = Blueprint('start', __name__, description='Health/welcome endpoints')

@bp.route('/')
class Home(MethodView):
    def get(self):
        return {"message": "Welcome to the Job Board API!"}, 200