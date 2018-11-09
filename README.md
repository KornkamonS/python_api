# Practice python api
## Description:
### this project create for practice python skill with create API by python.
------
### DAY 1 : Firebase
* use pyrebase library
* must have serviceAccountCredentials.json (get in firebase console)
* lib: [pyrebase](https://github.com/thisbejim/Pyrebase#authentication) , [uuid](https://docs.python.org/3/library/uuid.html)

### DAY 2 : Token Jwt and password hash salt
* use [jwt]() to create token.
* when register, change password user to hash(password + salt) => hash_password and sent hash_password to keep in database.
* when login use hash(input_password + salt_db)== hash_password_db
>* _db = data in database , salt is random string.
* learn to create class python