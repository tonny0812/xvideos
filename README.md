# xvdieos视频爬虫

网址：www.xvideos.com

需要科学上网

## 依赖

python3：requests

linux：ffmpeg

## 写在前面

* #### 关于代理

  本程序默认在windows下采用1080端口的http协议代理，在linux下采用8118端口的http协议代理（小白搞不懂的话后面会简单介绍如何搭建能运行本程序的代理环境，大神可以自己在down_one.py的Xvideos类的request函数中修改proxies的值来更换代理方式，墙外人可以删掉代理的语句）

* #### 关于邮件

  如果需要程序出错时向自己的邮箱发送邮件，需要修改sendEmail.py中的fromAdd, toAdd, \_pwd, 分别为发件邮箱地址，收件邮箱地址，发件邮箱[授权码](https://jingyan.baidu.com/article/8ebacdf065a1f149f65cd5b5.html "网易邮箱如何设置授权码")

* #### 视频合并

  下载的ts视频需要合并，windows下采用copy/b合并，linux下采用ffmpeg合并。

  事实证明相较于ffmpeg合并的视频，采用copy/b合并的视频又大又卡又模糊（卡顿十分明显），因此推荐使用linux平台运行本爬虫。

  欢迎大佬在评论区告知我window下更好的合并方法。

## 文件简介

* #### 主程序

  **down_one.py** 下载单个视频

  **down_some.py**  读取xvideos_urls.txt，下载视频

  **down_group.py** 下载关键字搜索出来的视频、最佳影片、标签视频

* #### 辅助程序

  **sendEmail.py** 发送邮件

  **exception_handling.py** 程序异常时写入异常日志，并发送邮件

  **get_favorite_urls.py** 手动从浏览器中导出收藏夹，使用本程序可提取出其中的xvideos的url

* #### 其他文件

  **xvideos_urls.txt** down_some.py从此文本中读入要爬取的视频网址

  **SAVED.txt** 存放已经下载的视频的编号

  **NO EXISTS.txt** 存放不存在或被删除的视频的编号

  **ERROR.txt**  存放下载失败的ts文件信息（很鸡肋）

  **TAG NAME.txt** 存放自己指定的标签所对应的名称（用于通过down_group.py下载某个标签的前n页视频时，若曾经给此标签指定过名称，则提示是否沿用曾经指定的名称）

  **xvideos.log**  异常日志

## 代理介绍

pass（过几天写）

## 流水账

* 2019.7.20 

  * 晚 增添down_group.py

  * 午 基本完成

* 2019.7.16 

  * 晚 开始琢磨写这个爬虫