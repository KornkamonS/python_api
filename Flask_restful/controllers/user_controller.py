
import datetime

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_restful import Resource, request, url_for

from models.TokenRevoke import *
from models.User import * 


def user_response(data):
    access_token = create_access_token(identity = data)
    refresh_token = create_refresh_token(identity = data)
    data={
        "error":False,
        "token":access_token,
        "refrest_token":refresh_token,
        "payload":data,
        "expire_at":str((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp())
        }
    return data

class Users_api(Resource):
    def post(self):
        data = User.validate_data(request.get_json())
         
        if not data['error']:
            return data,500
        data = data['data']

        if users_db.find_one({"username":data["username"]}) is not None:
            return ({'message': "Account already exist"}), 500

        user = User(data) 
        try:
            user_id=user.add_to_db()  
            return (user_response(user.get_data()), 200,{'Location': url_for('api.users_api', id=user_id, _external=True)})
        except :
            return {"message":"add user error, please try agin"},500  
                         
    @jwt_required        
    def get(self,id=None):
        if id==None:
            return list(User.user_database.find({},{ "password": 0 })),200
        else:   
            user =User.user_database.find_one({"_id":id},{ "password": 0 })
            if user is None:
                return {'message':'user not found'},404  
            return  user,200
    
    @jwt_required  
    def delete(self,id):
        try:
            count = User.delete(id)
            if count == 0 :
                return {'message':'user not found'} , 404
            return  {'message':'deleted successful'} , 200
        except: 
            return  {'message':'deleted fail'} , 500

    @jwt_required  
    def put(self,id):
        data = User.validate_data(request.get_json())
         
        if not data['error']:
            return data,500
        data = data['data']
        user = User(data) 
        try:
            user_id=user.add_to_db()  
            return (user_response(user.get_data()), 200,{'Location': url_for('api.users_api', id=user_id, _external=True)})
        except:
            return {"message":"add user error, please try agin"},500  

class UserLogin(Resource):
    def post(self):

        data = User.validate_data(request.get_json())
         
        if data['error']:
            data = data['data']
        else:  
            return ({'message': "Invalid username or password"}), 500

        if users_db.find_one({"username":data["username"]}) is None:
            return ({'message': "User not found"}), 404

        user=User(data)
        if(user.verify_password_user()):  
            return (user_response(user.get_data()), 200,{'Location': url_for('api.users_api', id=user.data['_id'], _external=True)})
        return {'message': 'wrong password'},404

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        
        try:
            revoked_token = TokenRevoke(jti)
            revoked_token.add() 
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = TokenRevoke(jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {'answer': 42 }
