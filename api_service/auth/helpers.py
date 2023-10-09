from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from api_service.sqlite_util import is_user_available


def authorize_user(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        if is_user_available(current_user):
            return fn(*args, **kwargs)
        else:
            return jsonify(message='Unauthorized User'), 401

    return decorated_function
