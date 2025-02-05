import json


class BadResponse(Exception):
    """
    Currently used if the response can't be json encoded, despite a .json extension
    """


class DeleteError(Exception):
    """
    Used when a delete request did not return a 204
    """


class Timeout(Exception):
    """
    Used when a timeout occurs.
    """


class HTTPException(Exception):
    def __init__(self, response, *args, **kwargs):
        try:
            errors = json.loads(response.content.decode('utf8'))['errors']
            message = '\n'.join([error['message'] for error in errors])
        except Exception:
            if hasattr(
                    response,
                    'status_code') and response.status_code == 401:
                message = response.content.decode('utf8')
            else:
                message = response
        super(HTTPException, self).__init__(message, *args, **kwargs)


class HTTPBadRequest(HTTPException):
    """Generic >= 400 error
    """


class HTTPUnauthorized(HTTPException):
    """401
    """


class HTTPForbidden(HTTPException):
    """403
    """


class HTTPNotFound(HTTPException):
    """404
    """


class HTTPConflict(HTTPException):
    """409 - returned when creating conflicting resources
    """


class HTTPTooManyRequests(HTTPException):
    """429 - returned when exceeding rate limits
    """


class HTTPServerError(HTTPException):
    """Generic >= 500 error
    """


def detect_and_raise_error(response):
    if response.status_code == 401:
        raise HTTPUnauthorized(response)
    elif response.status_code == 403:
        raise HTTPForbidden(response)
    elif response.status_code == 404:
        raise HTTPNotFound(response)
    elif response.status_code == 409:
        raise HTTPConflict(response)
    elif response.status_code == 429:
        exc = HTTPTooManyRequests(response)
        exc.retry_after_secs = int(response.headers['Retry-After'])
        raise exc
    elif response.status_code >= 500:
        raise HTTPServerError(response)
    elif response.status_code >= 400:
        raise HTTPBadRequest(response)
