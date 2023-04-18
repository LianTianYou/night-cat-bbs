from flask import Flask, request, jsonify
from blueprint.login import bp as login_bp
import config

app = Flask(__name__)
app.register_blueprint(login_bp)
app.config.from_object(config)


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
