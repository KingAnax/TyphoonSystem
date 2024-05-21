from flask import render_template, request, session, jsonify, Blueprint
from tools import MySQLTools

user_query = Blueprint('user_query', __name__)
# 初始化数据库
util = MySQLTools('localhost', 'root', '123456', 'hw', 'utf8')


@user_query.route('/basic', methods=['GET', 'POST'])
def basic():
    return render_template("/user/query/basic_query.html")


@user_query.route('/addition', methods=['GET', 'POST'])
def addition():
    return render_template("/user/query/addition_query.html")


@user_query.route('/move', methods=['GET', 'POST'])
def move():
    return render_template("/user/query/move_query.html")


@user_query.route('/getbd', methods=['POST', 'GET'])
def get_basic_data():
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)
        offset = info.get('offset', 0)
        bd = util.basicInfo()
        return jsonify({'total': len(bd), 'rows': bd[int(offset): (int(offset) + int(limit))]})


@user_query.route('/get_ad', methods=['POST', 'GET'])
def get_addition_data():
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)
        offset = info.get('offset', 0)
        ad = util.additionInfo()
        return jsonify({'total': len(ad), 'rows': ad[int(offset): (int(offset) + int(limit))]})


@user_query.route('/movedata', methods=['POST', 'GET'])
def rent_data():
    form = request.form
    tynm = form.get('ty')
    if tynm:
        global md
        md = util.moveInfo(tynm)
    return render_template("/user/query/move_query.html")


@user_query.route('/getmd', methods=['POST', 'GET'])
def get_move_data():
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)
        offset = info.get('offset', 0)
        global md
        return jsonify({'total': len(md), 'rows': md[int(offset): (int(offset) + int(limit))]})


