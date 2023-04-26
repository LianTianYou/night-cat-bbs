from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from tables import Post, PostImages, User, Like, Comment
from util import img_util, oss_util, request_util, post_util, value_util

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

    if not request_util.check_args(title, content):
        data['data']['msg'] = '参数错误'
        data['status'] = 'no'
        return jsonify(data)

    images = request.json.get('images')
    user_id = get_jwt_identity()

    post = Post(title = title, content = content, user_id = user_id)
    db.session.add(post)
    db.session.commit()

    if images:
        commit_post_images(images, post.post_id)
    return jsonify(data)

# 获取帖子内容

@bp.route("/get_post", methods = ["GET"])
def get_post():
    data = {
        "data": {
            "msg": "获取成功"
        },
        "status": "ok"
    }

    post_id = request.args.get("post_id")
    if not request_util.check_args(post_id):
        data['data']['msg'] = '参数错误'
        data["status"] = "no"
        return jsonify(data)

    post_id = int(post_id)
    post = Post.query.get(post_id)

    if not post:
        data['data']['msg'] = '获取的帖子不存在'
        data['status'] = "no"
        return jsonify(data)

    data['data']['body'] = post_util.get_post_data(post)

    return jsonify(data)

# 搜索帖子
@bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    post_list = Post.query.filter(Post.title.like(f'%{keyword}%')).all()

    post_dicts = []

    for post in post_list:
        post_dict = {
            "post_id": post.post_id,
            "title": post.title
        }
        post_dicts.append(post_dict)

    data = {
        "data": {
            "list": post_dicts,
            "msg": "搜索成功"
        },
        "status": "ok"
    }

    if not post_dicts:
        data["data"]["msg"] = "结果为空"
        data["status"] = "no"

    return jsonify(data)

# 点赞
@bp.route('/like', methods = ['POST'])
@jwt_required()
def like():
    data = {
        "data": dict(),
        "status": "ok"
    }

    post_id = request.json.get('post_id')
    user_id = get_jwt_identity()

    if not request_util.check_args(post_id):
        data["data"]["msg"] = "参数错误"
        data["status"] = "no"
        return jsonify(data)

    like = Like.query.filter_by(post_id=post_id, user_id=user_id).first()
    post = Post.query.get(post_id)

    if like:
        data["data"]["msg"] = "取消点赞"
        db.session.delete(like)
        post.like_count -= 1
    else:
        like = Like(post_id = post_id, user_id = user_id)
        data["data"]["msg"] = "点赞成功"
        post.like_count += 1
        db.session.add(like)
    db.session.commit()

    return jsonify(data)

# 添加评论
@bp.route('/add_comment', methods = ['POST'])
@jwt_required()
def add_comment():
    data = {
        "data": {
            "msg": "提交成功"
        },
        "status": "ok"
    }

    post_id=request.json.get('post_id')
    content=request.json.get('content')
    user_id=get_jwt_identity()

    if not request_util.check_args(post_id, content):
        data['data']['msg'] = '参数错误'
        return jsonify(data)

    comment = Comment(post_id=post_id, user_id=user_id, content=content)

    db.session.add(comment)
    db.session.commit()

    return jsonify(data)

# 获取评论
@bp.route('/get_comment', methods = ['GET'])
def get_comment():
    data = {
        "data": {
            "msg": "获取成功"
        },
        "status": "ok"
    }

    post_id = request.json.get('post_id')

    if not request_util.check_args(post_id):
        data['data']['msg'] = '参数错误'
        data['status'] = 'no'

    comments = Comment.query.filter_by(post_id=post_id).all()
    comment_list = []

    if not comments:
        data['data']['msg'] = '该帖子不存在'
        data['status'] = 'no'
        return jsonify(data)

    for comment in comments:
        comment_dict = dict()
        comment_dict['content'] = comment.content
        comment_dict['user_id'] = comment.user_id
        comment_list.append(comment_dict)

    data['data']['items'] = comment_list

    return jsonify(data)