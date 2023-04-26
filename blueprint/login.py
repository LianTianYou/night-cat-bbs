from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token
from util import user_util, request_util

bp = Blueprint("login", __name__, url_prefix = "/api")

# 登录
@bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    user_name = request.json.get("user_name")
    password = request.json.get("password")

    data = {
        "status": "no",
        "data": dict()
    }

    if not request_util.check_args(user_name, password):
        data["data"]["msg"] = "参数错误"
        return jsonify(data)

    user = user_util.get_user(user_name)
    if user_util.auth_user(user, password):
        user_id = user.user_id
        data["status"] = "ok"
        data["data"]["msg"] = "登录成功"
        token = create_access_token(identity = user_id)
        data["data"]["token"] = token
    else:
        data["data"]["msg"] = "用户名或密码错误"
        return jsonify(data)

    user_util.get_user_data(data, user)

    return jsonify(data)

# 注销
@bp.route("/logout", methods=["POST"])
def logout():
    data = {
        "status": "ok"
    }
    return jsonify(data)

# 注册
@bp.route("/signup", methods = ["POST"])
def signup():
    user_name = request.json.get("user_name")
    password = request.json.get("password")

    data = user_util.auth_signup(user_name, password)
    if data.get("status") == "ok":
        user_util.signup(user_name, password)
    return jsonify(data)