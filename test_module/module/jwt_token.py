import jwt
def get_token(data,secret):
    return jwt.encode(data,secret , algorithm='HS256')

def decode_token(token,secret) :
    return jwt.decode(token,secret, algorithm='HS256')
     
data={'test':"test"}
token=get_token(data,"tuna")
print(token)
token=b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDIxODQ5NDgsIm5iZiI6MTU0MjE4NDk0OCwianRpIjoiY2Y4YTJmMTUtNDU5Yy00OGUzLTkzYjAtMWZkMGM3YTY2MjQzIiwiZXhwIjoxNTQyMjcxMzQ4LCJpZGVudGl0eSI6eyJfaWQiOiI0YzFiZDhhYzAwZTEzMmQ2YmI0ZDgwMzNlYWRiZDI4NyIsInVzZXJuYW1lIjoidHVuYTEifSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.uadc0fiH4z1ES_JLfeQEXE1jZZW9WJw4l1LcPSIcTlY"
detoken=decode_token(token,'jwt-secret-string')
print(detoken)