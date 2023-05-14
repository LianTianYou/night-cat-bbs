from tables import User, Comment, Post, PostImages, History, Like
from util import img_util, value_util, user_util


def get_poster_info(user_id : int) -> dict:
    user = User.query.get(user_id)
    user_info = dict()
    user_info["user_id"] = user.user_id
    user_info["user_name"] = user.user_name
    user_info["profile"] = img_util.get_profile_url(user.profile)
    return user_info

def get_comments(post_id : int) -> list:
    comments = Comment.query.filter_by(post_id = post_id).all()
    comment_list = []
    for comment in comments:
        comment_dict = dict()
        comment_dict['content'] = comment.content
        comment_dict['post_time'] = str(comment.post_time)
        user = User.query.get(comment.user_id)
        comment_dict['user_info'] = dict()
        comment_dict['user_info']['user_id'] = user.user_id
        comment_dict['user_info']['user_name'] = user.user_name
        comment_dict['user_info']['profile'] = img_util.get_profile_url(user.profile)
        comment_list.append(comment_dict)
    return comment_list

def get_post_data(post : Post) -> dict:
    data = dict()
    data['post_info'] = get_post_info(post)
    data['post_body'] = get_post_body(post)
    data["poster_info"] = get_poster_info(post.user_id)
    return data

def get_post_body(post : Post) -> dict:
    body = dict()
    body['title'] = post.title
    body['content'] = post.content
    body['comments'] = get_comments(post.post_id)
    body['images'] = get_post_images(post.post_id)
    return body

def get_post_info(post : Post) -> dict:
    post_info = dict()
    post_info['post_time'] = str(post.post_time)
    post_info['like_count'] = post.like_count
    post_info['comment_count'] = Comment.query.filter_by(post_id=post.post_id).count()
    post_info['access_count'] = post.access_count
    post_info['post_id'] = post.post_id
    post_info['is_like'] = False
    user_id = user_util.get_now_id()
    like = Like.query.filter_by(user_id=user_id, post_id=post.post_id).first()
    if like:
        post_info['is_like'] = True
    return post_info

def get_post_images(post_id : int) -> list:
    images = []
    post_images = PostImages.query.filter_by(post_id=post_id).order_by(PostImages.order_number).all()

    for image in post_images:
        image_url = img_util.get_post_image_url(image.img_name)
        images.append(image_url)
    return images

def get_posts(posts : list[Post]) -> list:
    post_list = []

    for post in posts:
        post_dict = {'post': get_post_data(post)}
        post_list.append(post_dict)
    return post_list

def get_recommend_posts(posts : list) -> list:
    post_list = []
    for post in posts:
        item_dict = get_post_data(post)
        post_list.append(item_dict)
    return post_list

def get_histories(histories : list[History]) -> list:
    history_list = []
    for history in histories:
        history_dict = dict()
        post = Post.query.get(history.post_id)
        history_dict['post'] = get_post_data(post)
        history_dict['access_time'] = str(history.access_time)
        history_list.append(history_dict)
    return history_list