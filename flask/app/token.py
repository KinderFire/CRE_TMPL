from itsdangerous import BadTimeSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import abort, jsonify
from config import Config

APP_SECRET_KEY = Config.SECRET_KEY
MAX_TOKEN_AGE = 3600*12
token_generator = Serializer(APP_SECRET_KEY, expires_in=MAX_TOKEN_AGE)


def generate_auth_token(user_id, role_id, login_time):
    access_token = token_generator.dumps({'user_id': user_id, 'role_id': role_id, 'login_time': login_time})
    return access_token


def verify_token(token):
    user_info = None
    try:
        user_info = token_generator.loads(token)
    except SignatureExpired as e:
        abort(jsonify({'status': '401', 'message': '登入过期'}))
    except BadTimeSignature as e:
        abort(jsonify({'status': '401', 'message': '登入时间到期'}))
    except:
        abort(jsonify({'status': '401', 'message': '解析token出错'}))
    return user_info