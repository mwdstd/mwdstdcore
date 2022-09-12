from flask import jsonify, request
import jsons
import traceback
import inspect
from .apierror import APIError, RequestIsNotJSON


def json_call(func):
    def wrapper():
        try:
            sig = inspect.signature(func)
            if len(sig.parameters) > 0:
                if not request.is_json:
                    raise RequestIsNotJSON
                jsn = request.json
                res = func(jsn)
            else:
                res = func()
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
