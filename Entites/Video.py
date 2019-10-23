# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Entites
   Description :
   Author :       qiuqiu
   date：          2019/10/24
-------------------------------------------------
"""


class Video(object):
    def __init__(self, title, url, imgurl=''):
        self.title = title
        self.url = url
        self.imgurl = imgurl

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def get_img_url(self):
        return self.imgurl

    def set_img_url(self, imgurl):
        self.imgurl = imgurl

    def __eq__(self, other):
        if isinstance(other, Video):
            return ((self.title == other.title) and (self.url == other.url)) and (self.imgurl == other.imgurl)
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.title) + hash(self.url) + hash(self.imgurl)
