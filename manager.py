from flask import Flask
from flask.ext.session import Session
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

    # 设置session保存在redis数据库
    SESSION_TYPE="redis"
    # 开启session签名
    SESSION_USE_SINGER=True
    # 指定session保存的数据库
    HOST="127.0.0.1"
    PORT="6379"
    SESSION_REDIS=StrictRedis(host=HOST,port=PORT)
    # 设置session为需要过期
    SESSION_PERMANATE=False
    # 设置过期时间
    SESSION_LIFETIME=86400*2


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
# 设置session保存位置
Session(app)


@app.route('/')
def index():
    return 'good'


if __name__ == '__main__':
    app.run(debug=True)
