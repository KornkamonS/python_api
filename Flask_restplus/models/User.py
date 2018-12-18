import uuid

from passlib.apps import custom_app_context as pwd_context
import datetime
from models.table_connection import users_db


class User(object):

    user_database = users_db
    score_key = ['vowel_score', 'consonant_score']

    def __init__(self, data):
        self.data = {}
        if '_id' not in data:
            self.data['_id'] = self.getUID(data['username'])

        self.setData(data)

    def addUserToDb(self):
        print(self.data)
        self.data['_id'] = self.getUID(self.data['username'])
        self.data['password'] = self.hashPassword(self.data['password'])
        user_id = self.user_database.insert_one(self.data).inserted_id
        return user_id

    def setData(self, data):
        for k, v in data.items():
            self.data[k] = v

    def editUserData(self):

        if 'password' in self.data:
            self.data['password'] = self.hashPassword(self.data['password'])

        if 'username'in self.data:
            del self.data['username']

        updated_user = {"$set": self.data}
        self.user_database.find_one_and_update(
            {"_id": self.data['_id']}, updated_user)


    def getUID(self, username):
       return uuid.uuid3(uuid.NAMESPACE_URL, username).hex

    def hashPassword(self, password):
       return pwd_context.hash(password)

    def verifyPasswordUser(self):
        user = self.user_database.find_one({'_id': self.data['_id']})
        return pwd_context.verify(self.data['password'], user['password'])

    def get(self, fields={}):
        fields["password"] = 0
        return self.user_database.find_one({"_id": self.data['_id']}, fields)

    @classmethod
    def find_one(cls, data):
        return cls.user_database.find_one(data, {'password': 0})

    @classmethod
    def delete(cls, id):
        return cls.user_database.delete_one({"_id": id}).deleted_count

    def getDataInList(self,key,value,list):
        return (next((item for item in list if item.get(key)  == value), None)) 

