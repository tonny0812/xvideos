# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     HtmlDownloader
   Description :   HTML下载器，需要考虑页面编码，实现一个接口downlaod(url)
   Author :       qiuqiu
   date：          2019/10/22
-------------------------------------------------
"""
import SpiderConfig
from Utils import RequestUtil


class HtmlDownloader(object):

    def download_with_proxies(self, url):
        return RequestUtil.download_content(url, proxies=SpiderConfig.PROXIES, timeout=10)
