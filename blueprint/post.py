from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from tables import Post, PostImages
from util import img_util, oss_util, request_util

bp = Blueprint('post', __name__, url_prefix = '/api')


def commit_post_images(images : list, post_id : int):
    for number, img in enumerate(images, start = 1):
        img_data = img_util.base_to_bytes(img)
        img_name = img_util.upload_post_image(img_data, post_id = post_id, order_number = number)
        post_images = PostImages(img_name=img_name, post_id=post_id, order_number=number)
        db.session.add(post_images)
    db.session.commit()

# 发布帖子
@bp.route('/submit_post', methods = ['POST'])
@jwt_required()
def submit_post():
    data = {
        'data': {
            'msg': '发布成功'
        },
        "status": "ok"
    }

    title = request.json.get('title')
    content = request.json.get('content')

    if not request_util.auth_args(title, content):
        data['data']['msg'] = '参数错误'
        data['status'] = 'no'
        return jsonify(data)

    images = request.json.get('images')
    poster_id = get_jwt_identity()

    post = Post(title = title, content = content, poster_id = poster_id)
    db.session.add(post)
    db.session.commit()

    if images:
        commit_post_images(images, post.post_id)
    return jsonify(data)

# 获取帖子内容
@bp.route("/get_post", methods = ["GET"])
def get_post():
    post_id = request.json.get("post_id")
    post = Post.query.get(post_id)

    data = {
        "data": {
            "msg": "获取成功"
        },
        "status": "ok"
    }

    if not post:
        data['data']['msg'] = '获取的帖子不存在'
        data['status'] = "no"
        return jsonify(data)

    data['data']['title'] = post.title
    data['data']['content'] = post.content

    post_images = PostImages.query.filter_by(post_id=post_id).order_by(PostImages.order_number).all()

    images = []
    for image in post_images:
        image_urls = f'{oss_util.get_host()}/post_image/{image.img_name}'
        images.append(image_urls)

    data['data']['images'] = images

    return jsonify(data)

@bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    post_list = Post.query.filter(Post.title.like(f'%{keyword}%')).all()
    data = {
        "data": {},
        "status": "ok"
    }
    return ""