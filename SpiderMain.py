# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     SpiderMain
   Description :
   Author :       qiuqiu
   date：          2019/10/22
-------------------------------------------------
"""
from SpiderManager.SpiderManager import SpiderManager

if __name__ == "__main__":
    spider_man = SpiderManager()

    urls = ['https://www.xvideos.com', 'https://www.xvideos.com/new/1',
            'https://www.xvideos.com/new/2', 'https://www.xvideos.com/new/3',
            'https://www.xvideos.com/new/4', 'https://www.xvideos.com/new/5',
            'https://www.xvideos.com/new/6', 'https://www.xvideos.com/new/7',
            'https://www.xvideos.com/new/8', 'https://www.xvideos.com/new/9',
            'https://www.xvideos.com/new/10', 'https://www.xvideos.com/new/11']
    # for url in urls:
    #     print("开始抓取：", url)
    #     spider_man.crawl(url)
    spider_man.crawlVideoURL('https://www.xvideos.com/lang/chinese')