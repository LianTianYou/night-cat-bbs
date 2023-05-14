from flask import Blueprint, request, jsonify
from db import db
from tables import LastAccess, Like
from util import msg_util, request_util, response_util
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token

bp = Blueprint('msg', __name__, url_prefix='/api')

# @bp.route('/get_msg')
# @jwt_required
# def get_msg():
    # msg = msg_util.get_msg()
    # return msg

@bp.route('/add_access', methods=['POST'])
@jwt_required
def set_access():
    data = response_util.load_data()
    msg_type = request.json.get('msg_type')

    if not request_util.check_args(data, msg_type):
        return jsonify(data)

    last_access = LastAccess.query.filter_by(msg_type=msg_type).first()
    if msg_type == 'like':
        last = Like.query.order_by(Like.like_id.desc()).first()
        if last:
            last_access.last_id = last.like_id
    db.session.commit()

    data['data']['body'] = last_access.last_id
    response_util.set_ok(data)

    return jsonify(data)