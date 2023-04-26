import datetime

from db import db

# 用户表
class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    profile = db.Column(db.String(255))
    sex = db.Column(db.String(1))
    email = db.Column(db.String(20))
    age = db.Column(db.Integer)
    follow_count = db.Column(db.Integer, default=0)
    fans_count = db.Column(db.Integer, default=0)
    signup_time = db.Column(db.Integer, default = datetime.datetime.now)

# 帖子表
class Post(db.Model):
    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    post_time = db.Column(db.DateTime, default=datetime.datetime.now)
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)

# 帖子图片表
class PostImages(db.Model):
    __tablenames__ = 'post_image'

    img_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_name = db.Column(db.String(100))
    post_id = db.Column(db.Integer)
    order_number = db.Column(db.Integer)

# 点赞表
class Like(db.Model):
    __tablenames__ = 'like'

    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

# 评论表
class Comment(db.Model):
    __tablename__ = 'comment'

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    post_time = db.Column(db.DateTime, default=datetime.datetime.now)

class Follow(db.Model):
    __tablename__ = 'follow'

    follow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    target_id = db.Column()