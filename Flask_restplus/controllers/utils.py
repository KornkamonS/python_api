import uuid
from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError


def validateData(data, schema):
    try:
        validate(data, schema)
    except ValidationError as e:
        return {'error': True, 'message': str(e).split('\n')[0]}
    except SchemaError as e:
        return {'error': True, 'message': str(e).split('\n')[0]}
    return {'error': False, 'data': data}


def verifyToken(id, payload):
    return id == payload['_id']
        

# def messageResponse(message, code):
#     res = {"message": message}
#     if code != 200:
#         res['error'] = True
#     return api.marshal(res, message_model, skip_none=True), code


# def dataResponse(data, code):
#     res = {"data": data}
#     if code != 200:
#         res['error'] = True
#     return res, code


# def isUUID(uid):
#     try:
#         uuid.UUID(uid)
#         return True
#     except:
#         return False
