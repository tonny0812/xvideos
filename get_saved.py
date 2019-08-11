import re, os

root_path = r'E:\仓殷禀阜\xvideos'
list = []
for dir in os.listdir(root_path):
    for dir2 in os.listdir(os.path.join(root_path, dir)):
        for dir3 in os.listdir(os.path.join(root_path, dir, dir2)):
            with open(os.path.join(root_path, dir, dir2, dir3, 'information.txt'),errors='ignore')as f:
                list.append(re.search(r'https://www.xvideos.com/video(\d+)/',f.read()).group(1))
                
with open('SAVED.txt','w') as f:
    for i in list:
        f.write(i+'\n')