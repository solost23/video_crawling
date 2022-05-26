import time

import schedule

from db import db
from service import video_crawl


# 开启定时任务，初始化对象，跑程序
def run():
    # 初始化数据库，开启定时任务
    base_url = ""
    mysql_client = db.new_mysql_client()
    video_crawl_object = video_crawl.VideoCrawl(base_url, mysql_client)

    schedule.every().day().at("3:00").do(video_crawl_object.video_crawl)
    while True:
        schedule.run_pending()
