from exception_handling import log_exception
import down_one
import time


@log_exception
def downloads():
    global urls_txt
    urls_txt = 'xvideos_urls.txt'
    with open(urls_txt,'r',encoding='utf-8') as f:
        urls_list=f.readlines()
    for i, url in enumerate(urls_list):
        print('进度： %d/%d'%(i+1, len(urls_list)))
        print('网址:  %s'%url[:-1])    #去除url末尾的'\n'
        xvideos = down_one.Xvideos(url)
        xvideos.download()
        print()
               
if __name__ == '__main__':
    start = time.perf_counter()
    downloads()
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60)) 