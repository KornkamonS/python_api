import pyrebase
import uuid
import json
 
def get_uid(email):
    return uuid.uuid3(uuid.NAMESPACE_URL,email).hex

    with open('config.json') as f:
        config=json.load(f)  

    firebase = pyrebase.initialize_app(config['firebase'])
    db = firebase.database() 

def create_user(email,password,data):
    global db
    auth = firebase.auth()     
    uid=get_uid(email)
    user=auth.create_user_with_email_and_password(email, password)
    db.child('users/'+str(uid)).set(data)
    return user

def get_user_data(email):
    global db 
    uid=get_uid(email)
    db = firebase.database() 
    user=db.child('users/'+str(uid)).get()
    return user.val()