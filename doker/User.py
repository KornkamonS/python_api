from pymongo import MongoClient
from flask_login import UserMixin
myclient=MongoClient("mongodb://localhost:27017/")

##for docker
# myclient = MongoClient(
#     os.environ['DB_PORT_27017_TCP_ADDR'],
#     27017)
mydb = myclient["python_test_database"]
users_db = mydb["users"] 


class User(UserMixin):
    # proxy for a database of users
    user_database = users_db

    def __init__(self, username=None, password=None):
        
        if username is not None:
            self.id = self.get_uid(username)
            self.username=username

        if password is not None:
            self.password = self.hash_password(password)

    def save_to_db(self):
        user={ "_id":self.id,
                "username":self.username,
                "password":self.password}
        print(user)
        try:
            user_id=self.user_database.insert_one(user).inserted_id
            return user_id
        except:
            return None

    def get_uid(self,username):
       return uuid.uuid3(uuid.NAMESPACE_URL,username).hex
    
    def hash_password(self, password):
       return pwd_context.hash(password)

    @classmethod
    def get(cls,id):
        return cls.user_database.find_one(id)

    # @staticmethod
    # def generate_hash(password):
    #     return sha256.hash(password)
    
    # @staticmethod
    # def verify_hash(password, hash):
    # return sha256.verify(password, hash)