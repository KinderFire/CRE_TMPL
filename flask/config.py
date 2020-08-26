# import os
# basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """项目配置"""
    # 调试模式
    DEBUG = True

    # 配置日志
    LOG_LEVEL = "DEBUG"

    # mysql数据库配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/settl_mgt?charset=utf8'

    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 自动提交省去了每次 commit，添加数据对象后立马取 id 返回None
    # SQLALCHEMY_COMMIT_TEARDOWN = True

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False

    # 配置redis
    REDIS_HOST = '127.0.0.1'  # 项目上线以后，这个地址就会被替换成真实IP地址，mysql也是
    REDIS_PORT = 6379

    # 设置密钥
    SECRET_KEY = "ghUBljAa8uzw2afLqJ1XrukORJ4BlkTYJ1vaMuDh6opQ9uwGTAsDUyxcH62Aw3ju"

    # flask_session的配置信息
    # SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    # SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    # SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)  # 使用 redis 的实例
    # PERMANENT_SESSION_LIFETIME = 24 * 60 * 60  # session 的有效期，单位是秒


class DevelopementConfig(Config):
    """开发模式配置"""

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """生产模式下的配置"""
    DEBUG = False