from pymongo import MongoClient 
import gridfs
from main import myapp_config  

myclient = MongoClient(myapp_config['DATABASE_URL'], myapp_config['DATABASE_PORT'])
database = myclient[myapp_config['DATABASE_NAME']]

token_revoke_db = database['token_revoke']
users_db = database['users']
user_audio_db = database['user_audio'].files
file_db = gridfs.GridFS(database,collection='user_audio')
