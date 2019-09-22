# pythonImageWeb
Windows下python 版本选择：
    1.py -2 使用python2.x;py -3 使用python3.x
    2.python.exe重命名->python2 使用python2.x;python3 使用python3.x
mysql数据库：8.0.11:
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade sqlalchemy --ignore-installed
    __init__.py 添加
        import pymysql
        pymysql.install_as_MySQLdb()

云实时缩图：同一张图片多处现实时，能根据占位尺寸按需求定义截取方式，如若遇到需求更改，也没有影响。
    举例：个人详情页、首页和评论区的头像是同一张，但是尺寸不同。
