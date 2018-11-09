import jwt
def get_token(data,secret):
    return encoded_token = jwt.encode(data,secret , algorithm='HS256')

def decode_token(token,secret) 
    return jwt.decode(encoded_token,secret, algorithm='HS256')
     