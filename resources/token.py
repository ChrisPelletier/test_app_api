import jwt
import sample_app.config as config
import time


def create_jwt(user):
    return jwt.encode({
        'iss': config.CLIENT_NAME,
        'exp': int(time.time()) + 86400,
        'nbf': int(time.time()),
        'username': user.username,
        'user_id': user.id
    }, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def decode_token(token):
    try:
        decoded_token = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        if decoded_token['iss'] != config.CLIENT_NAME:
            return {"error": "token not created by api"}
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"error": "expired_token"}
