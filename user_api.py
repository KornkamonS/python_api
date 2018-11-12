import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
import uuid
import pymongo

# from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
  
# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
 
auth = HTTPBasicAuth()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["python_test_database"]
users_db = mydb["users"] 

class User():       
    def __init__(self) :
        self.user_data={}  

    def set_data(self,username,password):
        self.user_data['username']=username
        self.user_data['_id']=self.get_uid(username)
        self.user_data['password']=self.hash_password(password)

    def get_uid(self,username):
       return uuid.uuid3(uuid.NAMESPACE_URL,username).hex

    def hash_password(self, password):
       return pwd_context.hash(password)

def verify_password(user_password,input_password):
    return pwd_context.verify(input_password,user_password)

def generate_auth_token(user_id,expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': user_id})

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token
    user = users_db.find_one(data['id'])
    return user


@auth.verify_password
def verify_user(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = users_db.find_one({"username":username_or_token})
        if not user or not verify_password(user['password'],password):
            return False
    g.user = user
    return True


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if username is None or password is None:
        return (jsonify({'message': "Invalid username or password"}), 400)

    if users_db.find_one({"username":username}) is not None:
        return (jsonify({'message': "Account already exist"}), 400)

    user = User()
    user.set_data(username,password)
    x = users_db.insert_one(user.user_data)
    print("insert success at id {}".format(x.inserted_id))
    return (jsonify({"username":user.user_data['username']}), 200,
            {'Location': url_for('get_user', id=user.user_data['_id'], _external=True)})


@app.route('/api/users/<id>')
def get_user(id):
    user = users_db.find_one(id)
    if not user:
        return (jsonify({'message': "Not found"}), 400) 
    return jsonify({'username': user['username']})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = generate_auth_token(g.user['_id'],600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user['username']})


if __name__ == '__main__': 
    app.run(debug=True)