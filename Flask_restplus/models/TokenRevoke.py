from models.table_connection import token_revoke_db


class TokenRevoke(object):
    token_revoke = token_revoke_db

    def __init__(self, token):
        self.token = token

    def add(self):
        token = {"jti": self.token}
        token_id = self.token_revoke.insert_one(token).inserted_id
        return token_id

    @classmethod
    def get(cls, token):
        return cls.token_revoke.find_one({'jti': token})

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.token_revoke.find_one({"jti": jti})
        return bool(query)
