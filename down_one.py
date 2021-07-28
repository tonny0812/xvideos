import html
import os
import re
import threading
import time

import requests

import merge_ts_file


class Xvideos:

    def __init__(self, url=''):
        self.url = url
        self.video_num = -1
        # self.root_path = r'xvideos'    #默认根目录为本程序所在目录下的xvideos文件夹
        self.root_path = u'文件'
        self.num_thread = 10  # 默认线程
        self.timeout = 10  # 超时时间设置
        self.retry = 10  # 请求网页失败的最大重试次数
        self.cover_num = -1
        self.count = 0
        self.html = ''
        self.title = ''
        self.video_success = True
        self.wrong_ts_infor = ''
        self.wrong_pic_infor = ''
        self.pic_url_list = []
        self.ts_file_list = []
        self.final_fail_ts_file_list = []

    def right_url(self):
        if re.search(r'https?://www.xvideos.com/video\d+', self.url):
            return True
        else:
            print('url不正确')

    def should_pass(self, text_name):
        self.video_num = re.search(r'video(\d+)', self.url).group(1)
        if not os.path.exists(text_name):
            return False
        else:
            with open(text_name, 'r') as f:
                for line in f:
                    if line[:-1] == self.video_num:
                        if text_name == 'SAVED.txt':
                            print('此视频已下载，跳过\n')
                        elif text_name == 'NO EXISTS.txt':
                            print('此视频不存在，跳过\n')
                        return True
                return False

    def request(self, url, headers={}):
        default_http_proxy = '127.0.0.1:1080' if os.name == 'nt' else '127.0.0.1:8118'
        http_proxy = os.getenv('http_proxy') or os.getenv('HTTP_PROXY') or default_http_proxy
        https_proxy = os.getenv('https_proxy') or os.getenv('HTTPS_PROXY') or default_http_proxy
        proxies = { 'http': http_proxy, 'https': https_proxy }

        # if os.name == 'nt':  # windows
        #     proxies = {'http': '127.0.0.1:1080', 'https': '127.0.0.1:1080'}  # ssr的win客户端采用1080端口的http协议
        # elif os.name == 'posix':  # linux
        #     proxies = {'http': '127.0.0.1:10809',
        #                'https': '127.0.0.1:10809'}  # ssr+privoxy,通过privoxy将1080端口的socks协议转发给10809端口的http协议

        response = requests.get(url, timeout=self.timeout, proxies=proxies, headers=headers)
        return response.content

    def repeat_request(self, url, headers={}, fail_hint='', final_fail_hint=''):
        retry_times = 1
        while retry_times <= self.retry:
            try:
                response = self.request(url, headers={})
                return response
            except:
                if fail_hint:
                    print(eval(fail_hint))
            retry_times += 1
        else:  # while else 结构，正常时（不正常是指因为break return 异常等而退出循环）运行else内的语句
            if final_fail_hint:
                print(final_fail_hint)

    def mkdir(self):
        self.title = re.search(r'<h2 class="page-title">(.*?)<span class="duration">', self.html)
        if self.title:
            self.title = self.title.group(1).rstrip()
            self.title = html.unescape(self.title)  # 转换html实体，如&hellip;转换为省略号
            self.title = re.sub(r'[\/\\\*\?\|/:"<>\.]', '', self.title)  # 有的html实体也会转化出非法路径字符，也要去掉
            print('名称：', self.title)
            self.dir_path = os.path.join(self.root_path, self.title)
            if self.dir_path[-1] == ' ':  # window创建文件夹时，文件夹名以空格结尾的会自动删掉空格
                self.dir_path = self.dir_path[:-1]
            print(self.dir_path)
            if not os.path.exists(self.dir_path):
                try:
                    os.makedirs(self.dir_path)
                except OSError:  # linux路径过长会OSError: [Errno 36] File name too long:    #可参考https://stackoverflow.com/questions/34503540/why-does-python-give-oserror-errno-36-file-name-too-long-for-filename-short/34503913
                    dir_path_len = len(self.dir_path)
                    while True:
                        try:
                            dir_path_len -= 1
                            self.dir_path = self.dir_path[:dir_path_len]
                            os.makedirs(self.dir_path)
                            print(1)
                            os.rmdir(self.dir_path)  # 删除空文件夹
                            self.dir_path = self.dir_path[:-7]
                            print(self.dir_path)
                            if self.dir_path[-1] == ' ':
                                self.dir_path = self.dir_path[:-1]
                            os.makedirs(self.dir_path)  # 待会还要与‘图片’文件夹拼接
                            print(self.dir_path)
                            break
                        except:
                            pass
            return True
        else:
            print("No title! Maybe the video no exists! Exit!")
            with open('NO EXISTS.txt', 'a+', encoding='utf-8') as f:
                f.write(self.video_num + '\n')
            return False

    def thread_image(self, part_n):
        for i in range(4):
            pic_num = part_n * 4 + i
            if str(pic_num + 1) + '.jpg' in os.listdir(os.path.join(self.dir_path, '图片')):
                self.count += 1
                print("\r图片进度：%.2f%%" % (self.count / 32 * 100), end=' ')
            else:
                url = self.pic_url_list[pic_num]
                img = self.repeat_request(url,
                                          fail_hint='"' + str(pic_num + 1) + '.jpg fail and retry ' + '%d"%retry_times',
                                          final_fail_hint=str(pic_num + 1) + '.jpg final fail!')
                if img:
                    file_path = os.path.join(self.dir_path, '图片', str(pic_num + 1) + '.jpg')
                    with open(file_path, 'wb') as fb:
                        fb.write(img)

                    if pic_num + 1 == self.cover_num:  # 封面图片
                        file_path = os.path.join(self.dir_path, '1.jpg')
                        with open(file_path, 'wb') as fb:
                            fb.write(img)
                    if pic_num == 30 or pic_num == 31:  # 最后两张是大纲缩略图
                        file_path = os.path.join(self.dir_path, str(pic_num - 28) + '.jpg')
                        with open(file_path, 'wb') as fb:
                            fb.write(img)
                    self.count += 1
                    print("\r图片进度：%.2f%%" % (self.count / 32 * 100), end=' ')

    def download_image(self):
        pic_dict = ['setThumbUrl169', 'setThumbSlide', 'setThumbSlideBig']
        for pic_key in pic_dict:
            if pic_key == 'setThumbUrl169':
                content = re.search(r"html5player\.%s\('(.*?)(\d+?)\.jpg'\);" % pic_key, self.html)
                pic_base_url = content.group(1)
                self.cover_num = int(content.group(2))
                for i in range(1, 31):
                    url = pic_base_url + '%d.jpg' % i
                    self.pic_url_list.append(url)
            else:
                keyword = r"html5player\.%s\('(.*?)'\);" % pic_key
                url = re.search(keyword, self.html).group(1)
                self.pic_url_list.append(url)

        thread_list = []
        self.count = 0
        if not os.path.exists(os.path.join(self.dir_path, '图片')):
            os.makedirs(os.path.join(self.dir_path, '图片'))
        for i in range(8):  # 共32张图片，故开8线程，而不是沿用self.num_thread(因为担心不是整除32的，速度慢)
            t = threading.Thread(target=self.thread_image, kwargs={'part_n': i})
            t.setDaemon(True)  # 设置守护进程
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()  # 阻塞主进程，进行完所有线程后再运行主进程
        print()

    def download_preview_video(self):  # 下载预览视频
        if not '预览.mp4' in os.listdir(self.dir_path):
            re_str = r'/videos/thumbs169/(.*?)/mozaique'
            key = re.search(re_str, self.html).group(1)
            url = r'https://img-hw.xvideos-cdn.com/videos/videopreview/%s_169.mp4' % key  # 以后下载预览视频失败时先检查对应的解析域名是否改变了
            video_data = self.repeat_request(url, fail_hint='"preview_video fail and retry %d"%retry_times',
                                             final_fail_hint='preview_video final fail!')
            if video_data:
                file_path = os.path.join(self.dir_path, '预览.mp4')
                with open(file_path, 'wb') as f:
                    f.write(video_data)

    def download_ts_file(self, ts_url):
        re_str = r'hls-\d{3,4}p(?:-[a-zA-Z0-9]{5})?(\d+.ts)'
        # 目前见过两种，相对路径的前缀分别形如hls-720p3.ts， hls-360p-ba36e0.ts
        ts_name = re.search(re_str, ts_url).group(1)
        if ts_name in os.listdir(self.dir_path):
            self.count += 1
            self.ts_file_list.append(ts_name)
            print("\r视频进度：%.2f%%" % (self.count / self.ts_num * 100), end=' ')
        else:
            ts_file = self.repeat_request(ts_url, headers={'Connection': 'close'},
                                          fail_hint='"' + ts_name + ' fail and retry ' + '%d"%retry_times',
                                          final_fail_hint=ts_name + ' final failed! Add it into ERROR.txt')
            if ts_file:
                file_path = os.path.join(self.dir_path, ts_name)
                with open(file_path, 'ab') as f:
                    f.write(ts_file)
                    f.flush()
                self.count += 1
                self.ts_file_list.append(ts_name)
                print("\r视频进度：%.2f%%" % (self.count / self.ts_num * 100), end=' ')
            else:
                with open('ERROR.txt', 'a+', encoding='utf-8') as f:
                    f.write("{'%s': '%s'}\n" % (ts_url, self.dir_path))
                self.video_success = False

    def thread_video(self, start, end, part):
        for num, ts_url in enumerate(self.ts_url_list[start:end]):
            try:
                self.download_ts_file(ts_url)
            except:
                self.video_success = False
                raise

    def download_video(self):  # 结构为：获取ts链接，多线程爬取，合并
        m3u8_url = re.search(r"html5player\.setVideoHLS\('(.*?)'\);", self.html).group(1)  # 总的m3u8链接
        m3u8_content = self.repeat_request(m3u8_url, fail_hint="'get m3u8 fail and retry %d'%retry_times",
                                           final_fail_hint='get m3u8 fail! Exit!')  # 内含不同的清晰度所对应的m3u8链接
        if m3u8_content:
            base_url = re.search(r"(.*?)hls.m3u8", m3u8_url).group(1)  # 从m3u8_url中取出，留待拼接
            m3u8_content = m3u8_content.decode('utf-8')
            definition_list = re.findall(r'NAME="(.*?)p"', m3u8_content)
            max_definition = str(max(list(map(int,definition_list))))  # 找到最高清晰度
            line_list = m3u8_content.split('\n')
            for line in line_list:
                if 'hls-' in line and max_definition in line:
                    max_definition_m3u8_url = line  # 最高清晰度的m3u8链接(相对路径)
            max_definition_m3u8_url = base_url + max_definition_m3u8_url
            max_definition_m3u8_content = self.repeat_request(max_definition_m3u8_url,
                                                              fail_hint="'get max_definition_m3u8 fail and retry %d'%retry_times",
                                                              final_fail_hint='get max_definition_m3u8 final fail! Exit!')  # 内含该m3u8视频的ts文件信息
            if max_definition_m3u8_content:
                max_definition_m3u8_content = max_definition_m3u8_content.decode('utf-8')
                self.ts_url_list = []
                for line in max_definition_m3u8_content.split('\n'):
                    if '.ts' in line:
                        self.ts_url_list.append(base_url + line)
                self.ts_num = len(self.ts_url_list)
                '''
                拿到ts文件链接的流程是：
                从视频页源代码中找到html5player.setVideoHLS，拿到总的m3u8链接(绝对路径)
                请求内容，拿到不同清晰度的m3u8链接(相对路径)
                找出最高清晰度的m3u8链接（相对路径）
                从总的m3u8链接切割出base路径，与找出的相对路径拼接
                请求内容，拿到诸多ts文件链接(相对链接)
                再拼接
                '''
                if self.ts_num < self.num_thread:
                    self.num_thread = self.ts_num  # 线程数若大于ts文件数，则线程数减少到ts文件数
                part = self.ts_num // self.num_thread  # 分块。如果不能整除，最后一块应该多几个字节
                thread_list = []
                self.count = 0
                for i in range(self.num_thread):
                    start = part * i  # 第part个线程的起始url下标
                    if i == self.num_thread - 1:  # 最后一块
                        end = self.ts_num  # 第part个线程的终止url下标
                    else:
                        end = start + part  # 第part个线程的终止url下标
                    t = threading.Thread(target=self.thread_video, kwargs={'start': start, 'end': end, 'part': part})
                    t.setDaemon(
                        True)  # 设置守护进程；必须在start()之前设置；如果为True则主程序不用等此线程结束后再结束主程序；当我们使用setDaemon(True)方法，设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行，可能出现的情况就是，子线程的任务还没有完全执行结束，就被迫停止
                    t.start()
                    thread_list.append(t)
                    # 等待所有线程下载完成
                for t in thread_list:
                    t.join()  # 阻塞主进程，进行完所有线程后再运行主进程

                if self.video_success:
                    merge_ts_file.merge(self.ts_file_list, self.dir_path, self.title + '.mp4')
                if ((self.title + '.mp4' in os.listdir(self.dir_path) and
                     os.path.getsize(os.path.join(self.dir_path,
                                                  self.title + '.mp4')) > 0) or  # 只有合并了才算成功(存在'title'.ts或是av.mp4且大小不为0)
                        ('av.mp4' in os.listdir(self.dir_path) and  # av.mp4是路径过长而无法改名导致的
                         os.path.getsize(os.path.join(self.dir_path, 'av.mp4')) > 0)):
                    print('\n%s 合并成功\n' % self.title)  # 视频下载完成就算任务完成，图片和预览视频允许失败
                    with open('SAVED.txt', 'a+', encoding='utf-8') as f:
                        f.write(str(self.video_num) + '\n')
                else:
                    with open('merge fail.txt', 'w', encoding='utf-8') as f:
                        f.write(self.video_num + '\n')
                    if self.final_fail_ts_file_list:
                        for i in self.final_fail_ts_file_list:
                            print(i, end=' ')
                        print('final fail! NO merge ts_file!')
                        print(self.title + ' 失败结束')

    def write(self):
        file_path = os.path.join(self.dir_path, 'information.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('标题：\n%s\n网址：\n%s\n' % (self.title, self.url))

    def download(self):
        if self.right_url() and not self.should_pass('SAVED.txt') and not self.should_pass('NO EXISTS.txt'):
            self.count = 0
            self.html = self.repeat_request(self.url, fail_hint="'get html fail and retry %d'%retry_times",
                                            final_fail_hint='get html fianl fail! Exit!')
            if self.html:
                self.html = self.html.decode('utf-8')
                if self.mkdir():
                    self.download_image()
                    self.download_preview_video()
                    self.download_video()
                    self.write()
                    return True


if __name__ == '__main__':
    # url = input('请输入网址：\n')
    url = 'https://www.xvideos.com/video35904115/who_is_this_girl_'
    start = time.perf_counter()
    xvideos = Xvideos(url)
    xvideos.download()
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end - start) // 3600, (end - start) % 3600 // 60, (end - start) % 60))
