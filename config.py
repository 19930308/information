import logging
from redis import StrictRedis


class Config(object):
    """项目文件配置"""

    # 设置密匙
    SECRET_KEY = "JF0dbTOmNuIiP7L0SJxdpHi7YB1Dr7mU2AshyKt9tGFzfSiXNva6DOhu237ZxxGX"

    # 连接mysql数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/news"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 设置session保存在redis数据库
    SESSION_TYPE = "redis"
    # 开启session签名
    SESSION_USE_SINGER = True
    # 指定session保存的数据库
    HOST = "127.0.0.1"
    PORT = "6379"
    # 该数据库为保存session值的
    SESSION_REDIS = StrictRedis(host=HOST, port=PORT)
    # 设置session为需要过期
    SESSION_PERMANATE = False
    # 设置过期时间
    PERMANATE_SESSION_LIFETIME = 86400 * 2
    # 设置log等级
    LOG_LEVEL=logging.DEBUG


class Development(Config):
    DEBUG = True


class Product(Config):
    DEBUG = False


class Test(Config):
    DEBUG = True
    TESTTING = True


config = {
    "development": Development,
    "product": Product,
    "test": Test
}
