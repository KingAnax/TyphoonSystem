from flask import render_template, Blueprint, request, jsonify
from tools import MySQLTools

user_chart = Blueprint('user_chart', __name__)
# 初始化数据库
util = MySQLTools('localhost', 'root', '123456', 'hw', 'utf8')


@user_chart.route('/map', methods=['GET', 'POST'])
def trajectory():
    return render_template("/user/chart/map.html", value=0)


@user_chart.route('/pie', methods=['GET', 'POST'])
def pie():
    n1, n2, n3, n4, n5, n6 = util.numStatic()
    return render_template("/user/chart/pie.html",
                           n1=n1, n2=n2, n3=n3, n4=n4, n5=n5, n6=n6)


@user_chart.route('/query', methods=['GET', 'POST'])
def ty_query():
    if request.method == "POST":
        form = request.form
        tynm = form.get('myty')
        if tynm:
            util.drawMap(tynm)
        return render_template("/user/chart/map.html", value=1)
    return render_template("/user/chart/map.html", value=0)
