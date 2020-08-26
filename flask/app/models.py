from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# from . import login_manager


class OptStats(db.Model):
    __tablename__ = 'opt_stats'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    longdate = db.Column(db.Integer, comment="日期")
    product = db.Column(db.String(64), comment="品种")
    cq_stats = db.Column(db.DECIMAL(20, 4), comment="cq占比")
    qr_stats = db.Column(db.DECIMAL(20, 4), comment="qr占比")
    qr_receive = db.Column(db.Integer, comment="总询价数量")
    qr_response = db.Column(db.Integer, comment="有效回应报价数量")


class FutStats(db.Model):
    __tablename__ = 'fut_stats'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    longdate = db.Column(db.Integer, comment="日期")
    symbol = db.Column(db.String(64), comment="合约")
    cq_stats = db.Column(db.DECIMAL(20, 4), comment="cq占比")
    p_value = db.Column(db.DECIMAL(20, 4), comment="P值")


class CumOptStats(db.Model):
    __tablename__ = 'cum_opt_stats'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    longdate = db.Column(db.Integer, comment="日期")
    product = db.Column(db.String(64), comment="品种")
    cq_stats = db.Column(db.DECIMAL(20, 4), comment="cq占比")
    qr_stats = db.Column(db.DECIMAL(20, 4), comment="qr占比")
    qr_receive = db.Column(db.Integer, comment="总询价数量")
    qr_response = db.Column(db.Integer, comment="有效回应报价数量")


class CqResult(db.Model):
    __tablename__ = 'cq_result'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    longdate = db.Column(db.Integer, comment="日期")
    symbol = db.Column(db.String(64), comment="合约")
    mm_legal = db.Column(db.DECIMAL(20, 4), comment="mm_legal")
    no_quote = db.Column(db.DECIMAL(20, 4), comment="no_quote")
    one_side = db.Column(db.DECIMAL(20, 4), comment="one_side")
    two_side = db.Column(db.DECIMAL(20, 4), comment="two_side")
    total_sec = db.Column(db.DECIMAL(20, 4), comment="total_sec")
    mm_legal_ptg = db.Column(db.DECIMAL(20, 4), comment="mm_legal_ptg")
    no_quote_ptg = db.Column(db.DECIMAL(20, 4), comment="no_quote_ptg")
    one_side_ptg = db.Column(db.DECIMAL(20, 4), comment="one_side_ptg")
    two_side_ptg = db.Column(db.DECIMAL(20, 4), comment="two_side_ptg")


class CumCqResult(db.Model):
    __tablename__ = 'cum_cq_result'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    longdate = db.Column(db.Integer, comment="日期")
    product = db.Column(db.String(64), comment="品种")
    mm_legal = db.Column(db.DECIMAL(20, 4), comment="mm_legal")
    no_quote = db.Column(db.DECIMAL(20, 4), comment="no_quote")
    one_side = db.Column(db.DECIMAL(20, 4), comment="one_side")
    two_side = db.Column(db.DECIMAL(20, 4), comment="two_side")
    total_sec = db.Column(db.DECIMAL(20, 4), comment="total_sec")
    mm_legal_ptg = db.Column(db.DECIMAL(20, 4), comment="mm_legal_ptg")
    no_quote_ptg = db.Column(db.DECIMAL(20, 4), comment="no_quote_ptg")
    one_side_ptg = db.Column(db.DECIMAL(20, 4), comment="one_side_ptg")
    two_side_ptg = db.Column(db.DECIMAL(20, 4), comment="two_side_ptg")


class Product(db.Model):
    __tablename__ = 'product'
    name = db.Column(db.String(64), primary_key=True, comment="主键品种名")
    under = db.Column(db.String(64), comment="under")
    type = db.Column(db.String(64), comment="type")
    currency = db.Column(db.String(64), comment="currency")
    exchange = db.Column(db.String(64), comment="exchange")
    exch_prod_sym = db.Column(db.String(64), comment="exch_prod_sym")
    mkt_rule = db.Column(db.String(64), comment="mkt_rule")
    delivery_type = db.Column(db.String(64), comment="delivery_type")


