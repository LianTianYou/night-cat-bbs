import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from db import db
from tables import Post, PostImages, User, Like, Comment, History
from util import img_util, oss_util, request_util, post_util, value_util, user_util, response_util

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

    if not request_util.check_args(data, title, content):
        return jsonify(data)

    images = request.json.get('images')
    user_id = get_jwt_identity()

    post = Post(title = title, content = content, user_id = user_id)
    db.session.add(post)
    db.session.commit()

    if images:
        commit_post_images(images, post.post_id)
    return jsonify(data)

@bp.route('/update_post', methods=['POST'])
@jwt_required()
def update_post():
    data = {
        'data': {
            'msg': '修改失败'
        },
        'status': 'no'
    }

    post_id = request.json.get('post_id')
    post = Post.query.get(post_id)

    title = request.json.get('title')
    content = request.json.get('content')

    images = request.json.get('images')

    if title:
        post.title = title
    if content:
        post.content = content
    if images:
        post.images = images

    db.session.commit()
    data['data']['body'] = post_util.get_post_data(post)

    response_util.set_ok(data, '修改成功')
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
    if not request_util.check_args(data, post_id):
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
    posts = Post.query.filter(Post.title.like(f'%{keyword}%')).all()

    data = {
        "data": {
            "items": [],
            "msg": "结尾为空"
        },
        "status": "no"
    }

    if posts:
        data['data']['items'] = post_util.get_posts(posts)
        data["data"]["msg"] = "搜索成功"
        data["status"] = "ok"

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

    if not request_util.check_args(data, post_id):
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

    if not request_util.check_args(data, post_id, content):
        return jsonify(data)

    comment = Comment(post_id=post_id, user_id=user_id, content=content)

    post = Post.query.get(post_id)
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

    if not request_util.check_args(data, post_id):
        return jsonify(data)
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

def get_time() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@bp.route('/add_history', methods=['POST'])
@jwt_required()
def add_history():
    data = {
        "data": dict(),
        "status": "no"
    }

    post_id = request.json.get('post_id')
    if not request_util.check_args(data, post_id):
        return jsonify(data)

    post = Post.query.get(post_id)
    if not post:
        data['data']['msg'] = '该用户不存在'
        data['status'] = 'no'

    history = History.query.filter_by(post_id=post_id).first()
    if history:
        history.access_time = get_time()
    else:
        post.access_count += 1
        user_id = get_jwt_identity()
        history = History(user_id=user_id, post_id=post_id)
        db.session.add(history)

    db.session.commit()

    data['data']['msg'] = '添加成功'
    data['status'] = 'ok'

    return jsonify(data)

@bp.route('/get_histories', methods=['GET'])
@jwt_required()
def get_histories():
    data = {
        'data': dict(),
        'status': 'no'
    }

    user_id = get_jwt_identity()

    histories = History.query.filter_by(user_id=user_id).order_by(History.access_time.desc()).all()

    data['data']['items'] = post_util.get_histories(histories)
    data['status'] = 'ok'
    return jsonify(data)