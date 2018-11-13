from User import *

from flask import Flask, Response
from flask_login import LoginManager, login_required
import uuid
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

login_manager = LoginManager()
login_manager.init_app(app) 

@app.route('/')
def hello_page():
    return 'hello user API by tuna'
 
# @app.route('/api/users', methods=['POST'])
# def new_user():
#     username = request.json.get('username')
#     password = request.json.get('password')
    
#     if username is None or password is None:
#         return (jsonify({'message': "Invalid username or password"}), 400)

#     if users_db.find_one({"username":username}) is not None:
#         return (jsonify({'message': "Account already exist"}), 400)

#     user = User()
#     user.set_data(username,password)
#     x = users_db.insert_one(user.user_data)
#     print("insert success at id {}".format(x.inserted_id))
#     return (jsonify({"username":user.user_data['username']}), 200,
#             {'Location': url_for('get_user', id=user.user_data['_id'], _external=True)})

if __name__ == '__main__': 
    app.run(debug=True)

# user=User()
# user=User('Tunaa3','test')
# # print(User.save_to_db())## error 
# d=User.get("b366a56cd8013ddf96ffce94e86f16e7")
# # d=user.get()
# print(user.save_to_db())
# print(d)