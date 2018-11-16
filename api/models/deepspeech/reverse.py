import json
import sys
import argparse

def getAsciiToPhone(mapped_file): 
    with open(mapped_file) as mapped_file:
        phone_to_ascii =  json.load(mapped_file) 

    ascii_to_phone = {v: k for k, v in phone_to_ascii.items()}
    return ascii_to_phone 

def decoding_result(raw_result,mapped_phone_file):
    asciiToPhone=getAsciiToPhone(mapped_phone_file)

    visually_result=''

    for word in raw_result.strip().split(' '):
        for ch in word:
            if ch in asciiToPhone:
                visually_result+=asciiToPhone[ch]
            else :
                visually_result+=ch    
            visually_result+=' '

    return visually_result

if __name__=='__main__':

    parser = argparse.ArgumentParser("revers.py")

    parser.add_argument('--decoder-result', metavar='./path/to/decoder/result',
                            help='path to result of decoder from transcribe.py')

    parser.add_argument('--mapped-phone', metavar='mapped_phone.txt',
                            help='path to mapped phoneme file { default= mapped_phone.txt}',
                            default='mapped_phone.txt')
                            
    args = parser.parse_args()
    dargs = vars(args)  

    if dargs['decoder_result']!=None: 
        with open(dargs['decoder_result']) as decoder_result:
            result =  json.load(decoder_result)

    elif not sys.stdin.isatty():
        decoder_result=sys.stdin.read()
        result=json.loads(decoder_result)

    else:
        raise Exception('Please input encoded text.')

    print('\n--- result ---')
    for result_output in result['output']:
        print('transcription: ',result_output['transcription'])
        decoding_result(result_output['transcription'],dargs['mapped_phone'])
