import pymysql

from config import config


# 链接数据库
def new_mysql_client():
    # 返回数据库链接
    mysql_config = config.get_config()["connections"]["mysql"]
    conn = pymysql.connect(host=mysql_config["host"],
                           port=mysql_config["port"],
                           user=mysql_config["user"],
                           password=mysql_config["password"],
                           db=mysql_config["db"],
                           charset=mysql_config["charset"])
    return conn
