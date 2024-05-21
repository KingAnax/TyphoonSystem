from flask import render_template, flash, request, redirect, url_for, session, jsonify, Blueprint
from tools import MySQLTools

user = Blueprint('user', __name__)
# 初始化数据库
util = MySQLTools('localhost', 'root', '123456', 'hw', 'utf8')


# 主页
@user.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("/user/index.html")


@user.route('/prequery', methods=['GET', 'POST'])
def query_data():
    data = util.ty_min()
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)
        offset = info.get('offset', 0)
    return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
