import re

html = r'bookmarks_2019_8_16.html'
with open(html,'r',encoding='utf-8') as f1:
    with open('xvideos_urls.txt','w',encoding='utf-8') as f2:
        for line in f1:
            url = re.search(r'https?://www.xvideos.com/video\d+?.*?(?=")',line)
            if url:
                f2.write(url.group()+'\n')
                
with open('xvideos_urls.txt','r',encoding='utf-8') as f2:
    print(len(f2.readlines()))