# xvdieos视频爬虫

网址：www.xvideos.com

需要科学上网

## 功能

​	可实现单个视频下载、一个页面上所有视频下载、关键字搜索下载、最佳影片下载、标签页视频下载，下载包括30张图片、2张内容略图、预览视频、正片。

## 依赖

python3：requests，bs4，lxml

linux：`apt-get install ffmpeg`

windows：[ffmepg](<https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20190722-3883c9d-win64-static.zip> "windows ffmpeg x64下载" )（可以使用系统自带的copy/b下位代替）

## 写在前面

* #### 关于代理

  本程序默认：

  * windows下采用http协议代理，端口为1080
  * linux下采用http协议代理，端口为8118

  可在 **down_one.py** 中修改proxies的值来更换代理方式

  后面会简单介绍如何搭建能运行本程序的代理环境

* #### 变量更改

  * 根目录root_path，线程数num_thread，超时时限timeout，重新请求次数retry在 **down_one.py** 中修改

  * windows下ffmpeg的绝对路径ffmpeg_path，windows下使用copy/b或是ffmpeg的关联量win_merge在 **merge_ts_file.py** 中修改

* #### 关于邮件

  如果需要程序出错时向自己的邮箱发送邮件，需要修改sendEmail.py中的fromAdd, toAdd, \_pwd, 分别为发件邮箱地址，收件邮箱地址，发件邮箱[授权码](https://jingyan.baidu.com/article/8ebacdf065a1f149f65cd5b5.html "网易邮箱如何设置授权码")

* #### 视频合并

  下载的ts视频需要合并，windows下可自行选择copy/b或ffmpeg合并，linux下采用ffmpeg合并。

  事实证明相较于ffmpeg合并的视频，采用copy/b合并的视频又大又卡又模糊（卡顿十分明显），请自行斟酌（默认ffmpeg，可在**merge_ts_file.py** 修改win_merge的值来更换）


## 文件简介

* #### 主程序

  **down_one.py** 下载单个视频

  **down_some.py**  读取xvideos_urls.txt，下载视频

  **down_group.py** 下载关键字搜索出来的视频、最佳影片、标签视频

* #### 辅助程序

  **merge_ts_file.py** 合并ts视频文件

  **sendEmail.py** 发送邮件

  **exception_handling.py** 程序异常时写入异常日志，并发送邮件

  **get_favorite_urls.py** 手动从浏览器中导出收藏夹后，使用本程序可提取出其中的xvideos的url

  **get_saved.py** 获取指定目录下，已经下载过的视频，并存入SAVED.txt，适用于删除了某些视频时更新SAVED.txt

* #### 其他文件

  **xvideos_urls.txt** down_some.py从此文本中读入要爬取的视频网址

  **xvideos.log**  异常日志

  **SAVED.txt** 存放已经下载的视频的编号

  **NO EXISTS.txt** 存放不存在或被删除的视频的编号

  **ERROR.txt**  存放下载失败的ts文件信息（很鸡肋）

  **TAG NAME.txt** 存放自己指定的标签所对应的名称（用于通过down_group.py下载某个标签的前n页视频时，若曾经给此标签指定过名称，则提示是否沿用曾经指定的名称）

  **information.txt** 写入网页的标题与网址

## 代理介绍

* ### windows

  若使用ShadowsocksR客户端客户端科学上网，且使用默认设置，则该程序拿来就能用

* ### linux

  代理过程：provoxy 监听8118端口的http流量，将其转发给1080端口的sock5代理，并走 shadowsocks 到墙外。

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
  sudo /etc/init.d/privoxy force-reload   # 不重启服务的情况下重新加载配置
  ```

  VPS重启后需要重新启动ssr和privoxy，也可以设为启动项

参考：

[Linux安装并使用ssr客户端](https://blog.mrwang.pw/2018/12/13/Linux%E5%AE%89%E8%A3%85%E5%B9%B6%E4%BD%BF%E7%94%A8ssr/ )

[使用 privoxy 转发 socks 到 http ](http://einverne.github.io/post/2018/03/privoxy-forward-socks-to-http.html )

## 更新日志

* 2019.8.10

  windows下创建文件夹时，文件夹名称最后一个字符是空格时，系统会删除此空格作为名称。解决了一个源此的bug

* 2019.8.8

  由于类的初始化不正确导致**down_group.py** 下载一个页面的所有视频时，下载到的图片都是同一组。已修复。

  同时增添**get_saved.py** 

* 2019.7.23

  * 分离出merge_ts_file.py，在windows中引入ffmpeg，并解决copy/b不能合并过多ts文件的问题（cmd中字符串长度限制在八千多一些）

    （注意：合并ts视频的功能尚未在linux上测试）

  * 引入下载某图片或ts视频前检测是否存在的机制，存在则不再下载
  * 修改下载成功的条件，只有文件夹内存在title.ts且大小不为0，方写入SAVED.txt，避免合并失败却依旧写入SAVED.txt

* 2019.7.22

  * 文本名称包含html实体时则将html实体转换，如&hel lip;转换为省略号

  * 解决OSError: [Errno 36] File name too long

* 2019.7.21

  * 发现windows下ts文件过多时似乎不会合并，网上也有人遇到这种问题，可能是copy命令的锅

* 2019.7.20 

  * 晚 增添down_group.py

  * 午 基本完成

* 2019.7.16 

  * 晚 开始琢磨写这个爬虫

