from flask import render_template, Flask, request, url_for, session, flash, g
from werkzeug.utils import redirect
from py2neo import *
import listTodire
import recommend
import verify
import RWData

# 连接到neo4j数据库
graph = Graph("http://localhost:7474/", auth=("neo4j", "12520123"))

app = Flask(__name__)
app.config["SECRET_KEY"] = '12520123.abc'


# 直接返回至首页
@app.route("/")
def back_home():
    return redirect(url_for("home"))


# 首页的实现
@app.route('/home', methods=["GET", "POST"])
def home():
    # 根据用户信息实现网页的个性化的推荐页面
    # 随机取6个节点信息
    n_random = recommend.recommendRandom(6)
    # 获取12个新番信息
    n_xinfan = recommend.recommendXinfan(12)
    # 获取6个个性化节点信息
    n_gexin = []
    if g.user:
        n_gexin = recommend.recommendPersonality(g.user, 6)
    animation_info_gexin = listTodire.listToDireAnima(n_gexin, filter_tags=True)
    animation_info_random = listTodire.listToDireAnima(n_random, filter_tags=True)
    animation_info_xinfan = listTodire.listToDireAnima(n_xinfan, filter_tags=True)
    # 整合所有的信息
    all_info = {
        "username": g.user,
        "gexin": animation_info_gexin,
        "xinfan": animation_info_xinfan,
        "random": animation_info_random
    }
    return render_template("drama_home.html", **all_info)


# 动画详情页的实现以
@app.route("/animation/<string:animation_id>", methods=["GET", "POST"])
def animation_detail(animation_id):
    # 获取该动画的所有信息
    n = RWData.readAnimationInfo(animation_id)
    animation_info = listTodire.listToDireAnima(n)
    # 获取用户与该动画的评分信息
    score = RWData.readScore(g.user, animation_info["ID"][0])
    all_info = {
        "score": score,
        "animation_info": animation_info
    }
    return render_template("animation_detail.html", **all_info)


# 用户评分的写入
@app.route("/animation", methods=["GET"])
def animation():
    if request.method == "GET":
        score = request.args.get("score")
        aID = request.args.get("aID")
        RWData.writeScore(g.user, aID, score)


# 注册的实现
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("drama_register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        # 先检验用户名是否在数据库中
        if not verify.userExistVerify(username):
            # 再检验密码与重复密码是否相同
            if password == repeat_password:
                # 保存用户数据，写入数据库
                RWData.writeUser(username, password)
                # 并且直接登录保存用户的登录状态
                session["username"] = username
                return redirect("home")
            else:
                flash("请确认两次密码输入完全一样！")
                return redirect(url_for("register"))
        else:
            flash("该用户名已存在！")
            return redirect(url_for("register"))


# 登录页的实现
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("drama_login.html")
    else:
        # 从前端获取用户信息
        username = request.form.get("username")
        password = request.form.get("password")
        # 校验用户是否在数据库中存在
        if verify.passwordVerify(username, password):
            # 登录成功跳转至首页，并保存用户的登录状态
            session["username"] = username
            return redirect(url_for("home"))
        else:
            flash("用户名和密码不匹配！")
            return redirect(url_for("login"))


# 搜索页的实现
@app.route("/search")
def search():
    if request.method == "GET":
        keyword = request.args.get("wd")
        n = RWData.readSearchData(keyword)
        animationInfo = listTodire.listToDireAnima(n, filter_tags=True)
        all_Info = {
            "animation": animationInfo,
            "keyword": keyword
        }
        return render_template("search.html", **all_Info)


# 注销
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# 钩子函数
@app.before_request
def before_request():
    username = session.get("username")
    if username:
        g.user = username
    else:
        g.user = None


# 上下文处理器
@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run(port=6000)
