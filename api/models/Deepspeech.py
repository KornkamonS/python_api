
from tempfile import NamedTemporaryFile
import wave
import torch

from models.deepspeech.data_loader import SpectrogramParser
from models.deepspeech.decoder import GreedyDecoder
from models.deepspeech.model import DeepSpeech
from models.deepspeech.opts import add_decoder_args, add_inference_args
from models.deepspeech.transcribe import transcribe
from models.deepspeech.reverse import decoding_result 
import configparser

config = configparser.ConfigParser()
config.read('config.ini')  
torch.set_grad_enabled(False) 

class DeepSpeech(object):
    mapped_phone=config['MODEL']['MAPPED_PHON_PATH'] 
    model = DeepSpeech.load_model(config['MODEL']['MODEL_PATH'])
    cuda = config['MODEL']['CUDA']
    if cuda=='True':
        model.cuda()
    model.eval()

    labels = DeepSpeech.get_labels(model)
    audio_conf = DeepSpeech.get_audio_conf(model)
    decoder = config['MODEL']['DECODER']
    if decoder == "beam":
        from decoder import BeamCTCDecoder

        decoder = BeamCTCDecoder(labels, lm_path=args.lm_path, alpha=args.alpha, beta=args.beta,
                                cutoff_top_n=args.cutoff_top_n, cutoff_prob=args.cutoff_prob,
                                beam_width=args.beam_width, num_processes=args.lm_workers)
    else:
        decoder = GreedyDecoder(labels, blank_index=labels.index('_'))

    spect_parser = SpectrogramParser(audio_conf, normalize=True)

    def __init__(self,file,file_extension):
        self.file=file
        self.ext=file_extension

    def transcription(self):
        with NamedTemporaryFile(suffix=self.ext) as tmp_saved_audio_file:
            self.file.save(tmp_saved_audio_file.name)
            # logging.info('Transcribing file...')
            transcription, _ = transcribe(tmp_saved_audio_file.name, self.spect_parser, self.model, self.decoder, self.cuda)
            return decoding_result(transcription[0][0],self.mapped_phone)
            # logging.info('File transcribed')
            # res['error'] = False
            
            # res['transcription'] = result 
    
    