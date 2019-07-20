# xvdieos视频爬虫

网址：www.xvideos.com

需要科学上网

## 写在前面

* #### 关于代理

  本程序默认在windows下采用1080端口的http协议代理，在linux下采用8118端口的http协议代理（小白搞不懂的话后面会简单介绍如何搭建能运行本程序的代理环境，大神可以自己在down_one.py的Xvideos类的request函数中修改proxies的值来更换代理方式，墙外人可以删掉代理的语句）

* #### 关于邮件

  如果需要程序出错时向自己的邮箱发送邮件，需要修改sendEmail.py中的fromAdd, toAdd, \_pwd, 分别为发件邮箱地址，收件邮箱地址，发件邮箱[授权码](https://jingyan.baidu.com/article/8ebacdf065a1f149f65cd5b5.html "网易邮箱如何设置授权码")

## 文件简介

* #### 主程序

  **down_one.py** 下载单个视频

  **down_some.py**  读取xvideos_urls.txt，下载视频

* #### 辅助程序

  **sendEmail.py** 发送邮件

  **exception_handling.py** 程序异常时写入异常日志，并发送邮件

  **get_favorite_urls.py** 手动从浏览器中导出收藏夹，使用本程序可提取出其中的xvideos的url

## 代理介绍

pass（过几天写）

## 流水账

* 2019.7.16晚 开始琢磨写这个爬虫