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


class DataOutput(object):

    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = codecs.open(u'C:\\Users\\qiuqiu\\PycharmProjects\\xvideos\\文件\\list.html', 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write("<head><meta charset='utf-8'/></head>")
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td><a href='%s'>%s</a></td>" % (data['url'], data['url']))
            fout.write("<td><a href='%s'>%s</a></td>" % (data['url'], data['title']))
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()
