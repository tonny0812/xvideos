# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     HtmlParser
   Description :  用于解析网页内容抽取URL和数据
   Author :       qiuqiu
   date：          2019/10/22
-------------------------------------------------
"""

import urllib.parse

from bs4 import BeautifulSoup

from Entites.Video import Video


class HtmlParser(object):

    def parser(self, page_url, html_cont):
        '''
        用于解析网页内容抽取URL和数据
        :param page_url: 下载页面的URL
        :param html_cont: 下载的网页内容
        :return:返回小视频的title和URL
        '''
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        video_datas = self._get_video_infos(page_url, soup)
        return video_datas

    def _get_video_infos(self, page_url, soup):
        '''
        抽取新的URL集合
        :param page_url: 下载页面的URL
        :param soup:soup
        :return: 返回小视频的title&url
        '''
        videos = set()
        # 抽取符合要求的a标签
        blocks = soup.select('.thumb-block')
        for block in blocks:
            link = block.select('.thumb-under > p > a')[0]
            img_link = block.select('.thumb-inside  a img')[0]
            try:
                # 提取href属性
                title = link['title']
                url = link['href']
                img_url = img_link['data-src']
                # 拼接成完整网址
                full_vurl = urllib.parse.urljoin(page_url, url)
                video = Video("".join(title.split()), full_vurl, img_url)
                videos.add(video)
            except AttributeError as e:
                print(e)

        links = soup.select('.thumb-under > p > a')
        for link in links:
            try:
                # 提取href属性
                title = link['title']
                url = link['href']
                # 拼接成完整网址
                full_vurl = urllib.parse.urljoin(page_url, url)
                video = Video(title, full_vurl)
                videos.add(video)
            except AttributeError as e:
                print(e)
        return videos
