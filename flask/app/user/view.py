from . import user_blu
from .. import token, encoder
from app.models import *
from app.token import verify_token
from flask import render_template, request, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from ..decorators import permission_required
from .. import const
from sqlalchemy import and_, or_
import os
from werkzeug.utils import secure_filename
import csv


# 用户登入界面
# 用于用户登入，返回登入信息
@user_blu.route('/login', methods=['POST'])
def login():
    form = request.form
    if form:
        user = User.query.filter_by(account=form.get('account')).first()
        if user is None:
            return jsonify({'status': '403', 'message': '用户不存在'})
        if user.confirmed == 1:
            return jsonify({'status': '403', 'message': '您已被禁止登入,请联系管理人员'})
        if user.verify_password(form.get('password')):
            login_user(user)
            time_str = str(datetime.now()).split('.')[0]
            session_token = token.generate_auth_token(user.id, user.role_id, time_str)
            user.last_login_time = time_str
            try:
                e = encoder.MyEncoder()
                json_token = e.default(session_token)
                role = Role.query.filter_by(id=user.role_id).first()
                data = dict()
                data['id'] = user.id
                data['name'] = user.name
                data['account'] = user.account
                data['permissions'] = role.permissions
                data['role'] = role.name
                data['role_id'] = role.id
                data['token'] = json_token
                data['message'] = '登入成功'
                data['status'] = '200'
                data['last_login_time'] = time_str
                db.session.add(user)
                db.session.commit()
                return jsonify(data)
            except Exception as e:
                return jsonify({'status': '403', 'message': '登入失败', 'error': str(e)})
        return jsonify({'status': '403', 'message': '无效的用户名或密码'})
    return jsonify({'status': '403', 'message': '参数出错'})


# vue跳转前检查
# 用与页面跳转时检查token，不满足时浏览器删除cookie
@user_blu.route('/check_token', methods=['POST'])
def check_token():
    form = request.form
    if form:
        cookie_token = form.get('token')
        cookie_id = form.get('user_id')
        role_id = form.get('role_id')
        last_login_time = form.get('last_login_time')
        if cookie_token:
            user_info_string = verify_token(cookie_token)
            if int(user_info_string['user_id']) == int(cookie_id) and int(user_info_string['role_id']) == int(role_id):
                user = User.load_user(cookie_id)
                if user:
                    if user.confirmed == 1:
                        return jsonify({'status': '403', 'message': '您已被禁止登入,请联系管理人员'})
                    if user.last_login_time == last_login_time:
                        return jsonify({'status': '200', 'message': '验证通过'})
                    return jsonify({'status': '403', 'message': '同时只能在一个浏览器登入'})
                return jsonify({'status': '403', 'message': '未找到该用户'})
            return jsonify({'status': '403', 'message': '用户信息不符合'})
        return jsonify({'status': '403', 'message': 'token为空'})
    return (jsonify({'status': '203', 'message': '验证失败'}))


