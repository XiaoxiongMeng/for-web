from manage import app
from flask_sqlalchemy import SQLAlchemy
import pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1/python'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'exchange_user_table'
    id = db.Column(db.Integer, primary_key=True)  # id，为唯一标识符
    username = db.Column(db.String(10), nullable=False)  # 用户名，最长限制10个字符
    password = db.Column(db.String(300), nullable=False)  # 哈希加密后的密码
    mail = db.Column(db.String(30), nullable=False, unique=True)   # 邮箱，长度为0~30，不允许为空
    avatar = db.Column(db.String(60)) # 头像的url，
    permission = db.Column(db.Integer, default=0)  # 是否具有管理员权限
    fav_list = db.Column(db.String(600))  # 收藏列表
    toke_post = db.Column(db.String(600))  # 叫价列表
    balance = db.Column(db.Integer)  # 余额


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)  # id，为唯一标识符
    user_id = db.Column(db.Integer)  #用户id
    title = db.Column(db.String(40), nullable=False)  # 帖子名
    content = db.Column(db.String(6000), nullable=False)  # 帖子内容
    pic_urls = db.Column(db.String(400), nullable=False, unique=True)   # 图床，用于存储帖子中含有的图片
    price = db.Column(db.Float)  # 卖家价格
    buy_price = db.Column(db.Float)  # 买家当前协商价格
    is_approved = db.Column(db.Integer)  # 是否通过审核
    # is_hangon = db.Column(db.Integer)  # 是否处于待支付状态
    is_finished = db.Column(db.Integer)  # 是否完成
    is_deleted = db.Column(db.Integer)  # 是否被删除（删除后将出现在垃圾箱中，在垃圾箱中再次删除才会永久删除。已完成交易的要买卖家都支持删除才可永久删除）
    buyer_id = db.Column(db.Integer)  # 买家id