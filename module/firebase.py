import pyrebase
import uuid
import json


class myFirebase:
  def __init__(self):
    with open('config.json') as f:
      self.config=json.load(f) 

    self.firebase = pyrebase.initialize_app(self.config['firebase'])
    self.db = self.firebase.database() 
    
    
  def user_uid(self,email):
    return uuid.uuid3(uuid.NAMESPACE_URL,email).hex
 
  def create_user(self,email,password,data):
    auth = firebase.auth()     
    uid=user_uid(email)
    user=auth.create_user_with_email_and_password(email, password)
    self.db.child('users/'+str(uid)).set(data)
    return user
 
  def get_user_data(self,email):
    uid=self.user_uid(email)  
    user=self.db.child('users/'+str(uid)).get()
    return user.val()

# a=myFirebase() 
# print(a.get_user_data('test1@h.com'))

 
