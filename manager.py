from flask import Flask
from flask.ext.wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis


class Config(object):
    """项目文件配置"""
    DEBUG = True
    # 设置密匙
    SECRET_KEY = "JF0dbTOmNuIiP7L0SJxdpHi7YB1Dr7mU2AshyKt9tGFzfSiXNva6DOhu237ZxxGX"
    # 连接mysql数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:6379/news"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 创建flask实例对象
app = Flask(__name__)
# 加载配置
app.config.from_object(Config)
# 初始化mysql数据库
db = SQLAlchemy(app)
# 初始化redis数据库
redis_store = StrictRedis(host='127.0.0.1', port='6379')
# 开启CSRF保护
CSRFProtect(app)


@app.route('/')
def index():
    return 'good'


if __name__ == '__main__':
    app.run(debug=True)
