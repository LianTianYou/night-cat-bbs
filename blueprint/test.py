import datetime
import base64
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, decode_token, get_jwt_identity
from util import img_util
from util.request_util import jwt

bp = Blueprint("test", __name__, url_prefix = "/test")

@bp.route('/get_token')
def get_token():
    sec = request.form.get('sec')
    if sec:
        sec = int(sec)
    else:
        sec = 600
    user_name = 1
    token = create_access_token(identity = user_name, expires_delta=datetime.timedelta(seconds = sec))

    data = {
        "token": token
    }

    return jsonify(data)

@bp.route('/use_token')
@jwt_required()
def use_token():
    jwt_data = get_jwt()
    if jwt_data:
        return jsonify(jwt_data)
    else:
        return jsonify({"msg": "未登录"})

@bp.route('/up_file', methods=['POST', 'PUT'])
def get_file():
    # print(request.data)
    # print("=======================================================")
    # print(request.form)
    # print("=======================================================")
    # print(request.files)
    # print("=======================================================")
    file = request.json.get('file')
    file_data = img_util.base_to_bytes(file)
    with open('11.jpg', 'bw') as f:
        f.write(file_data)
    print(file_data)
    print(request.json.get('user_name'))
    return "ok"