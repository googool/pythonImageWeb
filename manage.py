# -*-coding:utf-8-*-

from project import app, db
from flask_script import Manager
from project.models import User, Image, Comment
import random

manage = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


@manage.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('yonghu' + str(i), 'mima' + str(i)))
        for j in range(0, 3):
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('comment'+str(k), 1+3*i+j, i+1))
    db.session.commit()

    # 更新
    for i in range(0, 100, 10):
        # 通过update函数
        User.query.filter_by(id=i + 1).update({'username': '牛客新' + str(i)})

    for i in range(1, 100, 2):
        # 通过设置属性
        u = User.query.get(i + 1)
        u.username = 'd' + str(i * i)
    db.session.commit()

    # 删除
    for i in range(50, 100, 2):
        Comment.query.filter_by(id=i + 1).delete()
    for i in range(51, 100, 2):
        comment = Comment.query.get(i + 1)
        db.session.delete(comment)
    db.session.commit()

    print 1, User.query.all()
    print 2, User.query.get(3)  # primary key = 3
    print 3, User.query.filter_by(id=2).first()
    print 4, User.query.order_by(User.id.desc()).offset(1).limit(2).all()
    print 4.2, User.query.order_by(User.id.desc()).offset(1).limit(2)
    '''
        /*SELECT user.id AS user_id, user.username AS user_username, user.password AS user_password, user.head_url AS user_hea
    d_url
    FROM user ORDER BY user.id DESC
     LIMIT %(param_1)s, %(param_2)s*/
    '''
    print 5, User.query.paginate(page=1, per_page=10).items
    u = User.query.get(1)
    print 6, u
    print 7, u.images
    print 8, Image.query.get(1).user
    # print 7, User.query.get(1).images.filter_by(id=1).first() # Base query:User.query.get(1).images
    # print User.query.filter_by(id=2).first_or_404()


if __name__ == '__main__':
    manage.run()
