from flask import Blueprint, request, jsonify, session

bp = Blueprint("pages", __name__, url_prefix = "/api")

def auth_login(user, pwd):
    USER = "root"
    PWD = "root"
    if USER == user and PWD == pwd:
        return 1
    else:
        return None

# 登录
@bp.route('/login', methods=['POST'])
def login():
    user = request.json.get("user")
    pwd = request.json.get("pwd")

    data = {
        "status": "no"
    }
    user_id = auth_login(user, pwd)
    print(user_id)
    if not user_id is None:
        data["status"] = "ok"
        session["user_id"] = user_id
    return jsonify(data)

# 注销
@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    data = {
        "status": "ok"
    }
    return jsonify(data)

# 注册
@bp.route("/signup", methods=["POST"])
def signup():
    user = request.json.get("user")
    pwd = request.json.get("pwd")
    data = {
        "status": "no"
    }
    if user and pwd:
        data["status"] = "ok"
    return jsonify(data)