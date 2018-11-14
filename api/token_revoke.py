from pymongo import MongoClient

myclient=MongoClient("mongodb://localhost:27017/")

##for docker
# myclient = MongoClient(
#     os.environ['DB_PORT_27017_TCP_ADDR'],
#     27017)
mydb = myclient["python_test_database"]
token_revoke_db = mydb["token_revoke"] 
  
class TokenRevoke(object):
    token_revoke = token_revoke_db

    def __init__(self, token):         
        self.token = token 

    def add(self):
        token={"jti":self.token}
        token_id=self.token_revoke.insert_one(token).inserted_id
        return token_id 

    @classmethod
    def get(cls,token):
        return cls.token_revoke.find_one({'jti':token})

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.token_revoke.find_one({"jti": jti})
        return bool(query)     
