# this is a video_crawling

import os, sys
# 默认从文件所在路径下找，所以要加入项目路径，才会从项目开始找
sys.path.append(os.getcwd())

from server import server

if __name__ == '__main__':
    server.run()
