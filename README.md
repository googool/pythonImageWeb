# pythonImageWeb
Windows下python 版本选择：
    1.py -2 使用python2.x;py -3 使用python3.x
    2.python.exe重命名->python2 使用python2.x;python3 使用python3.x

    ORM:sqlalchemy
mysql数据库：8.0.11:
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade sqlalchemy --ignore-installed
    __init__.py 添加
        import pymysql
        pymysql.install_as_MySQLdb()

云实时缩图：同一张图片多处现实时，能根据占位尺寸按需求定义截取方式，如若遇到需求更改，也没有影响。
    举例：个人详情页、首页和评论区的头像是同一张，但是尺寸不同。

    gunicorn -D -w 3 -b 0.0.0.0:8000 project:app
             -D:后台运行
             -w:启动线程数
             -b:绑定地址和端口
             project:app——运行的项目入口
             0.0.0.0：

    Nginx 配置 /etc/nginx/sites-enabled/c1

    server{
        listen 80;
        server_name chenjinxin.com;
        location / {
            proxy_pass http://127.0.0.1:8000;
        }
    }
    server{
        listen 80;
        server_name changxiangyu.cn;
        location / {
            proxy_pass http://127.0.0.1:8888;
        }
    }

    flask-mail:邮件激活
    导购：阿里妈妈；
