from flask import Flask
from flask.ext.session import Session
from flask.ext.wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config import config

# 初始化mysql数据库
db = SQLAlchemy()
redis_store = None


def create_app(config_name):
    # 创建flask实例对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])
    # 设置redis_store为全局变量
    global redis_store
    # db关联app,真正初始化
    db.init_app(app)
    # 初始化redis数据库
    redis_store = StrictRedis(host=config[config_name].HOST, port=config[config_name].PORT)
    # 开启CSRF保护
    CSRFProtect(app)
    # 设置session保存位置
    Session(app)
    return app
