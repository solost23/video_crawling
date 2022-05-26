# 执行具体功能

class VideoCrawl:
    '''
    视频爬获取任务
    '''
    base_url = None
    mysql_client = None

    def __init__(self, base_url, mysql_client):
        self.base_url = base_url
        self.mysql_client = mysql_client

    def video_crawl(self):
        print('huquchengogng')
        return "获取成功"