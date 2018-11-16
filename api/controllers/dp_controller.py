import os

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_restful import Resource, request, url_for
 
# from flask import Flask, request, jsonify
# import logging
from models.Deepspeech import *
# from models.deepspeech.data_loader import SpectrogramParser
# from models.deepspeech.decoder import GreedyDecoder
# from models.deepspeech.model import DeepSpeech
# from models.deepspeech.opts import add_decoder_args, add_inference_args
# from models.deepspeech.transcribe import transcribe
# from models.deepspeech.reverse import decoding_result
 
ALLOWED_EXTENSIONS = set(['.wav', '.mp3', '.ogg', '.webm'])

class deepspeech_api(Resource):
    @jwt_required
    def post(self):
# @app.route('/transcribe', methods=['POST'])
# def transcribe_file(): 
        res = {}
        if 'file' not in request.files:
            return {'message':'audio file shoule be passed for the transcription'},400
        
        file = request.files['file']
        # path_audio='./test_data/1028-20100710-hne_ar-01.wav' 
        # print(audio)
        filename = file.filename
        _, file_extension = os.path.splitext(filename)
        if file_extension.lower() not in ALLOWED_EXTENSIONS:
            return {'message':'{} is not supported format.'.format(file_extension)},400

        # try:
        dp=DeepSpeech(file,file_extension)
        res['transcription']=dp.transcription()
        res['error'] = False  
        return res,200
        # except:
            # return {'message':'something was wrong.'},500



 