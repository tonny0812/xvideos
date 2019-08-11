from exception_handling import log_exception
import down_one
from bs4 import BeautifulSoup
import time, os, re, traceback


def download_videos_of_one_page(url='', page_type='01-单页下载'):    #page_type表示该页面是什么类型的，比如说是最佳影片，比如说搜索关键字是XX
    if traceback.extract_stack()[-2][2] == 'choice':
        url = input('请输入网址：')
        dir_name = input('请输入文件夹名称（最终文件存放于root_path/01-单页下载/自定义文件夹名）:')
    xvideos = down_one.Xvideos()
    if traceback.extract_stack()[-2][2] == 'choice':
        root_path = os.path.join(xvideos.root_path, page_type, dir_name)
    else:
        root_path = os.path.join(xvideos.root_path, page_type)
    html = xvideos.repeat_request(url, final_fail_hint='request %s final fail'%url)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        tag_list = soup.select('div.thumb-inside div.thumb a')
        urls_list = ['https://www.xvideos.com'+tag['href'] for tag in tag_list]
        for i, url in enumerate(urls_list):
            print('当前页进度： %d/%d'%(i+1, len(urls_list)))
            print('网址： %s'%url)
            xvideos = down_one.Xvideos(url)
            xvideos.root_path = root_path
            xvideos.download()
            xvideos.ts_file_list = []
            print()


def search_videos_pages():    #视频搜索    #n=1表示默认只下载第一页的所有视频
    search_key = input('请输入搜索关键字：')
    base_url = r'https://www.xvideos.com/?k=%s' % search_key
    n = input('请输入爬取页数：')
    for page in range(int(n)):
        if page != 0:
            url = base_url + r'&p=%d'%page    #第二页的?p=1,依次类推
        else:
            url = base_url
        print('第%s页，共%s页' % (page+1, int(n)))
        download_videos_of_one_page(url, os.path.join('02-视频搜索', search_key))


def best_videos_pages():    #最佳影片
    data = input('请输入年月，格式形如2019-06：')
    base_url = r'https://www.xvideos.com/best/%s/' % data
    n = input('请输入爬取页数：')
    for page in range(int(n)):
        if page != 0:
            url = base_url + str(page)
        else:
            url = base_url
        print('第%s页，共%s页' % (page+1, int(n)))
        download_videos_of_one_page(url, os.path.join('03-最佳影片', data))    #视频文件夹保存在root_path/02-最佳影片/年月


def tag_videos_pages():    #视频标签0
    '''
    标签的url的页数get传值有好几种（并不通用）:
    一种是关键字搜索类型的（本质上就是搜索了标签中的字），如https://www.xvideos.com/?k=3d&p=2
    一种是不同的语言的、以及真·标签（tags）的，如https://www.xvideos.com/lang/chinese/2和https://www.xvideos.com/tags/big-ass/2/
    还有一种形如https://www.xvideos.com/c/2/ASMR-229
    类型太多，不同类型的标签名所在位置不同，提取出标签名称太麻烦，
    而且中文标签可能会提取出原来的英文标签，所以就不提取了，输入网址后由使用者自行键入标签名
    '''
    #url = 'https://www.xvideos.com/c/Teen-13'    ok
    url = input('请输入视频标签的第一页的网址：')
    tag_name = ''
    if os.path.exists('TAG NAME.txt'):
        with open('TAG NAME.txt','r',encoding='utf-8') as f1:
            for line in f1:
                if url+' ' in line:
                    tag_name = re.search(r' (.*?)\n', line).group(1)#TAG NAME.txt中的一行，前为url，后为tag_name,空格间隔
                    if input('本标签名称曾被指定为%s，是否沿用该名称？(y/n)'%tag_name) != 'y':
                        with open('TAG NAME.txt','w',encoding='utf-8') as f2:    #不沿用旧名称则将旧名称从文件中删掉
                            for line in f1:
                                if not url in line:
                                    f2.write(line)
                        tag_name = input('请指定标签名称：')
                    break
    if not tag_name:
        tag_name = input('请指定标签名称：')
        
    exists = False
    if os.path.exists('TAG NAME.txt'):
        with open('TAG NAME.txt','r',encoding='utf-8') as f:
            exists = False
            for line in f:
                if url in line:
                    exists = True    
    if not exists:   
        with open('TAG NAME.txt','a+',encoding='utf-8') as f:
            f.write(url+' '+tag_name+'\n')
            
    xvideos = down_one.Xvideos()
    html = xvideos.repeat_request(url, final_fail_hint='request %s final fail'%url)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        tag_list = soup.select('div.pagination ul li a')
        page2_url = tag_list[1]['href']
        page3_url = tag_list[2]['href']
        before = ''
        after = ''
        for i in range(len(page2_url)):
            if page2_url[i] != page3_url[i]:    #通过比较该标签的第二页和第三页的url的不同找出页数在url中的位置   #如果视频只有一页或两页，会出错
                before = page2_url[:i]
                after = page2_url[i+1:]
                break
        if before:    #如果页数在url的最后，则after是空串
            n = input('请输入爬取页数：')
            for page in range(int(n)):
                if page != 0:
                    url = 'https://www.xvideos.com' + before + str(page) + after    #url去除不同部分，与页数拼接得到第page页的url
                    print(url)
                print('第%s页，共%s页' % (page+1, int(n)))
                download_videos_of_one_page(url, os.path.join('04-视频标签', tag_name))    #视频文件夹保存在root_path/02-最佳影片/年月
        else:
            print('出错了，请检查该标签的第二页和第三页的url是否存在不同')


@log_exception
def choice():
    choice_type = input('请选择批量下载的类型：\n1-单页下载    2-视频搜索\n3-最佳影片    4-视频标签\n\nPS：4-视频标签的爬取必须保证视频页数大于等于3，否则请使用1次或2次1-单页下载\n请键入对应数字：')
    if choice_type == '1':
        download_videos_of_one_page()
    if choice_type == '2':
        search_videos_pages()
    if choice_type == '3':
        best_videos_pages()
    if choice_type == '4':
        tag_videos_pages()


if __name__ == '__main__':
    url = 'https://www.xvideos.com/'
    url = 'https://www.xvideos.com/history'
    #url = 'https://www.xvideos.com/lang/japanese'  ok
    #url = 'https://www.xvideos.com/lang/korean/1'
    #search_videos_pages(2)
    start = time.perf_counter()
    choice()
    end = time.perf_counter()
    print('任务执行共%d小时%d分%.2f秒' % ((end-start)//3600,(end-start)%3600//60,(end-start)%60))
    