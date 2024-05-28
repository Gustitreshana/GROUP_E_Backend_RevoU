from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.utils.api_response import api_response

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user and user.role == role:
                return func(*args, **kwargs)
            else:
                return api_response(403, "Access forbidden: Admins only.", {})
        return wrapper
    return decorator