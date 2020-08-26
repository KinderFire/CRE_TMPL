from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ProductionConfig, DevelopementConfig
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from flask_migrate import Migrate
from flask_login import LoginManager
import flask.json
import decimal

db = SQLAlchemy()

config = {
    "dev": DevelopementConfig,
    "prod": ProductionConfig,
}


def setup_log(Config):
    # 设置日志的记录等级
    logging.basicConfig(level=Config.LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 300, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flaskapp使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# class MyJSONEncoder(flask.json.JSONEncoder):
#
#     def default(self, obj):
#         if isinstance(obj, decimal.Decimal):
#             # Convert decimal instances to strings.
#             return str(obj)
#         return super(MyJSONEncoder, self).default(obj)


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])

    setup_log(config[config_name])

    db.init_app(app)

    # app.json_encoder = MyJSONEncoder

    # migrate = Migrate(app, db)
    Migrate(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    from .index import index_blu
    app.register_blueprint(index_blu, url_prefix='')

    from .user import user_blu
    app.register_blueprint(user_blu, url_prefix='/user')

    return app

