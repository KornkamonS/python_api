import datetime
import os
import uuid
from bson.objectid import ObjectId 
from flask import request, send_file, url_for, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restplus import Resource, Namespace

from controllers.serializers import (api, file_model,audio_res_model,
                                     file_upload_model, message_model)
from controllers.utils import validateData, verifyToken
from error_handler import DatabaseError, logging_info
from models.Audio import Audio
from models.User import User

ALLOWED_EXTENSIONS = set(['.wav', '.mp3', '.ogg', '.webm'])

audio_ns = Namespace(
    'audio', description='Operations related to Audio file')


@audio_ns.route('/<string:user_uid>')
@audio_ns.param('user_uid', 'The user identifier')
class audioAPI(Resource):
    @audio_ns.doc(params={
        'file_name': {'in': 'formData', 'description': 'Name of file upload'},
        'file_date': {'in': 'formData', 'description': 'Config name', 'type': 'datetime', 'required': True},
        'file_data': {'in': 'formData', 'description': 'Config name', 'type': 'file', 'required': True}
    })
    @audio_ns.marshal_with(audio_res_model, skip_none=True, envelope='data')
    @audio_ns.response('4xx', 'Invalid token or file data')
    @audio_ns.response(500, 'Save file error')
    @audio_ns.doc(security='apikey')
    @jwt_required
    def post(self, user_uid):
        """
        Post and analysis  user audio 
        """
        if not verifyToken(user_uid, get_jwt_identity()):
            audio_ns.abort(400, 'Invalid token')

        result = request.form
        file_upload_schema = file_upload_model._schema
        file_upload_schema['additionalProperties'] = False

        data = validateData(result, file_upload_schema)
        if data['error']:
            audio_ns.abort(400, data['message'])

        data = data['data'].to_dict()
        data['user_uid'] = user_uid
        if 'file_data' not in request.files:
            audio_ns.abort(
                400, 'Audio file shoule be passed for the transcription')

        file = request.files['file_data']
        _, file_extension = os.path.splitext(file.filename)

        if file_extension.lower() not in ALLOWED_EXTENSIONS:
            audio_ns.abort(
                400, '{} is not supported format'.format(file_extension))

        user = User(User.find_one(user_uid))

        
        data['user_uid'] = user.data['_id']
        data['file_extension'] = file_extension

        audio = Audio(data)
       
        logging_info('User {} upload file {}'.format(
            user_uid, audio.data['file_name']))
        try:
            audio.saveToDb(file)
        except:
            audio_ns.abort(500, 'Save file data error, plase try again')

        try:
            audio.doSomeThingWithFile()
            audio.updataAudioData()
            return audio.data, 200, {'Location': url_for('api.audio_audio_url', file_name=audio.data['file_name'], _external=True)}
        except:
            DatabaseError()
        audio_ns.abort(500, 'Save analysis audio error, plase try again')

    @audio_ns.response('4xx', 'Invalid token')
    @audio_ns.doc(security='apikey')
    @audio_ns.marshal_list_with(audio_res_model, envelope='data', skip_none=True)
    @audio_ns.doc(params={
        'id': {'in': 'query', 'description': 'audio file uid'}
    })
    @jwt_required
    def get(self, user_uid):
        """
        Get list of user's audio file 
        """
        if not verifyToken(user_uid, get_jwt_identity()):
            return audio_ns.abort(400, 'Invalid token')
            # return messageResponse('Invalid token', 400)
        hidden_data = {'file_path': 0, 'file_extension': 0}
        id = request.args.get('id')
        query = {'user_uid': user_uid}
        
        if id is not None:
            query['_id'] = ObjectId(id)
        print(query)
        return Audio.find(query, hidden_data), 200

    @audio_ns.response(400, 'Invalid token')
    @audio_ns.response(200, 'Deleted successful')
    @audio_ns.response(500, 'Deleted fail')
    @audio_ns.marshal_with(message_model, skip_none=True)
    @audio_ns.doc(security='apikey')
    @audio_ns.doc(params={
        'id': {'in': 'query', 'description': 'audio file uid'}
    })
    @jwt_required
    def delete(self, user_uid):
        """
        Delete list of user's audio file
        """
        if not verifyToken(user_uid, get_jwt_identity()):
            audio_ns.abort(400, 'Invalid token')

        id = request.args.get('id')

        query = {'user_uid': user_uid}
        if id is not None:
            query['_id'] = ObjectId(id)
        print(query)
        try:
            deleted_count = Audio.delete(query)
            return {'message': '{} items were deleted'.format(deleted_count)}, 200
        except:
            DatabaseError()
        audio_ns.abort(500, 'Deleted fail, please try again')


@audio_ns.route('/url/<string:file_name>')
@audio_ns.param('file_name', 'File name')
class audioUrl(Resource):
    @audio_ns.response(200, 'Return audio file')
    @audio_ns.response(400, 'Invalid token or data')
    @audio_ns.response(404, 'File not found')
    @audio_ns.doc(security='apikey')
    @jwt_required
    def get(self, file_name):
        """
        Get user audio file
        """
        user = get_jwt_identity()
        audio_data, audio_file = Audio.getFileFromDirectory(
            {'file_name': file_name})
        if audio_data is None:
            audio_ns.abort(404, 'File not found')
        print(audio_data, audio_file)
        if 'user_uid' in audio_data:
            if user['_id'] == audio_data['user_uid']:
                response = make_response(audio_file.read())
                response.mimetype = audio_data['contentType']
                return response
        audio_ns.abort(400, 'Invalid token')
