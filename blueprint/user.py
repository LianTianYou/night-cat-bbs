from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from tables import User, Follow, Post
from util import user_util, request_util, img_util, oss_util, value_util, post_util, response_util

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

    if not request_util.check_args(data, user_name, password, new_password):
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

def update_profile(profile_code, user : User):
    old_file_name = user.profile
    if old_file_name:
        oss_util.delete_file(f'profile/{old_file_name}')

    profile_data = img_util.base_to_bytes(profile_code)
    file_name = img_util.upload_profile(profile_data, user.user_id)
    user.profile = file_name

# 设置用户信息
@bp.route("/set_info", methods=["POST"])
@jwt_required()
def set_info():
    email = request.json.get("email")
    user_name = request.json.get("user_name")
    sex = request.json.get("sex")
    age = request.json.get("age")
    profile_code = request.json.get('profile')
    user_desc = request.json.get('user_desc')

    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if user_name:
        user.user_name = user_name
    if email:
        user.email = email
    if sex:
        user.sex = sex
    if age:
        user.age = age
    if profile_code:
        update_profile(profile_code, user)
    if user_desc:
        user.user_desc = user_desc

    db.session.commit()

    data = {
        "data": {
            "msg": "修改成功"
        },
        "status": "ok"
    }
    data = user_util.get_user_data(data, user)

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

    data = user_util.get_user_data(data, user)

    data['data']['msg'] = '获取成功'
    data['status'] = 'ok'
    return jsonify(data)

def add_follow(user : User, target_user : User):
    user.follow_count += 1
    target_user.fans_count += 1

def unfollow(user : User, target_user : User):
    if user.follow_count and target_user.fans_count:
        user.follow_count -= 1
        target_user.fans_count -= 1
@bp.route('/set_follow', methods=['POST'])
@jwt_required()
def set_follow():
    data = {
        "data": {
            "msg": "关注成功"
        },
        "status": "ok"
    }

    user_id = get_jwt_identity()
    target_id = request.json.get('target_id')

    if not request_util.check_args(data, target_id):
        return jsonify(data)

    user = User.query.get(user_id)
    target_user = User.query.get(target_id)
    if not target_user:
        data['data']['msg'] = '关注的用户不存在'
        data['status'] = 'no'
        return jsonify(data)

    follow = Follow.query.filter_by(user_id=user_id, target_id=target_id).first()
    if not follow:
        follow = Follow(user_id=user_id, target_id=target_id)
        add_follow(user, target_user)
        db.session.add(follow)
    else:
        unfollow(user, target_user)
        data['data']['msg'] = '取消关注'
        db.session.delete(follow)
    db.session.commit()

    return jsonify(data)

@bp.route('/get_my_post')
@jwt_required()
def get_my_post():
    data = response_util.load_data('获取失败')
    user_id = get_jwt_identity()

    posts = Post.query.filter_by(user_id=user_id).all()
    post_list = post_util.get_posts(posts)

    data['data']['items'] = post_list

    response_util.set_ok(data, '获取成功')

    return jsonify(data)