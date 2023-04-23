from db import db

# 用户表
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    profile = db.Column(db.String(255))
    sex = db.Column(db.String(1))
    email = db.Column(db.String(20))
    age = db.Column(db.Integer)

class Post(db.Model):
    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    poster_id = db.Column(db.Integer)

class PostImages(db.Model):
    __tablenames__ = 'post_image'

    img_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_name = db.Column(db.String(100))
    post_id = db.Column(db.Integer)
    order_number = db.Column(db.Integer)