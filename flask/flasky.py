from app import create_app
from flask import request, jsonify, abort
from app.token import verify_token
from app.models import User, Role
from flask_login import login_user

app = create_app('dev')

no_login_request = []


def add_config():
    no_login_request.append('/user/login')
    no_login_request.append('/user/check_token')
    no_login_request.append('/user/upload_user_info_csv')
    # no_login_request.append('/user/download_import_user_template')


add_config()


@app.before_request
def check_token():
    # request.path
    if request.path in no_login_request:
        return
    form = request.form
    if form:
        cookie_token = form.get('token')
        cookie_id = form.get('user_id')
        if cookie_token:
            user_info_string = verify_token(cookie_token)
            user_id = int(user_info_string['user_id'])
            cookie_id = int(cookie_id)
            if user_id == cookie_id:
                user = User.load_user(user_id)
                if user:
                    login_user(user)
                    return
    abort(jsonify({'status': '203', 'message': '验证失败'}))