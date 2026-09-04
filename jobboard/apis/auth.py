from jobboard.schemas.auth import RegisterSchema, LoginSchema, TokenSchema
from jobboard.models import User
from jobboard.extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_smorest import Blueprint, abort
from flask.views import MethodView

auth_bp = Blueprint('auth', __name__, description='User authentication endpoints')

@auth_bp.route('/auth/register')
class Register(MethodView):
    @auth_bp.arguments(RegisterSchema)
    @auth_bp.response(201, TokenSchema)
    def post(self, user_data):
        """Register new user"""
        existing_user = db.session.query(User).filter(User.email == user_data['email']).first()
        if existing_user:
            abort(409, message='User with this email already exists')
        
        new_user = User(email=user_data['email'], role=user_data['role'])
        new_user.set_password(user_data['password'])
        db.session.add(new_user)
        db.session.commit()

        claims = {'role': new_user.role}

        access_token = create_access_token(identity=str(new_user.id), additional_claims=claims)
        refresh_token = create_refresh_token(identity=str(new_user.id), additional_claims=claims)

        return {'access_token': access_token, 'refresh_token': refresh_token}
    

@auth_bp.route('/auth/login')
class Login(MethodView):
    @auth_bp.arguments(LoginSchema)
    @auth_bp.response(200, TokenSchema)
    def post(self, login_data):
        """Login user"""
        user = db.session.query(User).filter(User.email == login_data['email']).first()
        if user is None or not user.check_password(login_data['password']):
            abort(401, message='Invalid email or password')

        claims = {'role': user.role}

        access_token = create_access_token(identity=str(user.id), additional_claims=claims)
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims=claims)

        return {'access_token': access_token, 'refresh_token': refresh_token}

