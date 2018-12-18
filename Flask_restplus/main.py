# import configparser
import datetime

from flask import Blueprint, Flask, url_for
from controllers.serializers import api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config_by_name
from error_handler import error_handler, setLogger

app = Flask('Restplus_api')
app.config.from_object(config_by_name['dev_local'])
myapp_config = app.config
cors = CORS(app, resources={r"*": {"origins": "*"}})

jwt = JWTManager(app)
jwt._set_error_handler_callbacks(api)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    from models.TokenRevoke import TokenRevoke
    return TokenRevoke.is_jti_blacklisted(jti)


@app.route('/hello')
def index():
    return 'Hello, World! by TUNA\nDocument for API at {}'.format(url_for('api.doc', _external=True))


def init_blueprint():
    blueprint = Blueprint('api', __name__)
    from controllers.user_controller import user_ns, login_ns, logout_ns 
    from controllers.audio_controller import audio_ns
    api.init_app(blueprint)
    api.add_namespace(user_ns) 
    api.add_namespace(login_ns)
    api.add_namespace(logout_ns)
    api.add_namespace(audio_ns)
    app.register_blueprint(error_handler)
    app.register_blueprint(blueprint)


if __name__ == '__main__':

    setLogger(app)
    init_blueprint()
    app.run(host=app.config['HOST'], port=app.config['SERVER_PORT'])
