from . import index_blue

# 利用蓝图创建视图函数
@index_blue.route('/')
def index():

    return 'good'
