import os
import re
import smtplib
import random
import time
import jwt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from qiniu import Auth, put_file, etag

from models import Post

ak = '9WtJTijVY5XC9FnLpv0dvVoWfSv4xKF9-J3ITb1b'
sk = 'QRgzexYdbhuASYoj6F8tEqIPPj2-e3U1p_GMfihm'
q = Auth(ak, sk)


def send_code(target_mail):
    code = str(random.randint(100000, 999999))  # 生成六位数随机验证码
    sender_email = 'tianyuzhendebuxian@outlook.com'  # 发送人的邮箱地址
    sender_password = 'tyzdbx666'  # 发送人的邮箱密码
    receiver_email = target_mail  # 收件人的邮箱
    msg = MIMEMultipart()  # 创建一个MIMEMultipart对象用来发送邮件
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = '您的甜鱼平台注册验证码'
    message = f'您的甜鱼平台注册验证码为{code}，请妥善保管，不要泄露.有效期为五分钟，请尽快验证.'
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()  # 与发信服务器建立连接
    server.starttls()  # 加密链接
    server.login(sender_email, sender_password)  # 登陆发信服务器
    server.sendmail(sender_email, receiver_email, msg.as_string())  # 发信
    server.quit()  # 断开与服务器的链接
    return code


def creat_picture_url(file, id):
    base_url = "rsd3sm6au.hn-bkt.clouddn.com"
    bucket_name = "westtwo"
    key = str(id) + "_" + str(time.time())
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = put_file(token, key, file)
    assert ret['key'] == key
    assert ret['hash'] == etag(file)
    url = (os.path.join(base_url, key))
    return url


def generate_token(user_id, username, permission):
    secret_key = 'westtwohouduansecond'  # token加密密钥
    payload = {  # token的荷载信息
        'id': user_id,  # 用户id
        'username': username,  # 用户名
        'permission': permission  # 用户权限
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def fetch_posts_info(id):
    pic_urls = []
    posts = Post.query.filter_by(id=id).first()
    post_id=(posts.id)
    users_id=(posts.user_id)
    title=(posts.title)
    content=(posts.content)
    price=(posts.price)
    pic_url_temp = re.findall("<.*?>", posts.pic_urls)
    for u in range(len(pic_url_temp)):
        pic_url_temp[u] = pic_url_temp[u].strip("<")
        pic_urls.append(pic_url_temp[u].strip(">"))
    return {"post_id": post_id, "user_id": users_id, "title": title, "content": content, "price": price,
            "pic_urls" :pic_urls}
