import logging
import sys
import traceback
from logging.handlers import RotatingFileHandler

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request, abort

error_handler = Blueprint('error_handler', __name__)
log = logging.getLogger('Restplus_api.sub')


def logging_info(message):
        app.logger.info(message)


def messageResponse(message, status_code):
        res = {"message": message}
        if status_code != 200:
                res['error'] = True
        return jsonify(res), status_code


def setLogger(app):

   file_handler = RotatingFileHandler(
       'server.log', maxBytes=1024 * 1024 * 100, backupCount=20)

   formatter = logging.Formatter(
       "%(asctime)s\t|\t%(funcName)s\t|\t%(levelname)s\t|\t%(message)s")

   file_handler.setFormatter(formatter)

   app.logger.addHandler(file_handler)
   app.logger.setLevel(logging.INFO)


def moreErrorDetail(message):
    return message+'\t[ Detail ]: [{}] {}, ip={}, platform={}, browser={}:{}, agent={}'.format(
        request.method,
        request.path,
        request.remote_addr,
        request.user_agent.platform,
        request.user_agent.browser,
        request.user_agent.version,
        request.user_agent.string)


@error_handler.route('/test_exception')
def logExp():
    raise Exception('Test Expection log.')


@error_handler.route('/uuid')
def testUUid():
        import uuid
        return uuid.uuid4().hex

@error_handler.route('/uuid/<text>')
def testUUid2(text):
        import uuid
        return uuid.uuid3(uuid.NAMESPACE_URL, text).hex

@error_handler.route("/test_log")
def logTest():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return messageResponse("Code Handbook !! Log testing.", 200)


@error_handler.app_errorhandler(404)
def page_not_found(error):
    app.logger.error(moreErrorDetail('url not found'))
    return messageResponse('This url does not exist', 404)


@error_handler.app_errorhandler(Exception)
def unhandle_exception(e):

    exception_detail = '\t'.join(
        traceback.format_exception(*sys.exc_info()))

    app.logger.error('{}\n\t{}'.format(moreErrorDetail('{}'.format(e)),
                                       exception_detail))
    return messageResponse('Internal Server Error : {}'.format(e), 500)


def DatabaseError():
    exception_detail = '\t'.join(
        traceback.format_exception(*sys.exc_info(), limit=-1))
    app.logger.error('{}\n\t{}'.format(moreErrorDetail('Database Error'),
                                       exception_detail))
#     return messageResponse('connection to database error, plase contact admin or try again', 500)
