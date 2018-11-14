from flask import Blueprint, Flask, jsonify

import models
import user_controller
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_restful import Api
from User import *
import datetime
from token_revoke import *
app = Flask(__name__)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return TokenRevoke.is_jti_blacklisted(jti)

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World! by TUNA'})

api.add_resource(user_controller.Users_api,'/users','/users/<id>')
api.add_resource(user_controller.UserLogin, '/login')  
api.add_resource(user_controller.UserLogoutAccess, '/logout')

api.add_resource(user_controller.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user_controller.TokenRefresh, '/token/refresh') 
api.add_resource(user_controller.SecretResource, '/secret')
app.register_blueprint(api_bp)

if __name__ == '__main__': 
    app.run(debug=True)