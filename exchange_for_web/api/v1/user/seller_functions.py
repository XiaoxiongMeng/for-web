import os
import jwt
from flask import request, jsonify
from models import Post, db, User
from . import seller_operation
from .functions import creat_picture_url


@seller_operation.route('/createposts', methods=['POST'])
def create_post():
    print("测试节点-发帖-进入")
    lists = request.files  # 从传来的数据中取出图片
    query = request.form  # 从传来的数据中取出表单
    token = request.headers.get('Authorization')  # 获取token
    user_id = jwt.decode(token, 'westtwohouduansecond', algorithms=['HS256'])['id']  # 从token中解析出用户名
    title = query['title']  # 帖子标题
    content = query['content']  # 帖子内容
    price = query['price']  # 卖家设置的价格
    if not os.path.exists('temp'):  # 创建一个缓存文件夹
        os.makedirs('temp')
    pic_url = ""
    for i in lists:
        file = request.files[i]  # 取出第i个文件
        file.save('temp/{}_{}'.format(user_id, i))  # 缓存到本地缓存文件夹中
        pic_url = pic_url + "<" + (creat_picture_url('temp/{}_{}'.format(user_id, i), user_id)) + ">"  # 上传到图床
        os.remove('temp/{}_{}'.format(user_id, i))  # 删除本地图片释放内存
    try:
        last_record = Post.query.order_by(Post.id.desc()).first()  # 获得最后一条记录的id
        id = int(last_record.id) + 1  # 给本条帖子设置id
    except:  # 如果还没有帖子，那么本帖子的id就是1
        id = 1
    new_user = Post(title=title, content=content, id=id, user_id=user_id, pic_urls=pic_url, price=price, is_approved=0,
                    is_deleted=0)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(code=200, message='帖子已成功发布，等待买家吧！')


@seller_operation.route("/seller/posted_posts",methods=["GET"])
def posted_post():
    lists = []
    token = request.headers.get("Authorization")
    user_id = jwt.decode(token, 'westtwohouduansecond', algorithms=['HS256'])['id']
    posts = Post.query.filter_by(user_id=user_id).all()
    for i in range(len(posts)):
        lists.append({"id": posts[i].id, "title": posts[i].title, "is_approved": posts[i].is_approved, "content": posts[i].content})
    return jsonify(code=200, message="以下是待审核的交易帖", data={"posts_lists": lists})