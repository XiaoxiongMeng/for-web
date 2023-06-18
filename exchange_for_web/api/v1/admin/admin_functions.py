import re

from models import User, Post
from . import admin_operation
from ..user.functions import fetch_posts_info
import jwt
from flask import request, jsonify


@admin_operation.route("/admin/audit", methods=["GET"])
def audit():
    lists = []
    token = request.headers.get("Authorization")
    user_id = jwt.decode(token, 'westtwohouduansecond', algorithms=['HS256'])['id']
    x = User.query.filter_by(id=user_id).first()
    if x.permission == 0:
        return jsonify(code=403, message="您不是系统管理员，无权对帖子进行审核！")
    posts = Post.query.filter_by(is_approved="0").all()
    for i in range(len(posts)):
        lists.append({"id": posts[i].id, "user_id": posts[i].user_id, "title": posts[i].title,
                      "content": posts[i].content})
    return jsonify(code=200, message="以下是待审核的交易帖", data={"post_list": lists})