# 用户管理界面
# 用于获取当前所有用户信息
@user_blu.route('/find_all_user', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def find_all_user():
    form = request.form
    if form:
        keyword = const.Util.str_to_null(form.get('keyword'))
        filter_role = const.Util.str_to_null(form.get('filter_role'))
        page_index = int(const.Util.str_to_null(form.get('pageIndex')))
        page_size = int(const.Util.str_to_null(form.get('pageSize')))
        paginate = None
        if filter_role == '':
            paginate = User.query.filter(
                or_(User.name.like('%' + keyword + '%'), User.account.like('%' + keyword + '%'))
            ).paginate(page=page_index, per_page=page_size, error_out=False)
        elif filter_role == 'Level_0':
            paginate = User.query.filter(
                and_(or_(User.name.like('%' + keyword + '%'), User.account.like('%' + keyword + '%')), User.confirmed == True)
            ).paginate(page=page_index, per_page=page_size, error_out=False)
        else:
            role = Role.query.filter(Role.name == filter_role).first()
            paginate = User.query.filter(
                and_(or_(User.name.like('%' + keyword + '%'), User.account.like('%' + keyword + '%')), User.role_id == role.id)
            ).paginate(page=page_index, per_page=page_size, error_out=False)
        table_data = []
        for user in paginate.items:
            table_data.append(const.ModelsUtil.analysis_user(user))
        return jsonify({'status': '200', 'message': '查询成功', 'lis': table_data, 'total': paginate.total})
    return jsonify({'status': '403', 'message': '参数出错'})


# 用户管理界面
# 用于批量拉黑已选择的用户（批量）
@user_blu.route('/batch_blackout', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def batch_blackout():
    form = request.form
    if form:
        id_list = const.Util.lis_to_none(form.get('id_list'))
        user_list = User.query.filter(
            User.id.in_(id_list)
        ).all()
        message = '已拉黑用户'
        name_list = []
        try:
            for user in user_list:
                user.confirmed = True
                name_list.append(user.name)
                db.session.add(user)
            db.session.commit()
            message += str(name_list)
            return jsonify({'status': '200', 'message': message})
        except Exception as e:
            return jsonify({'status': '403', 'message': '批量拉黑出错', 'error': str(e)})
    return jsonify({'status': '403', 'message': '参数为空'})


# 用户管理界面
# 用于解除被拉黑的用户（单个）
@user_blu.route('/remove_blackout', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def remove_blackout():
    form = request.form
    if form:
        choose_id = const.Util.str_to_none(form.get('choose_id'))
        if choose_id is None:
            return jsonify({'status': '403', 'message': '未获取到该用户的ID'})
        user = User.query.filter(
            User.id == choose_id
        ).first()
        message = '已恢复用户'
        name_list = []
        try:
            if user is not None:
                user.confirmed = False
                name_list.append(user.name)
                db.session.add(user)
                db.session.commit()
                message += str(name_list)
                message += '的登入功能'
                return jsonify({'status': '200', 'message': message})
            else:
                return jsonify({'status': '403', 'message': '未找到ID为[{}]的用户'.format(choose_id)})
        except Exception as e:
            return jsonify({'status': '403', 'message': '批量拉黑出错', 'error': str(e)})
    return jsonify({'status': '403', 'message': '参数为空'})


# 用户管理界面
# 用于重置用户密码（单个）
@user_blu.route('/reset_password', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def reset_password():
    form = request.form
    if form:
        choose_id = const.Util.str_to_none(form.get('choose_id'))
        if choose_id is None:
            return jsonify({'status': '403', 'message': '未获取到该用户的ID'})
        user = User.query.filter(
            User.id == choose_id
        ).first()
        message = '已重置用户'
        name_list = []
        try:
            if user is not None:
                user.password = '{}@ddqh'.format(user.account)
                name_list.append(user.name)
                db.session.add(user)
                db.session.commit()
                message += str(name_list)
                message += '的密码，密码为账号加上@ddqh'
                return jsonify({'status': '200', 'message': message})
            else:
                return jsonify({'status': '403', 'message': '未找到ID为[{}]的用户'.format(choose_id)})
        except Exception as e:
            return jsonify({'status': '403', 'message': '重置用户密码出错', 'error': str(e)})
    return jsonify({'status': '403', 'message': '参数为空'})


# 用户管理界面
# 根据用户ID修改用户信息（单个）
@user_blu.route('/edit_user_by_id', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def edit_user_by_id():
    form = request.form
    if form:
        edit_id = const.Util.str_to_none(form.get('edit_id'))
        edit_name = const.Util.str_to_none(form.get('edit_name'))
        edit_account = const.Util.str_to_none(form.get('edit_account'))
        edit_role_name = const.Util.str_to_none(form.get('edit_role_name'))
        if edit_id is None:
            return jsonify({'status': '403', 'message': '未获取到该用户的ID'})
        user = User.query.filter(
            User.id == edit_id
        ).first()
        if user is None:
            return jsonify({'status': '403', 'message': '未找到ID为[{}]的用户'.format(edit_id)})
        user.name = edit_name
        user.account = edit_account
        role = Role.query.filter(Role.name == edit_role_name).first()
        if role is None:
            return jsonify({'status': '403', 'message': '未找到名称为[{}]的权限'.format(edit_role_name)})
        user.role = role
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'status': '200', 'message': '修改成功'})
        except Exception as e:
            return jsonify({'status': '403', 'message': '修改失败', 'error': str(e)})
    return jsonify({'status': '403', 'message': '参数为空'})


# 用户管理界面
# 根据用户信息添加用户信息（单个）
@user_blu.route('/add_user', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def add_user():
    form = request.form
    if form:
        add_name = const.Util.str_to_none(form.get('add_name'))
        add_account = const.Util.str_to_none(form.get('add_account'))
        add_role_name = const.Util.str_to_none(form.get('add_role_name'))
        role = Role.query.filter(Role.name == add_role_name).first()
        if role is None:
            return jsonify({'status': '403', 'message': '未找到名称为[{}]的权限'.format(add_role_name)})
        try:
            u = User()
            u.name = add_name
            u.account = add_account
            u.role = role
            u.password = '{}@ddqh'.format(add_account)
            db.session.add(u)
            db.session.commit()
            return jsonify({'status': '200', 'message': '添加成功'})
        except Exception as e:
            return jsonify({'status': '403', 'message': '添加失败', 'error': str(e)})
    return jsonify({'status': '403', 'message': '参数为空'})


# 用户管理界面
# 接受上传的用户表CSV，解析后返回用户数据给前端
@user_blu.route('/upload_user_info_csv', methods=['GET', 'POST'])
def upload_user_info_csv():
    form = request.files['file']
    if form:
        # basepath = os.path.abspath(os.path.dirname(__file__))
        basepath = os.path.abspath(r'.')
        basepath = os.path.join(basepath, 'temp/user')
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        filename = secure_filename(form.filename)
        upload_path = os.path.join(basepath, filename)
        form.save(upload_path)
        try:
            data_list = []
            with open(upload_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if str(row[0]).strip() == '用户名':
                        continue
                    lis = dict()
                    lis['username'] = str(row[0]).strip()
                    lis['account'] = str(row[1]).strip()
                    lis['role_name'] = str(row[2]).strip()
                    data_list.append(lis)
            return jsonify({'status': '200', 'message': '解析成功', 'list': data_list})
        except Exception as e:
            return jsonify({'status': '200', 'message': '解析文件失败', 'error': str(e)})
    return jsonify({'status': '403', 'message': '文件上传失败'})


# 用户管理界面
# 根据解析的CSV数据进行用户信息导入
# 这段代码可以优化查询次数但我觉得没必要，毕竟不是经常操作的代码
# 一般一次就够了，我只是用来测一下，需要怎样布局而已
@user_blu.route('/import_user_info', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def import_user_info():
    form = request.form
    if form:
        upload_data = const.Util.str_to_none(form.get('upload_data'))
        if upload_data is not None:
            upload_data = eval(upload_data)
        else:
            upload_data = []
        try:
            for line in upload_data:
                u = User.query.filter(User.account == line['account']).first()
                if u is None:
                    u = User()
                u.name = line['username']
                u.account = line['account']
                role = Role.query.filter(Role.name == line['role_name']).first()
                if role is None:
                    return jsonify({'status': '403', 'message': '未找到名称为[{}]的权限'.format(line['role_name'])})
                else:
                    u.role = role
                u.password = '{}@ddqh'.format(line['account'])
                db.session.add(u)
            db.session.commit()
            return jsonify({'status': '200', 'message': '添加成功'})
        except Exception as e:
            return jsonify({'status': '403', 'message': '添加失败', 'error': str(e)})
    return jsonify({'status': '403', 'message': '参数为空'})


# 用户管理界面
# 下载导入用户的CSV模板
@login_required
@permission_required(Permission.WRITE)
@user_blu.route('/download_import_user_template', methods=['GET', 'POST'])
def download_import_user_template():
    # 路径
    basepath = os.path.abspath(os.path.dirname(__file__))
    basepath = os.path.join(basepath, '../templates/csv')
    # 传输
    response = send_from_directory(basepath, 'import_user_template.csv', as_attachment=True)
    response.headers["Access-Control-Expose-Headers"] = "Content-disposition"
    return response