import datetime

from db import db

# 学习阶段
class Level(db.Model):
    __tablename__ = 'level'
    level_id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(255), nullable=True)
    level_description = db.Column(db.String(255), nullable=True)

# 帖子
class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    post_time = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())
    level_id = db.Column(db.Integer, db.ForeignKey('level.level_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    level_value = db.Column(db.Float, nullable=True)
    type_id = db.Column(db.Integer, db.ForeignKey('post_type.type_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    # 设置外键约束
    user = db.relationship('User', backref='posts')
    level = db.relationship('Level', backref='posts')
    post_type = db.relationship('PostType', backref='posts')

# 回复
class PostComment(db.Model):
    __tablename__ = 'post_comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    content = db.Column(db.Text, nullable=True)
    post_time = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())
    # 设置外键约束
    post = db.relationship('Post', backref='comments')
    user = db.relationship('User', backref='comments')

# 帖子评价
class PostEvaluate(db.Model):
    __tablename__ = 'post_evaluate'
    evaluate_id = db.Column(db.Integer, primary_key=True)
    evaluate_level = db.Column(db.Integer, nullable=True)
    evaluate_body = db.Column(db.String(255), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    # 设置外键约束
    post = db.relationship('Post', backref='evaluations')
    user = db.relationship('User', backref='evaluations')

# 帖子图片
class PostImage(db.Model):
    __tablename__ = 'post_images'
    img_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_name = db.Column(db.String(255), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    order_number = db.Column(db.Integer, nullable=True)

    # 设置外键约束
    post = db.relationship('Post', backref='images')

# 帖子话题
class PostTopic(db.Model):
    __tablename__ = 'post_topic'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.topic_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)

    # 设置外键约束
    post = db.relationship('Post', backref='topics')
    topic = db.relationship('Topic', backref='posts')

# 帖子类型
class PostType(db.Model):
    __tablename__ = 'post_type'
    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(6), nullable=True)
    type_description = db.Column(db.String(255), nullable=True)

    # 反向引用
    posts = db.relationship('Post', backref='type')

# 话题
class Topic(db.Model):
    __tablename__ = 'topic'
    topic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_name = db.Column(db.String(255), nullable=True)
    topic_description = db.Column(db.String(255), nullable=True)
    topic_image = db.Column(db.String(255), nullable=True)

    # 反向引用
    posts = db.relationship('PostTopic', backref='topic')

# 用户
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(20), nullable=True)
    profile = db.Column(db.String(255), default='default.png', nullable=True)

    # 反向引用
    posts = db.relationship('Post', backref='author')
    collections = db.relationship('UserCollect', backref='user')

# 用户收藏
class UserCollect(db.Model):
    __tablename__ = 'user_collect'
    collect_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)

    # 设置外键约束
    post = db.relationship('Post', backref='collectors')

# 用户关注的用户
class UserFollow(db.Model):
    __tablename__ = 'user_follow'
    follow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    target_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)

# 用户访问记录
class UserHistory(db.Model):
    __tablename__ = 'user_history'
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    access_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# 用户信息
class UserInfo(db.Model):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sex = db.Column(db.String(1), nullable=True)
    email = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    signup_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_description = db.Column(db.String(255), nullable=True)
    level_id = db.Column(db.Integer, db.ForeignKey('level.level_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    level_value = db.Column(db.Float, nullable=True)

# 用户学习时长统计
class UserLearningRecord(db.Model):
    __tablename__ = 'user_learning_record'
    record_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    learning_duration = db.Column(db.Integer, nullable=True)

# 用户喜欢
class UserLike(db.Model):
    __tablename__ = 'user_like'
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=True)
    comment_id = db.Column(db.Integer, nullable=True)
    access_time = db.Column(db.DateTime, nullable=True)

# 用户消息访问记录
class UserMsgAccess(db.Model):
    __tablename__ = 'user_msg_access'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    msg_type = db.Column(db.String(10), nullable=True)
    last_id = db.Column(db.Integer, nullable=True)

    # 定义外键关系
    user = db.relationship('User', backref=db.backref('msg_accesses', lazy='dynamic'))

# 用户关注话题
class UserTopic(db.Model):
    __tablename__ = 'user_topic'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.topic_id'), nullable=True)

    # 定义外键关系
    user = db.relationship('User', backref=db.backref('topics', lazy='dynamic'))
    topic = db.relationship('Topic', backref=db.backref('users', lazy='dynamic'))
