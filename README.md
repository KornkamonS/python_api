# Practice python api
## Description:
### this project create for practice python skill with create API by python.
------
### DAY 1 : Firebase
* use pyrebase library
* must have serviceAccountCredentials.json (get in firebase console)
* lib: [pyrebase](https://github.com/thisbejim/Pyrebase#authentication) , [uuid](https://docs.python.org/3/library/uuid.html)

### DAY 2 : Token Jwt and password hash salt
* use [jwt](https://steelkiwi.com/blog/jwt-authorization-python-part-1-practise/) to create token.
* when register, change password user to hash(password + salt) => hash_password and sent hash_password to keep in database.
* when login use hash(input_password + salt_db)== hash_password_db
>* _db = data in database , salt is random string.
* learn to create class python

### DAY 3 : MongoDB ,flask_auth , SqlAlchemy
* use flask_auth to do the authenticate
* try to change SqlAlchemy to MongoDB from the [example](https://blog.miguelgrinberg.com/post/restful-authentication-with-flask)
* lib to wrapped pymongo for model [link](https://github.com/joshmarshall/mogo)