# xvdieos视频爬虫

网址：www.xvideos.com

需要科学上网

## 依赖

python3：requests，bs4

linux：`apt-get install ffmpeg`

## 写在前面

* #### 关于代理

  本程序默认：

  * windows下采用http协议代理，端口为1080
  * linux下采用http协议代理，端口为8118

  可在down_one.py的Xvideos类的request函数中修改proxies的值来更换代理方式

  后面会简单介绍如何搭建能运行本程序的代理环境

* #### 关于邮件

  如果需要程序出错时向自己的邮箱发送邮件，需要修改sendEmail.py中的fromAdd, toAdd, \_pwd, 分别为发件邮箱地址，收件邮箱地址，发件邮箱[授权码](https://jingyan.baidu.com/article/8ebacdf065a1f149f65cd5b5.html "网易邮箱如何设置授权码")

* #### 视频合并

  下载的ts视频需要合并，windows下采用copy/b合并，linux下采用ffmpeg合并。

  事实证明相较于ffmpeg合并的视频，采用copy/b合并的视频又大又卡又模糊（卡顿十分明显），而且ts文件过多时无法合并，因此推荐使用linux平台运行本爬虫。

  欢迎大佬在评论区告知我window下更好的合并方法。（发现ffmpeg也可以在windows上安装，然后在python中通过subprocess.call(command, shell=True)调用，不过懒得写了，反正我用不到，谁家的爬虫会在自己的电脑上跑啊。有需要的可以自己写一下，不麻烦）

## 文件简介

* #### 主程序

  **down_one.py** 下载单个视频

  **down_some.py**  读取xvideos_urls.txt，下载视频

  **down_group.py** 下载关键字搜索出来的视频、最佳影片、标签视频

* #### 辅助程序

  **sendEmail.py** 发送邮件

  **exception_handling.py** 程序异常时写入异常日志，并发送邮件

  **get_favorite_urls.py** 手动从浏览器中导出收藏夹后，使用本程序可提取出其中的xvideos的url

* #### 其他文件

  **xvideos_urls.txt** down_some.py从此文本中读入要爬取的视频网址

  **xvideos.log**  异常日志

  **SAVED.txt** 存放已经下载的视频的编号

  **NO EXISTS.txt** 存放不存在或被删除的视频的编号

  **ERROR.txt**  存放下载失败的ts文件信息（很鸡肋）

  **TAG NAME.txt** 存放自己指定的标签所对应的名称（用于通过down_group.py下载某个标签的前n页视频时，若曾经给此标签指定过名称，则提示是否沿用曾经指定的名称）

## 代理介绍

* ### windows

  若使用ShadowsocksR客户端客户端科学上网，且使用默认设置，则该程序拿来就能用

* ### linux

  流程：provoxy 监听8118端口的http流量，将其转发给1080端口的sock5代理，并走 shadowsocks 到墙外。

  **以下为程序运行环境配置**

  (以下操作在阿里云Ubuntu16.4上通过)

  `apt-get update` 

  更新源

  `sudo apt-get install git` 

  安装git

  `git clone http://git.mrwang.pw/Reed/Linux_ssr_script.git`

   在具有写权限的目录执行如下命令获取到ssr脚本仓库

  `cd Linux_ssr_script && chmod +x ./ssr` 

  进入刚刚克隆的仓库目录并赋予`ssr`脚本执行权限

  `sudo mv ./ssr /usr/local/sbin/`

  将脚本放入可执行脚本的目录

  `ssr install `

  安装ssr，脚本会下载ssr客户端并移动到合适的位置

  `ssr config`

  编辑配置文件，在里面输入你的节点连接信息，然后保存。

  ​	配置文件内容形如

  ```
  {
      "server": "服务器地址",
      "local_address": "127.0.0.1",
      "local_port": 1080,
      "timeout": 300,
      "workers": 1,
      "server_port": 80,
      "password": "密码",
      "method": "none",
      "obfs": "http_post",
      "obfs_param": "download.windowsupdate.com",
      "protocol": "auth_chain_a",
      "protocol_param": "3412:H2LChD"
  }
  ```

  ​	科学上网的节点这里不提供，请自行准备

  `sudo apt install privoxy` 

  安装privoxy

  `vim /etc/privoxy/config`

  ​	默认的配置文件地址在 `/etc/privoxy/config` 目录下。假设本地 1080 端口已经启动，然后要将本地 1080 socks5 代理转成 http 代理，重要的配置只有两行。

  ```
  # 把本地 HTTP 流量转发到本地 1080 SOCKS5 代理
  forward-socks5t / 127.0.0.1:1080 .
  # 可选，默认监听本地连接
  listen-address 127.0.0.1:8118
  ```

  使用如下命令启动

  ```
  sudo /etc/init.d/privoxy start
  sudo /etc/init.d/privoxy reload   # 不重启服务的情况下重新加载配置
  ```

参考：


## 更新日志

* 2019.7.22
  * 解决OSError: [Errno 36] File name too long
* 2019.7.21
  * 发现windows下ts文件过多时似乎不会合并，网上也有人遇到这种问题，可能是copy命令的锅
* 2019.7.20 
  * 晚 增添down_group.py

  * 午 基本完成
* 2019.7.16 
  * 晚 开始琢磨写这个爬虫