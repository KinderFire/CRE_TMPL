from .models import *

# 这里是变量
class Const:
    pass


class Util:

    @staticmethod
    def str_to_none(_str):
        if _str is None:
            return _str
        if str(_str).strip() == '':
            return None
        else:
            return str(_str).strip()

    @staticmethod
    def str_to_null(_str):
        if _str is None:
            return ''
        else:
            return str(_str).strip()

    @staticmethod
    def lis_to_none(_lis):
        if _lis is None:
            return []
        else:
            return _lis


class ModelsUtil:

    @staticmethod
    def analysis_user(user):
        data = {}
        data['id'] = user.id
        data['name'] = user.name
        data['account'] = user.account
        data['member_since'] = str(user.member_since)
        if user.confirmed:
            data['confirmed'] = '已被拉黑'
        else:
            data['confirmed'] = '正常'
        data['role_name'] = user.role.name
        data['last_login_time'] = user.last_login_time
        return data
