from exception_handling import log_exception
import down_one
import time, re


def delete_the_nth_line_in_file(del_line):    #从网上搞来的轮子,del_line为行数
    with open(urls_txt, 'r', encoding='utf-8') as old_file:
        with open(urls_txt, 'r+', encoding='utf-8') as new_file:
            current_line = 0
            # 定位到需要删除的行
            while current_line < (del_line - 1):
                old_file.readline()
                current_line += 1
            # 当前光标在被删除行的行首，记录该位置
            seek_point = old_file.tell()
            # 设置光标位置
            new_file.seek(seek_point, 0)
            # 读需要删除的行，光标移到下一行行首
            old_file.readline()  
            # 被删除行的下一行读给 next_line
            next_line = old_file.readline()
            # 连续覆盖剩余行，后面所有行上移一行
            while next_line:
                new_file.write(next_line)
                next_line = old_file.readline()
            # 写完最后一行后截断文件，因为删除操作，文件整体少了一行，原文件最后一行需要去掉
            new_file.truncate()


def remove_successful_url_from_urls_file():    
    #当爬取完某一网页后，将该url从文本中删除，针对crawler_for_img_multiple_urls.py
    with open(urls_txt, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f):  
            line = line[:-1]
            if re.match(r'\d+',line):    #line是帖子序号
                url_serial_number_from_txt = line
                
                url_number = re.search(r'www\.xvideos\.com/video(\d+?)/', line)    #line是帖子网址
                if url_number:
                    url_serial_number_from_url = url_number.group(1)   
                   
                    if url_serial_number_from_txt == url_serial_number_from_url:
                        delete_the_nth_line_in_file(line_number+1)


@log_exception
def downloads():
    global urls_txt
    urls_txt = 'xvideos_urls.txt'
    with open(urls_txt,'r',encoding='utf-8') as f:
        urls_list=f.readlines()
    for i, url in enumerate(urls_list):
        print('进度： %d/%d'%(i+1, len(urls_list)))
        print('网址:  %s'%url[:-1])    #去除url末尾的'\n'
        if down_one.download(url):
            remove_successful_url_from_urls_file()
        print()
               
if __name__ == '__main__':
    start = time.perf_counter()
    downloads()
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60))        
