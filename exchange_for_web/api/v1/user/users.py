from flask import request, jsonify
from . import user_page

from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from .functions import send_code, generate_token

caches = {}  # 缓存电子邮件验证码信息


@user_page.route('/user/test')  # 内网穿透后用作测试
def test():
    return "hello world!"


@user_page.route('/user/login', methods=['POST'])  # 登录功能
def log_in():
    query = request.form  # 从post请求中获取前端传来的表单
    username = query['username']
    password = query['password']
    if '@' in username:  # 检测用户是否是邮箱登录
        x = User.query.filter_by(mail=username).all()  # 如果是邮箱登录，查询数据表中是否含有mail的信息
    else:
        x = User.query.filter_by(username=username).all()  # 如果不是，查询数据表中是否含有用户username的信息
    if len(x) == 1:  # 检查用户名是否唯一
        if check_password_hash(x[0].password, password):  # 唯一则检查密码是否正确
            token = generate_token(x[0].id, username, x[0].permission)  # 若正确，生成token并返回token，头像图床和用户名，id信息
            return jsonify(code=200, message='登陆成功！',
                           data={"id": x[0].id, "username": x[0].username, "avatar": x[0].avatar, "token": token})
        else:  # 如果密码不正确，报错并返回
            return jsonify(code=401, message='密码错误，请检查后再试.')
    elif len(x) > 1:  # 如果用户不唯一，报错并返回
        return jsonify(code=401, message='有重复的用户名，请改用邮箱登录.')
    else:  # 如果用户不存在，报错并返回
        return jsonify(code=404, message='用户不存在，请检查用户名是否正确')


@user_page.route('/user/signup/code', methods=['POST'])  # 发送验证码
def send_mail_code():
    global caches  # 引用全局变量caches
    query = request.form
    target_mail = query['mail']
    x = User.query.filter_by(mail=target_mail).first()  # 检查电子邮件是否已被注册
    if x:
        return jsonify(code=409, message='该电子邮件地址已经被注册.')
    try:
        code = send_code(target_mail)  # 发送验证码
    except:  # 发送失败，就是格式不对
        return jsonify(code=400, message='发送失败！请检查邮箱格式是否正确.如果检查无误，请联系管理员.')
    caches[target_mail] = code  # 在caches字典中创建一个key为目标电子邮件，value为验证码
    return jsonify(code=200, message='发送成功！请前往邮箱接收验证码')


@user_page.route('/user/signup', methods=['POST'])  # 注册功能
def signup():
    global caches
    query = request.form
    mail = query['mail']
    username = query['username']
    password = generate_password_hash(query['password'])  # 哈希加密
    if '@' in username:  # 因为特殊的登陆账号检测机制，使得用户名中不能存在@，在这里检测
        return jsonify(code=409, message='用户名中不能包括“@”.')
    try:  # 尝试从caches中取出mail的value
        temp_code = caches[mail]
    except KeyError:  # 取出失败就是没发送验证码
        return jsonify(code=400, message='请先发送一个邮箱验证码.')
    if temp_code != query['code']:
        return jsonify(code=400, message='邮箱验证码不正确.')
    try:
        last_record = User.query.order_by(User.id.desc()).first()
        id = int(last_record.id) + 1
    except:
        id = 1
    new_user = User(username=username, password=password, id=id, mail=mail, balance=0)
    db.session.add(new_user)
    try:
        db.session.commit()
        del caches[mail]  # 删除caches 中的键值对，释放内存
        return jsonify(code=200, message='注册成功！', data={"id": id, "username": username})
    except:
        return jsonify(code=409, message='该电子邮件已被注册过，请尝试直接登录.')
