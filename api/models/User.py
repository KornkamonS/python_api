import configparser
import uuid

from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError
from passlib.apps import custom_app_context as pwd_context
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('config.ini') 

myclient=MongoClient(config['DATABASE']['DATABASE_URI'],
                    int(config['DATABASE']['PORT']))
 
database = myclient[config['DATABASE']['DATABASE_NAME']]
users_db = database[config['DATABASE']['TABLE_USER']] 
  
class User(object):
    user_schema = {
        "type": "object",
        "properties": {
            "username":{
                "type":"string"
            },
            "nameFirst": {
                "type": "string",
            },
            "nameFirst": {
                "type": "string",
            },
            "gender": {
                "type": "string",
            },
            "nativeLanguage": {
                "type": "string",
            },
            "total_progess": {
                "type": "integer",
            },
            "email": {
                "type": "string",
                "format": "email"
            },
            "password": {
                "type": "string",
                "minLength": 4
            }
        },
        "required": ["username"],
        "additionalProperties": False
    }
 
    user_database = users_db

    def __init__(self, data):
        
        self.data=data
        self.data['_id'] = self.get_uid(self.data['username'])

    def add_to_db(self):  
        self.data['password'] = self.hash_password(self.data['password']) 
        user_id=self.user_database.insert_one(self.data).inserted_id
        return user_id        

    def get_uid(self,username):
       return uuid.uuid3(uuid.NAMESPACE_URL,username).hex
    
    def hash_password(self, password):
       return pwd_context.hash(password)

    def verify_password_user(self):
        user=users_db.find_one({'_id':self.data['_id']})
        return pwd_context.verify(self.data['password'],user['password'])

    def get_data(self):
        return self.user_database.find_one({"_id":self.data['_id']},{"password":0})

    @classmethod
    def get(cls,id):
        return cls.user_database.find_one(id)

    @classmethod
    def delete(cls,id):  
        return cls.user_database.delete_one({ "_id": id}).deleted_count

    @classmethod
    def validate_data(cls,data):
        try:
            validate(data, cls.user_schema)
        except ValidationError as e:
            return {'error': False, 'message': str(e)}
        except SchemaError as e:
            return {'error': False, 'message': str(e)}
        return {'error': True, 'data': data}
