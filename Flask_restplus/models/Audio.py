
from mimetypes import MimeTypes
import uuid
import os
from error_handler import logging_info
from models.table_connection import users_db, user_audio_db, file_db
from main import myapp_config
from tempfile import NamedTemporaryFile

class Audio(object):
    mime = MimeTypes()
    user_audio_database = user_audio_db
    file_database = file_db 

    def __init__(self, data):
        self.data = {}
        # if '_id' not in data:
        #     self.data['_id'] = self.getUID(
        #         data['user_uid']+data['file_date'] + uuid.uuid4().hex[:5])

        self.setData(data)
        self.data['file_name'] = uuid.uuid4().hex + data['file_date'] + \
            self.data['file_extension']

    def setData(self, data):
        for k, v in data.items():
            self.data[k] = v

    def getUID(self, name):
        return uuid.uuid3(uuid.NAMESPACE_URL, name).hex

    def saveToDb(self, file):
        self.data['contentType'], _ = self.mime.guess_type(
            self.data['file_name'])
            
        # for file size < 16 MB
        # from bson.binary import Binary
        # self.data['file'] = Binary(self.file.read())

        self.data['_id'] = self.file_database.put(file, **self.data)

    def updataAudioData(self):
        update_field = ['DoSomeThing']
        update_data = {}
        for key in update_field:
            if key in self.data:
                update_data[key] = self.data[key]
        import datetime
        update_data['transcription_date'] = datetime.datetime.now()
        self.user_audio_database.find_one_and_update(
            {'_id': self.data['_id']}, {"$set": update_data})

    
    def doSomeThingWithFile(self):
        
        logging_info('transcription file')
        with NamedTemporaryFile(suffix=self.data['file_extension']) as tmp_saved_audio_file:
            file_data = self.file_database.get(self.data['_id']).read()
            tmp_saved_audio_file.write(file_data) 
            self.data['DoSomeThing'] = "Test process" 

    @classmethod
    def find_one(cls, query, arg=None):
        return cls.user_audio_database.find_one(query, arg)

    @classmethod
    def find(cls, query, arg=None):
        return list(cls.user_audio_database.find(query, arg))

    @classmethod
    def delete(cls, query):
        result = Audio.find(query)
        for audio in result:
            cls.file_database.delete(audio['_id'])
        return len(result)

    @classmethod
    def getFileFromDirectory(cls, query):
        data = cls.user_audio_database.find_one(query)
        if data is None:
            return None, None
        file = cls.file_database.find_one(data['_id'])
        return data, file
