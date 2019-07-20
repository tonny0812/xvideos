import re
import os
import requests
import threading
import functools


def cmp(a,b):
    na = re.search(r'(\d+).ts', a).group(1)
    nb = re.search(r'(\d+).ts', b).group(1)
    if int(na) > int(nb):
        return 1
    else:
        return -1


class Xvideos:
 
    def __init__(self, url):
        self.url = url
        self.root_path = r'xvideos'    #默认根目录为本程序所在目录下的xvideos文件夹
        self.num_thread = 10           #默认线程
        self.timeout = 10              #超时时间设置
        self.retry = 10                #最大重试次数
        self.html = ''
        self.title = ''
        self.success = True
        self.wrong_ts_infor = ''
        self.wrong_pic_infor = ''
        self.ts_file_list = []
        self.final_fail_ts_file_list = []
        self.final_fail_pic_list = []


    def should_pass(self, text_name):
        if not os.path.exists(text_name):
            return False
        else:
            video_num = re.search(r'video(\d+)', self.url).group(1)
            with open(text_name, 'r') as f:
                for line in f:
                    if line[:-1] == video_num:
                        if text_name == 'SAVED.txt':
                            print('此视频已下载，跳过\n')
                        elif text_name == 'DELETED.txt':
                            print('此视频已被删除，跳过\n')
                        return True
                return False


    def request(self, url, headers={}):
        if os.name == 'nt':    #windows
            proxies={'http': '127.0.0.1:1080', 'https': '127.0.0.1:1080'}    #ssr的win客户端采用1080端口的http协议
        elif os.name == 'posix':    #linux
            proxies={'http': '127.0.0.1:8118', 'https': '127.0.0.1:8118'}    #ssr+privoxy,通过privoxy将1080端口的socks协议转发给8118端口的http协议
        response = requests.get(url, timeout=self.timeout, proxies=proxies, headers=headers)
        return response.content


    def repeat_request(self, url, headers={}, fail_hint='', final_fail_hint=''):
        retry_times = 1
        while retry_times <= self.retry:
            try:
                response = self.request(url,headers={})
                return response
            except:
                if fail_hint:
                    print(eval(fail_hint))
            retry_times += 1
        else:    #while else 结构，正常时（不正常是指因为break return 异常等而退出循环）运行else内的语句
            if final_fail_hint:
                print(final_fail_hint)


    def mkdir(self):
        
        self.title = re.search(r'<h2 class="page-title">(.*?)<span class="duration">', self.html)
        if self.title:
            self.title = self.title.group(1).rstrip()
            self.title = re.sub(r'[\\\*\?\|/:"<>\.]', '', self.title)
            print('名称：', self.title)
            self.dir_path = os.path.join(self.root_path, self.title)
            if not os.path.exists(self.dir_path):
                os.makedirs(self.dir_path)
            return True
        else:
            print("No title! Maybe the url isn't xvideos or the video has deleted! Exit!")
            return False


    def thread_image(self, pic_num, pic_key):
        keyword = r"html5player\.%s\('(.*?)'\);" % pic_key
        url = re.search(keyword, self.html).group(1)
        img = self.repeat_request(url, fail_hint='"'+pic_num+'.jpg fail and retry '+'%d"%retry_times', final_fail_hint=pic_num+'.jpg final fail!')
        if img:
            img_type = url.split('.')[-1]
            file_path = os.path.join(self.dir_path, pic_num+'.'+img_type)
            with open(file_path, 'wb') as fb:
                fb.write(img)
            #print('PIC %s success'%pic_num)
        else:
            self.final_fail_pic_list.append(pic_num)
            self.wrong_pic_infor += "{'%s': '%s'}\n"%(url,self.dir_path)


    def download_image(self):
        pic_dict = {'1': 'setThumbUrl',
                    '2': 'setThumbUrl169',
                    '3': 'setThumbSlide',
                    '4': 'setThumbSlideBig'}
        thread_list = []
        for i in pic_dict:
            t = threading.Thread(target=self.thread_image, kwargs={'pic_num': i, 'pic_key': pic_dict[i]})
            t.setDaemon(True)    #设置守护进程
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()    #阻塞主进程，进行完所有线程后再运行主进程


    def download_ts_file(self, ts_url):    
        #print(1,ts_url)
        '''
        re_str = r'(?:hls-\d{3,4}p(\d+.ts))|(?:hls-\d{3,4}p-[a-zA-Z0-9]{5}(\d+.ts))'
        #目前见过两种，相对路径的前缀分别形如hls-720p3.ts， hls-360p-ba36e0.ts
        re_result = re.search(re_str, ts_url)
        if re_result.group(1):
            ts_name = re_result.group(1)
        elif re_result.group(2):
            ts_name = re_result.group(2)    #这么多行代码全都是re的正向零宽断言必须定长的锅，不得不采用这种迂回的写法，难道就不能搞个语法糖吗
        '''
        re_str = r'hls-\d{3,4}p(?:-[a-zA-Z0-9]{5})?(\d+.ts)'
        ts_name = re.search(re_str, ts_url).group(1)
        ts_file = self.repeat_request(ts_url, headers={'Connection': 'close'}, fail_hint='"'+ts_name +' fail and retry '+'%d"%retry_times', final_fail_hint=ts_name+' final failed! Add it into ERROR.txt')
        if ts_file:
            file_path = os.path.join(self.dir_path, ts_name)
            with open(file_path, 'ab') as f:
                f.write(ts_file)
                f.flush()
            self.count += 1
            print("\r下载进度：%.2f%%" % (self.count/self.ts_num*100), end='')
            self.ts_file_list.append(ts_name)
        else:
            with open('ERROR.txt', 'a+', encoding='utf-8') as f:
                f.write("{'%s': '%s'}\n"%(ts_url, self.dir_path))
            self.success = False
            self.final_fail_ts_file_list.append(ts_name)
            self.wrong_ts_infor += "{'%s': '%s'}\n"%(ts_url,self.dir_path)    #最后写入信息.txt


    def thread_video(self, start, end, part):    
        for num, ts_url in enumerate(self.ts_url_list[start:end]):
            try:
                self.download_ts_file(ts_url)
            except:
                self.success = False
                raise
        
        
    def merge_ts_file(self):    
        if os.name == 'nt':    #windows采用copy/b合并(但是合并出来的视频相较于linux的ffmpeg而言，又大又卡又模糊S)
            
            pan = re.search(r'^[a-zA-Z]:',self.dir_path)    
            if pan:    #dir_path是绝对路径
                dir_path2 = self.dir_path
            else:    ##dir_path是相对路径
                run_path = os.path.dirname(os.path.abspath('__file__'))
                dir_path2 = os.path.join(run_path, self.dir_path)        #最终都获得绝对路径
            
            self.ts_file_list = sorted(self.ts_file_list,key=functools.cmp_to_key(cmp))
            input_file = '+'.join(self.ts_file_list)
            output_file = self.title+'.ts'
            
            cmd_str = ''
            cmd_str += 'cd /d "%s" & ' % dir_path2
            cmd_str += 'copy/b %s "%s" & ' % (input_file, output_file)
            for i in self.ts_file_list:
                cmd_str += 'del /Q %s $' % i
                
            os.system(cmd_str)
            #print(os.popen(cmd_str).read())    #os.popen()除了可以实现os.system的功能外，还多了一个输出控制台内容的功能
            '''
            另外要注意，多条命令时不能调用多个os.system或os.popen命令
            因为每条命令都是单独的一个进程
            比如改变了路径后，但下一个os.system或os.popen又回到了最初的路径
            可以将每条命令用&间隔开，然后一次执行
            '''
        elif os.name == 'posix':    #linux采用ffmpeg合并  #ffmpeg后面加上-loglevel quiet 不向控制台打印信息
            pan = re.search(r'^/root',self.dir_path)
            if pan:    #dir_path是绝对路径
                dir_path2 = self.dir_path
            else:    #dir_path是相对路径
                run_path = os.path.dirname(os.path.abspath('__file__'))
                dir_path2 = os.path.join(run_path, self.dir_path)        #最终都获得绝对路径
            
            self.ts_file_list = sorted(self.ts_file_list,key=functools.cmp_to_key(cmp))
            #print(self.ts_file_list)
            input_file = '|'.join(self.ts_file_list)
            output_file = self.title + '.mp4'
            
            command = ''
            command += 'cd "%s" && '%dir_path2    #进入视频所在路径
            command += 'ffmpeg -i "concat:%s" -loglevel quiet -acodec copy -vcodec copy -absf aac_adtstoasc "%s" && '%(input_file,output_file)    #使用ffmpeg将ts合并为mp4
            command += 'rm -f *.ts  && '
            command += 'mv "%s.mp4" "%s.ts"' % (self.title, self.title)
            #指行命令
            os.system(command)
            

    def download_video(self):    #结构为：获取ts链接，多线程爬取，合并
        m3u8_url = re.search(r"html5player\.setVideoHLS\('(.*?)'\);",self.html).group(1)    #总的m3u8链接
        #print(m3u8_url)
        m3u8_content = self.repeat_request(m3u8_url, fail_hint="'get m3u8 fail and retry %d'%retry_times", final_fail_hint='get m3u8 fail! Exit!')    #内含不同的清晰度所对应的m3u8链接
        if m3u8_content:
            base_url = re.search(r"(.*?)hls.m3u8", m3u8_url).group(1)    #从m3u8_url中取出，留待拼接
            m3u8_content = m3u8_content.decode('utf-8')
            #print('m3u8_content ', m3u8_content)
            #print()
            definition_list = re.findall(r'NAME="(.*?)p"', m3u8_content)
            max_definition = max(definition_list)    #找到最高清晰度
            #print(max_definition)
            line_list = m3u8_content.split('\n')
            for line in line_list:
                if 'hls-' in line and max_definition in line:
                    max_definition_m3u8_url = line    #最高清晰度的m3u8链接(相对路径)
                    #print(max_definition_m3u8_url)
            max_definition_m3u8_url = base_url + max_definition_m3u8_url
            #print('max_definition_m3u8_url', max_definition_m3u8_url)
            max_definition_m3u8_content = self.repeat_request(max_definition_m3u8_url, fail_hint="'get max_definition_m3u8 fail and retry %d'%retry_times", final_fail_hint='get max_definition_m3u8 final fail! Exit!')    #内含该m3u8视频的ts文件信息
            if max_definition_m3u8_content:
                max_definition_m3u8_content = max_definition_m3u8_content.decode('utf-8')
                #print('max_definition_m3u8_content:',max_definition_m3u8_content)
                self.ts_url_list = []
                for line in max_definition_m3u8_content.split('\n'):
                    if '.ts' in line:
                        self.ts_url_list.append(base_url + line)
                self.ts_num = len(self.ts_url_list)
                #print(1,self.ts_url_list)
                #print('has gotten ts urls')
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
                    self.num_thread = self.ts_num    #线程数若大于ts文件数，则线程数减少到ts文件数
                part = self.ts_num // self.num_thread  # 分块。如果不能整除，最后一块应该多几个字节
                thread_list = []
                for i in range(self.num_thread):
                    start = part * i    #第part个线程的起始url下标
                    if i == self.num_thread - 1:   #最后一块
                        end = self.ts_num    #第part个线程的终止url下标
                    else:
                        end = start + part    #第part个线程的终止url下标
                    t = threading.Thread(target=self.thread_video, kwargs={'start': start, 'end': end, 'part': part})
                    t.setDaemon(True)    #设置守护进程；必须在start()之前设置；如果为True则主程序不用等此线程结束后再结束主程序；当我们使用setDaemon(True)方法，设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行，可能出现的情况就是，子线程的任务还没有完全执行结束，就被迫停止
                    t.start()
                    thread_list.append(t)
                    # 等待所有线程下载完成
                for t in thread_list:
                    t.join()    #阻塞主进程，进行完所有线程后再运行主进程
                
                if self.success:    #图片失败不算失败
                    self.merge_ts_file()
                    print('\n%s 下载完成' % self.title)
                    video_num = re.search(r'video(\d+)', self.url).group(1)
                    with open('SAVED.txt','a+', encoding='utf-8') as f:
                        f.write(video_num+'\n')
                else:
                    print()
                    if self.final_fail_ts_file_list:
                        for i in self.final_fail_ts_file_list:
                            print(i,end=' ')
                        print('final fail! NO merge ts_file!')
                        print(self.title+' 失败结束')
                    
                  
    def write(self):
        file_path = os.path.join(self.dir_path, '信息.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('标题：\n%s\n网址：\n%s\n'%(self.title, self.url))
            if self.final_fail_pic_list:
                for i in self.final_fail_pic_list:
                    f.write(i,'.jpg ')
                f.write('\n\nfinal fail!\n\n%s'%self.wrong_pic_infor)
            if self.final_fail_ts_file_list:
                for i in self.final_fail_ts_file_list:
                    f.write(i+' ')
                f.write('\n\nfinal fail! NO merge ts_file!\n\n%s'%self.wrong_ts_infor)
                    

    def download(self):
        if not self.is_saved():
            self.count = 0
            self.html = self.repeat_request(self.url, fail_hint="'get html fail and retry %d'%retry_times", final_fail_hint='get html fianl fail! Exit!')
            if self.html:
                self.html = self.html.decode('utf-8')
                if self.mkdir():
                    self.download_image()
                    self.download_video()
                    self.write()
                    return True
                else:
                    return False
                    

def download(url):
    xvideos = Xvideos(url)
    xvideos.download()
    

if __name__ == '__main__':
    #url = 'https://www.xvideos.com/video40421333/_'
    #url = 'https://www.xvideos.com/video40807117/_' 
    #url = 'https://www.xvideos.com/video41666493/_'
    #url = 'https://www.xvideos.com/video31640165/019_helen_part_1_-_fuckasianbeauty.com'
    #url = 'https://www.xvideos.com/video42935697/_-_._._hx410410'
    url = input('请输入网址：\n')
    download(url)