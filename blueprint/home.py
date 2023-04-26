from flask import Blueprint, jsonify

from tables import Post, User
from util import value_util, post_util

bp = Blueprint('home', __name__, url_prefix = '/api')

@bp.route('/get_recommend', methods = ['GET'])
def get_recommend():
    data = {
        "data": {
            "items": []
        },
        "status": "no"
    }

    posts = Post.query.order_by(Post.post_id.desc()).limit(10).all()
    data['data']['items'] = post_util.get_recommend_posts(posts)
    data['status'] = 'ok'

    return jsonify(data)