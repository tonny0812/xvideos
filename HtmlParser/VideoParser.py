# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     VideoParser
   Description :
   Author :       qiuqiu
   date：          2019/10/27
-------------------------------------------------
"""
import re
import urllib.parse

from bs4 import BeautifulSoup


class VideoParser(object):

    def m3u8parser(self, html_cont):
        '''
        用于解析总的m3u8链接
        :param html_cont: 下载的网页内容
        :return:总的m3u8链接
        '''
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        title = self._get_m3u8_title(soup)
        html_cont = html_cont.decode('utf-8')
        m3u8_url = re.search(r"html5player\.setVideoHLS\('(.*?)'\);", html_cont).group(1)  # 总的m3u8链接
        base_url = re.search(r"(.*?)hls.m3u8", m3u8_url).group(1)  # 从m3u8_url中取出，留待拼接
        return title, base_url, m3u8_url

    def _get_m3u8_title(self, soup):
        title = soup.select(".page-title")[0]
        if title:
            return title.get_text()
        return None

    def m3u8HighestParser(self, base_url, m3u8_cont):
        '''
        抽取内含不同的清晰度所对应的m3u8链接，返回最高清晰度的m3u8链接
        :param base_url: base_url
        :param html_cont:html_cont
        :return: 返回最高清晰度的m3u8链接
        '''
        if base_url is None or m3u8_cont is None:
            return

        m3u8_cont = m3u8_cont.decode('utf-8')
        definition_list = re.findall(r'NAME="(.*?)p"', m3u8_cont)
        max_definition = max(definition_list)  # 找到最高清晰度
        line_list = m3u8_cont.split('\n')
        for line in line_list:
            if 'hls-' in line and max_definition in line:
                max_definition_m3u8_url = line  # 最高清晰度的m3u8链接(相对路径)

        max_definition_m3u8_url = urllib.parse.urljoin(base_url, max_definition_m3u8_url)
        return max_definition_m3u8_url

    def m3u8TSParser(self, base_url, h_m3u8_cont):
        ts_url_list = []
        h_m3u8_cont = h_m3u8_cont.decode('utf-8')
        for line in h_m3u8_cont.split('\n'):
            if '.ts' in line:
                ts_url_list.append(urllib.parse.urljoin(base_url, line))
        return ts_url_list
