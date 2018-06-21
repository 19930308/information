from flask import current_app
from flask import render_template

from . import index_blue

# 利用蓝图创建视图函数
# 主页
@index_blue.route('/')
def index():
    return render_template('index.html')

# 加载图标
@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('/news/favicon.ico')