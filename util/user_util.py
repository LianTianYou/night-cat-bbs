from flask_jwt_extended import create_access_token
from tables import User
from db import db
from util import img_util, value_util


def get_user(user_name : str) -> User:
    return User.query.filter_by(user_name = user_name).first()

def auth_user(user : User, password : str) -> bool:
    if user and user.password == password:
        return True
    return False
def get_user_id(user_name, password) -> int:
    user = get_user(user_name)
    if user and user.password == password:
        return user.id
    return -1

def auth_signup(user_name, password) -> dict:
    result = {
        "status": "no",
        "data": {
            "msg": "注册失败"
        }
    }
    if len(user_name) < 4:
        result["data"]["msg"] = "用户名位数不足"
    if len(password) < 4:
        result["data"]["msg"] = "密码位数不足"
    user = get_user(user_name)
    if not user:
        result["data"]["msg"] = "注册成功"
        result["status"] = "ok"
    else:
        result["data"]["msg"] = "用户名已存在"
    return result

def auth_password(password) -> dict:
    result = {
        "status": "no",
        "data": {
            "code": 400,
        }
    }
    if len(password) < 4:
        result["data"]["msg"] = "密码长度不足"
    else:
        result["data"]["code"] = 200
        result["status"] = "ok"
    return result

def signup(user_name, password):
    user = User(user_name = user_name, password = password)
    db.session.add(user)
    db.session.commit()

def update_pwd(user : User, new_password : str):
    user.password = new_password
    db.session.commit()

def create_token(user_id):
    token = create_access_token(identity = user_id)
    return token

def get_user_data(data : dict, user : User) -> dict:
    profile_url = user.profile
    if profile_url:
        profile_url = img_util.get_profile_url(profile_url)

    data['data']['info'] = {
        "user_name": user.user_name,
        "email": user.email,
        "sex": user.sex,
        "age": user.age,
        "follow_count": user.follow_count,
        "fans_count": user.fans_count,
        "profile": profile_url
    }
    return data