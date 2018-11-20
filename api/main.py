import configparser
import datetime

from flask import Blueprint, Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_restful import Api

import controllers.user_controller as user
from models.TokenRevoke import *

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

app.config['JWT_SECRET_KEY'] = config['DEFAULT']['JWT_SECRET_KEY']
app.config['SECRET_KEY'] = config['DEFAULT']['SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
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

api.add_resource(user.Users_api,'/users','/users/<id>')
api.add_resource(user.UserLogin, '/login')  
api.add_resource(user.UserLogoutAccess, '/logout')

api.add_resource(user.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user.TokenRefresh, '/token/refresh') 
api.add_resource(user.SecretResource, '/secret')  

app.register_blueprint(api_bp)

if __name__ == '__main__': 
    app.run(host='0.0.0.0',port=80,debug=True)
