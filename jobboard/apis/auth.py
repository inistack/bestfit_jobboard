from jobboard.schemas.auth import RegisterSchema, LoginSchema, TokenSchema
from jobboard.models import User
from jobboard.extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_smorest import Blueprint, abort
from flask.views import MethodView

auth_bp = Blueprint('auth', __name__, description='User authentication endpoints')

@auth_bp.route('/auth/register')
class Register(MethodView):
    pass

