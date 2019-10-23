# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     DataOutput
   Description :   数据存储，store_data(data)将解析数据放到内存中，output_html()将数据存储成html格式
   Author :       qiuqiu
   date：          2019/10/22
-------------------------------------------------
"""
import codecs

from bs4 import BeautifulSoup

import SpiderConfig


class DataOutput(object):

    def __init__(self):
        self.videos = []

    def store_data(self, video):
        if video is None:
            return
        self.videos.append(video)

    def store_datas(self, videos):
        if videos is None and len(videos) == 0:
            return
        for video in videos:
            self.store_data(video)

    def output_html(self):
        _content = []
        _content.append("<html>")
        _content.append("<head><meta charset='utf-8'/></head>")
        _content.append("<body>")
        _content.append("<table>")
        for video in self.videos:
            _content.append("<tr>")
            _content.append("<td>")
            _content.append("<img src='%s'/><br/>" % (video.get_img_url()))
            _content.append("<a href='%s' target='_blank' rel='noopener noreferrer'>%s</a>" % (video.get_url(), video.get_title()))
            _content.append("</td>")
            _content.append("</tr>")
        _content.append("</table>")
        _content.append("</body>")
        _content.append("</html>")

        html_cont = ''.join(_content)
        soup = BeautifulSoup(html_cont, "lxml")
        fout = codecs.open(SpiderConfig.VIDEOS_OUTPUT_FILE_PATH, 'w', encoding='utf-8')
        fout.write(soup.prettify())
        fout.close()
