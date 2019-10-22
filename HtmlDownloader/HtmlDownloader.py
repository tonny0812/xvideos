# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     HtmlDownloader
   Description :   HTML下载器，需要考虑页面编码，实现一个接口downlaod(url)
   Author :       qiuqiu
   date：          2019/10/22
-------------------------------------------------
"""
import requests


class HtmlDownloader(object):

    def download(self, url, proxies=None, headers={}, timeout=10):
        if url is None:
            return None
        if proxies is None:
            proxies = {'http': '127.0.0.1:1080', 'https': '127.0.0.1:1080'}

        response = requests.get(url, timeout=timeout, proxies=proxies, headers=headers)
        if response.status_code == requests.codes.ok:
            return response.content
        return None