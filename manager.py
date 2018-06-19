
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from info import app, db

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
