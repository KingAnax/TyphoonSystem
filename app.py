from flask import Flask, render_template
from tools import MySQLTools

from user.query import user_query as user_query_blueprint
from user.change import user_news as user_news_blueprint
from user.chart import user_chart as user_chart_blueprint
from user import user as user_blueprint

# 初始化数据库
util = MySQLTools('localhost', 'root', '123456', 'hw', 'utf8')
# 初始化flask框架
app = Flask(__name__)

bike_id = ""
user_id = ""


@app.template_filter('slice')
def sub(str, start, end):
    return str[start: end]


# 登录界面路由
@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('./user/index.html')


# 注册蓝图
app.register_blueprint(user_query_blueprint, url_prefix='/user/query')
app.register_blueprint(user_news_blueprint, url_prefix='/user/change')
app.register_blueprint(user_chart_blueprint, url_prefix='/user/chart')
app.register_blueprint(user_blueprint, url_prefix='/user')

if __name__ == '__main__':
    app.run()
