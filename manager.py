from flask import Flask
from flask.ext.session import Session
from flask.ext.wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from config import Config

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
# 集成flask_script，插入脚本
manager=Manager(app)
# 设置数据库迁移命令
Migrate(app,db)
manager.add_command('db',MigrateCommand)


@app.route('/')
def index():
    return 'good'


if __name__ == '__main__':
    manager.run()
