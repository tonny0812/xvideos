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
        self.realurl = []
        self.localpath = ""

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def get_img_url(self):
        return self.imgurl

    def set_img_url(self, imgurl):
        self.imgurl = imgurl

    def get_real_url(self):
        return self.realurl

    def set_real_url(self, realurls):
        for url in realurls:
            self.realurl.append(url)

    def get_local_path(self):
        return self.localpath

    def set_local_path(self, localpath):
        self.localpath = localpath

    def __eq__(self, other):
        if isinstance(other, Video):
            return ((self.title == other.title) and (self.url == other.url)) and (self.imgurl == other.imgurl)
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.title) + hash(self.url) + hash(self.imgurl)

    # def __str__(self) -> str:
    #     return "{" + self.title + "," + self.url + "," + str(self.realurl) + "}"


if __name__ == "__main__":
    video = Video('title', 'url')
    print(video.get_title(), video.get_url())
    urls = ['u1', 'u2']
    for url in urls:
        print(url)
    video.set_real_url(urls)
    print(video)
