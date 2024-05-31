from flask import render_template, request, redirect, url_for, session, Blueprint
from tools import MySQLTools

user_news = Blueprint('user_change', __name__)
# 初始化数据库
util = MySQLTools('localhost', 'root', '123456', 'hw', 'utf8')


@user_news.route("/ty_create", methods=['GET', 'POST'])
def news_create():
    if request.method == "POST":
        form = request.form
        ty_no = form.get('ty_no')
        name = form.get('name')
        util.addTy(ty_no, name)
        return redirect(url_for('user.index'))
    return render_template("/user/change/ty_create.html")
