from flask import Flask, request, jsonify
from blueprint.login import bp as login_bp
from blueprint.user import bp as user_bp
from blueprint.post import bp as post_bp
from blueprint.test import bp as test_bp
from blueprint.home import bp as home_bp
from blueprint.msg import bp as msg_bp
from flask_cors import CORS, cross_origin
from util.request_util import jwt
from db import db
import config

app = Flask(__name__)

app.register_blueprint(login_bp)
app.register_blueprint(user_bp)
app.register_blueprint(test_bp)
app.register_blueprint(post_bp)
app.register_blueprint(home_bp)
app.register_blueprint(msg_bp)

app.config.from_object(config)
db.init_app(app)
jwt.init_app(app)
cors = CORS(app, resources = {r"/*": {"origins": "*"}}, supports_credentials = True)


# 设置允许的HTTP方法
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    return response

@app.route('/')
def index():
    return '访问成功'

if __name__ == '__main__':
    app.run()
