介绍:盘古运维系统包括：发布管理/计划任务管理/资产管理
具体的模块介绍参看 readme文档的开发路程介绍
即将上线新版本，因为自己前端有点渣，改的比较慢。
下图第一个图为即将上线的新版本，还没全部改完。

20170615
此平台已经并将会慢慢演变成运维系统，现在实现了发布管理，任务管理（crontab管理），下一步把资产管理和dnspod之类的整合进去，现在正在写CMDB资产管理

简单的代码发布系统，测试于Windows机器，功能暂不完善，可提供一个思路
目前实现了 代码更新和回滚。
可以发布到预发布机，等在预发布机测试通过后，再从预发布机上rsync到其他服务器

rsync使用了sshkey的登录方式，root除去了输入密码的对话框

使用
可以登录到后台，添加主机添加SVN的项目添加组（暂时没用到）添加从预发布机到其他机器
svn更新代码时有点问题，获取当前登录用户 用了全局变量，更改代码重启过后客户端不退出在操作svn更新的时候会出现未定义的变量。
所以设置了回话超时。多久以后没有操作在操作就得重新登录

相应的目录和用户需要提前创建好。比如 /svndata/repos 

环境 py2.7 Django1.10

使用时需要有搭建svn服务器，用于测试使用

此版本例子 SVN服务器:192.168.17.129
           代码发布系统运行在了自己的本地win7系统上。
		   用户名/密码 admin/1234.abcd
		   
		   
		   
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/1.png)
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/2.png)
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/3.png)
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/4.png)
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/5.png)
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/6.png)
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/7.png)
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/8.png)
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/9.png)
![image](https://github.com/mumulizi/svnmanager/blob/master/picture/10.png)


		   
		   

		   