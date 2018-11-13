import random
import hashlib
import uuid
def get_salt(n):
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=[]
    for i in range(n):
        chars.append(random.choice(ALPHABET))
    return "".join(chars)

def hash_password(password):
    salt=get_salt(32)
    encode_pass=(password+salt).encode()
    hash_ob=hashlib.sha512(encode_pass)
    return hash_ob.hexdigest()+':'+salt

def check_password(password,input):
    hash_password,salt=password.split(':') 
    return hashlib.sha512((input+salt).encode()).hexdigest()==hash_password

# a=hash_password('123456')
# r=check_password(a,'123456')
# print(r)
# r=check_password(a,'1223456')
# print(r)