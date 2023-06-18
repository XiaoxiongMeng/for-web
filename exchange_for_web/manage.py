from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
from api.v1.user import user_page, seller_operation
from api.v1.admin import admin_operation

app.register_blueprint(user_page)  # 注册蓝图
app.register_blueprint(seller_operation)
app.register_blueprint(admin_operation)
CORS(app)  # 实现跨域
if __name__ == '__main__':
    app.run(host='0.0.0.0')  # 内网可用


@app.route('/')
def hello_world():
    return "Welcome come to sweet fish!"
