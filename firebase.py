import pyrebase
import uuid
 
config = {
    "apiKey": "AIzaSyCTpzI-V7DSHx38tw43iVROVCiojHOTA_U",
    "authDomain": "python-api-test-tuna.firebaseapp.com",
    "databaseURL": "https://python-api-test-tuna.firebaseio.com",
    # "projectId": "python-api-test-tuna",
    "storageBucket": "python-api-test-tuna.appspot.com",
    # "messagingSenderId": "634226262770",
    "serviceAccount": "serviceAccountCredentials.json"
  }
firebase = pyrebase.initialize_app(config)
def create_user(email,password):
    auth = firebase.auth()
    
    ## Problem: gen uuid duplicate !!!!!!!!!!!
    uid=uuid.uuid3(uuid.NAMESPACE_URL,email)
    user=auth.create_user_with_email_and_password(email, password)
 
    data = {
        "eamil": email,
        "name": email
    } 
    db = firebase.database() 
    a=db.child('users/'+str(uid)).set(data)
    return user

def get_user_data(email):

    uid=uuid.uuid3(uuid.NAMESPACE_URL,email)
    a=db.child('users/'+str(uid)).get()
    return a.val()

email='test3@h.com'
password='123456'

create_user(email,password)

