from flask_restplus import Api, fields

Authorization = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(version='1.0', title='My Restplus API',
          description='API for Sayit application', authorizations=Authorization)

message_model = api.model('messageResponse', {
    'message': fields.String(description='return message')
})
file_model = api.model('file', {
    'file': fields.Raw(description='audio file')
})
user_data = api.model('user', {
    '_id': fields.String(readonly=True, description="The user identifier"),
    'username': fields.String(required=True, description='username'),
    'nameFirst': fields.String(description='First name'),
    'nameLast': fields.String(description='Last name'),
    'gender': fields.String(description='Gender'),
    'email': fields.String(description='E-mail'),
})

user_register = api.clone('userRegister', user_data, {
    'password': fields.String(required=True, description='Password', min_length=4)
})
user_edit_data = api.clone('userEdit', user_register, {
    'password': fields.String(required=False),
    'username': fields.String(readonly=True, description="Username", required=False)
})
user_login = api.model('userLogin', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})
access_token_model = api.model('accessToken', {
    'access_token': fields.String(require=True, description="User's access token for")
})


user_response_model = api.model('userResponse', {
    'token': fields.String(required=True, description='Access token'),
    'refresh_token': fields.String(required=True, description='Refresh token'),
    'payload': fields.Nested(user_data, required=True, description='Contain user data'),
    'expire_at': fields.Integer(required=True, description='Expiration Time of access token, keep in integer timestamp')
})

file_upload_model = api.model('fileUpload', {
    'file_name': fields.String(description='Access token'),
    'file_date': fields.String(format='date-time', required=True, description='Date-time that upload the file')
})
audio_res_model = api.model('audioResponse', {
    "_id": fields.String(readonly=True),    
    "file_date": fields.Integer,
    "user_uid": fields.String,
    "file_extension": fields.String,
    "file_name": fields.String,
    "file_path": fields.String,
    "DoSomeThing": fields.String
})