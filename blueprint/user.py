from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from tables import User
from util import user_util, request_util, img_util, oss_util

bp = Blueprint("user", __name__, url_prefix = "/api")

# 修改密码
@bp.route('/update_pwd', methods = ['POST'])
@jwt_required()
def update_pwd():
    user_name = request.json.get('user_name')
    password = request.json.get('password')
    new_password = request.json.get('new_password')

    data = {
        "status": "no",
    }

    if not request_util.auth_args(user_name, password, new_password):
        data["data"]["msg"] = "参数不足"
        return jsonify(data)

    data = user_util.auth_password(password)
    if data['status'] != 'ok':
        return jsonify(data)

    user = user_util.get_user(user_name)

    if user_util.auth_user(user, password):
        if password == new_password:
            data["data"]["msg"] = "新密码和原密码不能相同"
            data["status"] = "no"
            return jsonify(data)

        user_util.update_pwd(user, new_password)
        data["status"] = "ok"
        data['data']['msg'] = '修改成功'
        return jsonify(data)
    else:
        data["data"]["msg"] = "用户名或密码错误"
        data["status"] = "no"
        return jsonify(data)

# 设置用户信息
@bp.route("/set_info", methods=["POST"])
@jwt_required()
def set_info():
    email = request.json.get("email")
    sex = request.json.get("sex")
    age = request.json.get("age")
    profile_code = request.json.get('profile')

    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if email:
        user.email = email
    if sex:
        user.sex = sex
    if age:
        user.age = age
    if profile_code:
        profile_data = img_util.base_to_bytes(profile_code)
        file_name = img_util.upload_profile(profile_data, user_id)
        user.profile = file_name

    db.session.commit()

    data = {
        "status": "ok"
    }

    return jsonify(data)

# 获取用户信息
@bp.route("/get_info", methods=['GET'])
@jwt_required()
def get_info():
    user_id = get_jwt_identity()

    data = {
        "data": {
            "msg": "身份验证失败",
            "info": dict()
        },
        "status": "no"
    }
    user = User.query.get(user_id)
    if user is None:
        return jsonify(data)

    profile_path = user.profile
    if profile_path:
        profile_path = f'{oss_util.get_host()}/profile/{profile_path}'

    data['data']['info'] = {
        "user_name": user.user_name,
        "email": user.email,
        "sex": user.sex,
        "age": user.age,
        "profile": profile_path
    }
    data['data']['msg'] = '获取成功'
    data['status'] = 'ok'
    return jsonify(data)