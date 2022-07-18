from flask import jsonify, request
import jsons
import traceback
from .apierror import APIError, RequestIsNotJSON


def json_call(func):
    def wrapper():
        try:
            if not request.json:
                raise RequestIsNotJSON
            jsn = request.json
            res = func(jsn)
            return jsons.dumps(res, strip_properties=True, strip_nulls=True, strip_privates=True, strip_class_variables=True), 200
        except APIError as e:
            traceback.print_exc()
            return jsonify({'Error': e.message}), 400
        except:
            traceback.print_exc()
            return jsonify({'Error': 'Unexpected error'}), 400
    wrapper.__name__ = func.__name__
    return wrapper


def getitem(iterable, index, default=None):
    try:
        return iterable[index]
    except IndexError:
        return default
