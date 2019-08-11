import os
import re
import functools

def cmp(a,b):
    na = re.search(r'(\d+).ts', a).group(1)
    nb = re.search(r'(\d+).ts', b).group(1)
    if int(na) > int(nb):
        return 1
    else:
        return -1

def merge_less_100(ts_file_list, dir_path, name):
    
    ffmpeg_path = r'C:\CS\ffmpeg\bin\ffmpeg.exe'    #ffmpeg绝对路径
    win_merge = 2             #windows下合并ts视频的方式，1为copy/b，2为ffmpeg

    if os.name == 'nt':    #windows
        pan = re.search(r'^[a-zA-Z]:',dir_path)    
    elif os.name == 'posix':
        pan = re.search(r'^/root',dir_path)
    
    if pan:    #dir_path是绝对路径
        dir_path2 = dir_path
    else:    #dir_path是相对路径
        run_path = os.path.dirname(os.path.abspath('__file__'))
        dir_path2 = os.path.join(run_path, dir_path)        #最终都获得绝对路径

    ts_file_list = sorted(ts_file_list,key=functools.cmp_to_key(cmp))
    if os.name == 'nt' and win_merge == 1:    #copy/b
        input_file = '+'.join(ts_file_list)
    elif os.name == 'posix' or (os.name == 'nt' and win_merge == 2):    #ffmpeg
        input_file = '|'.join(ts_file_list)
    output_file = name
    
    if os.name == 'nt':
        command = ''
        #command = 'chcp 65001 & '    #cmd编码设为utf-8
        command += 'cd /d "%s" & ' % dir_path2
        if win_merge == 1:    #copy/b
            command += 'copy/b %s "%s" & ' % (input_file, output_file)
        elif win_merge == 2:    #ffmpeg
            if not re.match(r'new\d+?.ts',output_file):    #ts视频数大于100的第二轮合并或是ts视频数小于100的合并（output_file名为最终文件名的都要经过中间名称，output_file为new\d的不用）
                command += '%s -i "concat:%s" -y -acodec copy -vcodec copy -crf 0 "%s" & '%(ffmpeg_path,input_file,'av.mp4')    #使用ffmpeg将ts合并为mp4    #使用替身名称，否则ffmpeg遇utf-8字符不工作
            else:    #ts视频数大于100的第一轮合并
                command += '%s -i "concat:%s" -y -acodec copy -vcodec copy -crf 0 "%s" & '%(ffmpeg_path,input_file,output_file)
        os.popen(command).read()
        if ( (name in os.listdir(dir_path) and 
              os.path.getsize(os.path.join(dir_path,name))>0 ) or 
             ('av.mp4' in os.listdir(dir_path) and    #av.mp4是路径过长而无法改名导致的
              os.path.getsize(os.path.join(dir_path,'av.mp4'))>0) ):    #合并成功再删除ts文件
            command = ''
            command += 'cd /d "%s" & ' % dir_path2
            for i in ts_file_list:
                command += 'del /Q %s $ ' % i
            os.popen(command).read()
            #with open('4.txt','a+',encoding='utf-8')as f:
            #    f.write(command+'\n\n\n')
        if win_merge ==2 and not re.match(r'new\d+?.ts',output_file):
            command = ''
            command += 'cd /d "%s" & ' % dir_path2
            command += 'ren "%s" "%s"' % ('av.mp4', output_file)    #再把名字换回去    #av后要有文件格式的后缀，否则ffmpeg报错
            os.popen(command).read()
        
    elif os.name == 'posix':    #linux采用ffmpeg合并  #ffmpeg后面加上-logevel quiet 不向控制台打印信息  #-crf 0为无损  #-y遇到同名文件则覆盖
        command = ''
        command += 'cd "%s" && '%dir_path2    #进入视频所在路径
        command += 'ffmpeg -i "concat:%s" -y -loglevel quiet -acodec copy -vcodec copy -crf 0 "%s" && '%(input_file,output_file)    #使用ffmpeg将ts合并为mp4
        for i in ts_file_list:
            command += 'rm -rf %s && '%i
        
    #os.popen(command).read()    #os.pepen不会弹出cmd的黑框    #使用read()巧妙地阻塞os.popen
    '''
    1、多条命令时不能调用多个os.system或os.popen命令
       因为每条命令都是单独的一个进程
       比如改变了路径后，但下一个os.system或os.popen又回到了最初的路径
       可以将每条命令用&间隔开，然后一次执行
    2、在windows命令提示符下使用的字符串的最大的长度 8191 个字符。 
       数量巨大时分批处理
    '''

def merge(ts_file_list, dir_path, name):
    if os.name == 'nt':
        if len(ts_file_list)<=100:
            merge_less_100(ts_file_list, dir_path, name)
        else:
            ts_file_list = sorted(ts_file_list,key=functools.cmp_to_key(cmp))
            for i in range((len(ts_file_list)-1)//100+1):
                merge_less_100(ts_file_list[i*100:i*100+100], dir_path, 'new%d.ts'%i)
            new_ts_file_list = []
            for file in os.listdir(dir_path):
                if re.match(r'new\d+?.ts', file):
                    new_ts_file_list.append(file)
            merge_less_100(new_ts_file_list, dir_path, name)
    elif os.name == 'posix':
        merge_less_100(ts_file_list, dir_path, name)    #未测试