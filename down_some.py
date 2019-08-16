from exception_handling import log_exception
import down_one
import time, os


@log_exception
def downloads():
    #dir_name = input('请输入文件夹名称（最终文件存放于root_path/00-来自文本/自定义文件夹名）:')
    dir_name = '20190817'
    urls_txt = 'xvideos_urls.txt'
    with open(urls_txt,'r',encoding='utf-8') as f:
        urls_list=f.readlines()
    for i, url in enumerate(urls_list):
        print('进度： %d/%d'%(i+1, len(urls_list)))
        print('网址:  %s'%url[:-1])    #去除url末尾的'\n'
        xvideos = down_one.Xvideos(url)
        xvideos.root_path = os.path.join(xvideos.root_path, '00-来自文本', dir_name)
        xvideos.download()
        print()

if __name__ == '__main__':
    start = time.perf_counter()
    downloads()
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60))