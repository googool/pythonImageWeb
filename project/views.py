# -*-coding:utf-8-*-

from project import app, db, login_manager
from models import Image, User
from flask import render_template, redirect, request, flash, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user
import hashlib
import random
import json


@app.route('/')
def index():
    paginate = Image.query.all().paginate(page=0, per_page=10)

    map = {'has_next': paginate.has_next}
    images = []
    for image in paginate.items:
        imgvo = {'id': image.id, 'url': image.url, 'comment_count': len(image.comments)}
        images.append(imgvo)
    map['images'] = images
    return json.dumps(map)


@app.route('/image/<int:image_id>/')
@login_required
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    paginate = Image.query.paginate(page=1, per_page=3)
    return render_template('profile.html', user=user, has_next=paginate.has_next, images=paginate.items)

@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id,page,per_page):
    # 参数检查
    paginate=Image.query.filter_by(user_id=user_id).paginate(page=page,per_page=per_page)

    map = {'has_next':paginate.has_next}
    images=[]
    for image in paginate.items:
        imgvo={'id':image.id,'url':image.url,'comment_count':len(image.comments)}
        images.append(imgvo)
    map['images']=images
    return json.dumps(map)

@app.route('/regloginpage/')
def regloginpage(msg=''):
    if current_user.is_authenticated:
        return redirect('/')

    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    # 如果已经登录的就跳到首页
    return render_template('login.html', msg=msg, next=request.values.get('next'))

def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)

@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    # 校验
    user = User.query.filter_by(username=username).first()
    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', u'用户名和密码不能为空', 'reglogin')

    user = User.query.filter_by(username=username).first()
    if user == None:
        return redirect_with_msg('/regloginpage', u'用户名不存在', 'reglogin')

    m = hashlib.md5()
    m.update(password + user.salt)
    if m.hexdigest() != user.password:
        return redirect_with_msg('/regloginpage', u'密码错误', 'reglogin')

    login_user(user)

    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)
    return redirect('/')

@app.route('/reg/', methods={'get', 'post'})
def reg():
    # args url里的
    # form body里的
    # values 全部
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    # 校验
    user = User.query.filter_by(username = username).first()
    if username == '' or password == '':
        return redirect_with_msg('/regloginpage', u'用户名和密码不能为空', 'reglogin')
    if user != None:
        return redirect_with_msg('/regloginpage', u'用户名已存在', 'reglogin')

    salt = ''.join(random.sample('0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 10))
    m = hashlib.md5()
    m.update(password+salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()
    login_user(user)

    next = request.values.get('next')
    if next != None and next.startswith('/') > 0:
        return redirect(next)
    return redirect('/')

    # 请大家考虑更多边界问题

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')