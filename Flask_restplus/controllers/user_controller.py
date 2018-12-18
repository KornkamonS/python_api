import datetime

from flask import request, url_for
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_restplus import Resource, Namespace

from controllers.serializers import (access_token_model, api, message_model,
                                     user_data,
                                     user_edit_data,
                                     user_login, user_register,
                                     user_response_model)
from controllers.utils import validateData, verifyToken
from error_handler import DatabaseError
from models.TokenRevoke import TokenRevoke
from models.User import User

user_ns = Namespace('users', description='Operations related to user')


def userResponse(user_data):
    access_token = create_access_token(identity=user_data)
    refresh_token = create_refresh_token(identity=user_data)
    data = {
        "token": access_token,
        "refresh_token": refresh_token,
        "payload": user_data,
        "expire_at": int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp())
    }
    return data


@user_ns.route('')
class UserCollection(Resource):

    @user_ns.doc(body=user_register)
    @user_ns.response(500, 'Add user error')
    @user_ns.response(409, 'Username has already taken')
    @user_ns.response(404, 'Wrong password or User not found')
    @user_ns.response(400, 'Invalid input')
    @user_ns.marshal_with(user_response_model)
    @user_ns.expect(user_register)
    def post(self):
        """
        Create a new user account
        """

        data = validateData(user_ns.payload, user_register._schema)
        if data['error']:
            user_ns.abort(400, data['message'])

        data = data['data']
        if User.find_one({"username": data["username"]}) is not None:
            user_ns.abort(409, "username has already taken")

        user = User(data)
        try:
            user.addUserToDb()
            return userResponse(user.get()), 200, {'Location': api.url_for(UserItem, user_uid=user.data['_id'], _external=True)}
        except:
            DatabaseError()
        user_ns.abort(500, "Add user error, please try agin")

    @user_ns.doc(security='apikey')
    @user_ns.doc(responses={500: 'Internal Server Error'})
    @user_ns.marshal_list_with(user_data, skip_none=True, envelope='data')
    @jwt_required
    def get(self):
        '''
        Get all user's data
        '''
        return list(User.user_database.find({}, {"password": 0})), 200


@user_ns.route('/<string:user_uid>')
@user_ns.param('user_uid', 'The user identifier')
class UserItem(Resource):

    @user_ns.response(404, 'User not found')
    @user_ns.response(400, 'Invalid token')
    @user_ns.marshal_with(user_data, skip_none=True, envelope='data')
    @user_ns.doc(security='apikey')
    @jwt_required
    def get(self, user_uid=None):
        '''
        Get an user data
        '''
        if not verifyToken(user_uid, get_jwt_identity()):
            user_ns.abort(400, 'Invalid token')

        user = User({'_id': user_uid})
        user = user.get()
        if user is None:
            user_ns.abort(404, 'User not found')

        return user, 200

    @user_ns.response(200, 'Deleted successful')
    @user_ns.response(404, 'User not found')
    @user_ns.response(400, 'Invalid token')
    @user_ns.response(500, 'Deleted fail')
    @user_ns.doc(security='apikey')
    @user_ns.marshal_with(message_model, skip_none=True)
    @jwt_required
    def delete(self, user_uid):
        '''
        Delete an user 
        '''
        if not verifyToken(user_uid, get_jwt_identity()):
            user_ns.abort(400, 'Invalid token')
        try:
            count = User.delete(user_uid)
        except:
            DatabaseError()
            user_ns.abort(500, 'Deleted fail, please try again')

        if count == 0:
            user_ns.abort(404, 'User was deleted')

        return {'message': 'User is deleted'}, 200

    @user_ns.response(404, 'User not found')
    @user_ns.response(400, 'Invalid token or data')
    @user_ns.response(500, 'Update data error')
    @user_ns.doc(body=user_edit_data)
    @user_ns.expect(user_edit_data)
    @user_ns.doc(security='apikey')
    @user_ns.marshal_with(user_data, envelope='data', skip_none=True)
    @jwt_required
    def put(self, user_uid):
        '''
        Update an existing user 
        '''
        if not verifyToken(user_uid, get_jwt_identity()):
            user_ns.abort(400, 'Invalid token')

        editted_data = user_ns.payload
        editted_data['_id'] = user_uid

        user = User.find_one(user_uid)
        if user is None:
            user_ns.abort(404, 'User not found')

        user = User(user)
        user.setData(editted_data)
        
        schema = user_edit_data._schema
        schema['additionalProperties'] = False
        data = validateData(user.data, schema)
        if data['error']:
            user_ns.abort(400, data['message'])

        try:
            user.editUserData()
            return user.get(), 200, {'Location': url_for('api.users_user_item', user_uid=user.data['_id'], _external=True)}
        except:
            DatabaseError()
        user_ns.abort(500, 'Edit user error, please try again')



login_ns = Namespace('login', description='Operations for login')


@login_ns.route('')
class UserLogin(Resource):

    @login_ns.expect(user_login, validate=True)
    @login_ns.response(404, 'User not found')
    @login_ns.response(400, 'Invalid username or password')
    @login_ns.marshal_with(user_response_model)
    def post(self):
        """
        Create user's access token and refresh token
        """
        data = login_ns.payload

        if User.find_one({"username": data["username"]}) is None:
            login_ns.abort(404, 'User not found')

        user = User(data)
        if(user.verifyPasswordUser()):
            return userResponse(user.get()), 200, {'Location': url_for('api.users_user_item', user_uid=user.data['_id'], _external=True)}

        login_ns.abort(400, 'Invalid username or password')


@login_ns.route('/refresh')
class TokenRefresh(Resource):
    # @login_ns.response(200, 'get access token successful', access_token_model)
    @login_ns.marshal_with(access_token_model)
    @login_ns.response('4xx', 'Invalid token')
    @login_ns.doc(security='apikey')
    @jwt_refresh_token_required
    def post(self):
        '''
        Get new user's access token  
        '''
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200


logout_ns = Namespace('logout', description='Operations for logout')


@logout_ns.route('')
class UserLogoutAccess(Resource):
    # @logout_ns.response(200, 'log out successful', message_model)
    @logout_ns.response(500, 'Log out fail')
    @logout_ns.response('4xx', 'Invalid token')
    @logout_ns.marshal_with(message_model)
    @logout_ns.doc(security='apikey')
    @jwt_required
    def post(self):
        """
        Revoke user's access token
        """
        jti = get_raw_jwt()['jti']

        try:
            revoked_token = TokenRevoke(jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}, 200
        except:
            DatabaseError()
        logout_ns.abort(500, 'Log out fail, please try again')


@logout_ns.route('/refresh')
class UserLogoutRefresh(Resource):
    @logout_ns.response(200, 'Log out successful')
    @logout_ns.response(500, 'Log out fail')
    @logout_ns.response('4xx', 'Invalid token')
    @logout_ns.marshal_with(message_model)
    @logout_ns.doc(security='apikey')
    @jwt_refresh_token_required
    def post(self):
        """
        Revoke user's refresh token  
        """
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = TokenRevoke(jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}, 200
        except:
            DatabaseError()
        logout_ns.abort(500, 'Log out fail, please try again')
