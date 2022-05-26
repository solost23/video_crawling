import time
import random

import requests
import uuid

from lxml import etree
from header import user_agent


# 执行具体功能
class VideoCrawl:
    '''
    视频爬获取任务
    '''
    base_url = None
    mysql_client = None

    sql = '''
        insert into video(id, user_id, class_id, title, introduce, image_url, video_url, thumb_count, comment_count, 
        delete_status, create_time, update_time) values (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s);
    '''

    def __init__(self, base_url, mysql_client):
        self.base_url = base_url
        self.mysql_client = mysql_client

    def get_uuid(self):
        return uuid.uuid1()

    def video_crawl(self):
        # 网址: self.base_url + 1.html
        video_detail_dict_list = []
        i = 0
        while True:
            i = i + 1
            url = self.base_url + str(i) + ".html"
            page_text = requests.get(url, headers={'User-Agent': user_agent.UserAgent[random.randint(0, len(user_agent.UserAgent)) - 1]}).text
            # 解析内容,存入列表
            print("解析第%s页数据" % (i))
            data = self.parse_content(page_text)
            if data == "此页为空":
                break
            video_detail_dict_list.append(data)

        cursor = self.mysql_client.cursor()
        for video_detail_dict_list in video_detail_dict_list:
            for video_detail_dict in video_detail_dict_list:
                try:
                    cursor.execute(self.sql, (
                        # uuid
                        self.get_uuid(),
                        "0",
                        "0",
                        video_detail_dict.get("video_title"),
                        video_detail_dict.get("video_introduce"),
                        video_detail_dict.get("img_url"),
                        video_detail_dict.get("video_detail_url"),
                        0,
                        0,
                        "DELETE_STATUS_NORMAL",
                        int(time.time()),
                        int(time.time())
                        ))
                    self.mysql_client.commit()
                    print(video_detail_dict, "插入成功")
                except Exception as e:
                    print(e)
                    self.mysql_client.rollback()
                    print(video_detail_dict, "插入失败")

    # 解析内容，并放入一个列表型的字典中
    def parse_content(self, page_text):
        video_info_dict_list = []
        # 解析出标题，介绍，图片网址，视频网址
        html = etree.HTML(page_text)
        video_detail_title_list = html.xpath("// *[ @ id = 'wrapper'] / div[3] / div / div / div[2] / div / div / div / div /div[2]/h3/a/@title")
        video_detail_introduce_list = html.xpath("// *[ @ id = 'wrapper'] / div[3] / div / div / div[2] / div / div / div / div /div[2]/h3/a/@title")
        video_detail_img_url_list = html.xpath("// *[ @ id = 'wrapper'] / div[3] / div / div / div[2] / div / div / div / div /div[1]/a/img/@data-src")
        video_detail_url_list = html.xpath("// *[ @ id = 'wrapper'] / div[3] / div / div / div[2] / div / div / div / div /div[2]/h3/a/@href")
        if video_detail_title_list == [] and video_detail_url_list == [] and video_detail_introduce_list == [] and video_detail_img_url_list == []:
            # 此页为空，退出
            return "此页为空"
        for index in range(len(video_detail_title_list)):
            # 处理信息
            video_title = video_detail_title_list[index]
            video_introduce = video_detail_introduce_list[index]
            # 处理img_url
            img_url = "https://madoumedia.net" + video_detail_img_url_list[index]

            # 从视频详情页中分析出视频源视频url
            video_detail_url = video_detail_url_list[index]

            # 获取信息存入字典
            video_detail_dict = {
                "video_title": video_title,
                "video_introduce": video_introduce,
                "img_url": img_url,
                "video_detail_url": video_detail_url,
            }
            video_info_dict_list.append(video_detail_dict)
        return video_info_dict_list
