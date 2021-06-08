from .toolbox import gen_response
from rest_framework.response import Response

OK = 200
ERR_INVALID = 400
ERR_UNAUTH = 401
ERR_MISSING = 404
ERR_TEAPOT = 418
ERR_SERVER = 500
ERR_UNHOLY = 666

RESP_OK = Response(status=OK, data=None)
RESP_INVALID = Response(status=ERR_INVALID, data={"reason": "Invalid request"})
RESP_MISSING = Response(status=ERR_MISSING, data={"reason": "Something is missing!"})
RESP_SERVER = Response(status=ERR_SERVER, data={"reason": "Something unexpected happened on our end D:"})
