from jsonschema.validators import validator_for
from sanic.exceptions import InvalidUsage
from sanic.handlers import ErrorHandler
from sanic.response import json
from sanic.views import HTTPMethodView


def get_result_dict(answer, success=True, errors=None):
    return {
        'answer': answer,
        'success': success,
        'errors': errors or []
    }


class ApiError(Exception):
    def __init__(self, errors, status_code, headers=None):
        # Prepare
        result = get_result_dict(None, False, errors)

        self.result = result
        self.status_code = status_code
        self.headers = headers or {}


class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception):
        if isinstance(exception, ApiError):
            return json(exception.result,
                        status=exception.status_code,
                        headers=exception.headers)
        else:
            return super(CustomErrorHandler, self).default(request, exception)


class JsonSchemaHTTPMethodView(HTTPMethodView):
    # HTTP Method (uppercase) : Json schema to validate
    _schemas = {}

    def __init__(self):
        self._data = None

    def dispatch_request(self, request, *args, **kwargs):
        schema = self._schemas.get(request.method)
        if schema:
            v = validator_for(schema)(schema)
            if request.method in ('GET', 'HEAD'):
                # Processing url parameters
                self._data = {i: k[0] for i, k in request.args.items()}
            else:
                # Processing body parameters
                try:
                    self._data = request.json
                except InvalidUsage:
                    raise ApiError(['Invalid JSON data'], 406)

            errors = [e.message for e in v.iter_errors(self._data)]
            if errors:
                raise ApiError(errors, 406)
        return super(JsonSchemaHTTPMethodView, self).dispatch_request(request, *args, **kwargs)