class Pnl(db.Model):
    __tablename__ = 'pnl'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    longdate = db.Column(db.Integer, comment="日期")
    product = db.Column(db.String(64), comment="品种")
    edge = db.Column(db.DECIMAL(20, 4), comment="edge")
    fwd = db.Column(db.DECIMAL(20, 4), comment="fwd")
    dist_fwd = db.Column(db.DECIMAL(20, 4), comment="dist_fwd")
    trdr_f_adj = db.Column(db.DECIMAL(20, 4), comment="trdr_f_adj")
    prem_f_adj = db.Column(db.DECIMAL(20, 4), comment="prem_f_adj")
    delta = db.Column(db.DECIMAL(20, 4), comment="delta")
    gamma = db.Column(db.DECIMAL(20, 4), comment="gamma")
    hist_vol = db.Column(db.DECIMAL(20, 4), comment="hist_vol")
    prof_vol = db.Column(db.DECIMAL(20, 4), comment="prof_vol")
    vadj_vol = db.Column(db.DECIMAL(20, 4), comment="vadj_vol")
    greek_vol = db.Column(db.DECIMAL(20, 4), comment="greek_vol")
    vol = db.Column(db.DECIMAL(20, 4), comment="vol")
    decay = db.Column(db.DECIMAL(20, 4), comment="decay")
    pos_dist = db.Column(db.DECIMAL(20, 4), comment="pos_dist")
    high_order = db.Column(db.DECIMAL(20, 4), comment="high_order")
    aggr = db.Column(db.DECIMAL(20, 4), comment="aggr")
    intl = db.Column(db.DECIMAL(20, 4), comment="intl")
    total = db.Column(db.DECIMAL(20, 4), comment="total")
    pnl_type = db.Column(db.String(64), comment="pnl_type")
    remark = db.Column(db.String(64), comment="remark")


class Settle(db.Model):
    __tablename__ = 'settle'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    longdate = db.Column(db.Integer, comment="日期")
    product = db.Column(db.String(64), comment="品种")
    settle_t = db.Column(db.DECIMAL(20, 2), comment="settle_t")
    settle_p = db.Column(db.DECIMAL(20, 2), comment="settle_p")
    settle_total = db.Column(db.DECIMAL(20, 2), comment="settle_total")
    intl_t = db.Column(db.DECIMAL(20, 2), comment="intl_t")
    intl_p = db.Column(db.DECIMAL(20, 2), comment="intl_p")
    intl_total = db.Column(db.DECIMAL(20, 2), comment="intl_total")
    cost_f = db.Column(db.DECIMAL(20, 2), comment="cost_f")
    cost_o = db.Column(db.DECIMAL(20, 2), comment="cost_o")
    exercise = db.Column(db.DECIMAL(20, 2), comment="exercise")


class Volume(db.Model):
    __tablename__ = 'volume'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    longdate = db.Column(db.Integer, comment="日期")
    product = db.Column(db.String(64), comment="品种")
    vol_mm = db.Column(db.Integer, comment="成交量")
    vol_market = db.Column(db.DECIMAL(20, 2), comment="市场成交量")
    vol_ptg = db.Column(db.DECIMAL(20, 4), comment="成交占比")


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    name = db.Column(db.String(64), comment="姓名")
    account = db.Column(db.String(64), unique=True, index=True, comment="账号")
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    # 用户状态
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    password_hash = db.Column(db.String(128), comment="密码")
    last_login_time = db.Column(db.String(64), default='')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('密码是不可读取的属性')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    @staticmethod
    def insert_admin():
        user = User()
        user.name = 'admin'
        user.account = 'root'
        user.role_id = 5
        user.password = '123456'
        db.session.add(user)
        db.session.commit()


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    name = db.Column(db.String(64), unique=True, comment="角色名")
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'Level_1': [Permission.FOLLOW, True],
            'Level_2': [Permission.FOLLOW, Permission.COMMENT, True],
            'Level_3': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, True],
            'Level_4': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, False],
            'Level_5': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN, False],
        }
        default_role = 'Level_2'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class Permission:
    FOLLOW = 1  # 浏览
    COMMENT = 2  # 评论
    WRITE = 4  # 添加数据
    MODERATE = 8  # 修改数据
    ADMIN = 16  # 管理
