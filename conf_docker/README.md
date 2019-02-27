### 正式使用说明
#### 1.conf_docker文件夹里的内容应该与manage.py 同级 
> `mv -f conf_docker/* . `
#### 2.创建docker image
> 如果已经创建过，记得删除： `rm -rf uwsgi_docker.sock`
> `docker build -t django2.0:1.0 . `
#### 3.修改uwsgi.ini
> 写上相对路径：module= tianjing_lt_video.wsgi:application
> 测试需要将  py-autoreload=1 注释
#### 4.修改supervisor-app.conf
> 写上该模块名： command= celery -A tianjing_lt_video worker --loglevel=INFO 
#### 5.创建docker container
* 端口映射  -p 8001:80  
* 容器名称 --name dev_reports  
* 项目文件目录 -v  path_to_your_project_code:/home/code/app  
* 容器nginx日志：/var/log/nginx/  
* session,cache 数据
* rabbitmq数据
> `docker run -d -p 8801:80  --name dev_pinche --restart=always -v /home/code/dev/pinche:/home/code/app -v /home/logs/dev/pinche/docker:/home/logs -v /home/session/dev/pinche/docker:/home/session -v /home/cache/dev/pinche/docker:/home/cache -v /home/logs/dev/pinche/docker/rabbitmq:/data/rabbitmq/mnesia sichuan_yd_video:1.0  `开发
> `docker run -d -p 8002:80 --name online_pinche --restart=always -v /home/code/online/pinche:/home/code/app -v /home/logs/online/pinche/docker:/home/logs -v /home/session/online/pinche/docker:/home/session -v /home/cache/online/pinche/docker:/home/cache  -v /home/logs/online/pinche/docker/rabbitmq:/data/rabbitmq/mnesia django2.0:1.0  `正式
    

### 容器操作 
以下的6c33d849a971为容器id
* 进入终端页面  
>`docker exec -it 969fb21c364e /bin/bash`
* 查看supervisorctl 状态
> `docker exec -it 969fb21c364e supervisorctl status`
* 重启supervisor
> `docker exec -it 969fb21c364e supervisorctl reload`
* 重启uwsgi
> `docker exec -it 969fb21c364e supervisorctl restart app-uwsgi`
> `docker exec -it dev_tianjing_lt_video supervisorctl restart app-uwsgi`
* 重启nginx
> `docker exec -it 969fb21c364e supervisorctl restart nginx-app`
* 当有些启动不起来，比方rabbitmq，可以先ps 关闭进程，然后再用supervisorctl 重启
* rabbitmq 启动不起来还有一个原因是 rabbitmq-start 为windows环境，这个时候需要将它设置为linux的
vi  /usr/local/bin/rabbitmq-start
 :set ff   如果是doc则改为
 :set ff=unix  就好了

### 参考链接
* https://github.com/yangtao4389/django-uwsgi-nginx



 
## 创建mysql容器
* 创建docker_mysql  
> `docker pull mysql:5.7`  
> `docker run --name mysql_server -p 13306:3306 -v /home/docker_mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=mysqlpwd -d mysql:5.7`  
* 进入mysql  
> `docker exec -it mysql_server   /bin/bash`  
> `mysql -uroot -p`  
> `mysqlpwd`   密码  
* 创建账号   
> `CREATE USER 'username'@'host' IDENTIFIED BY 'password';`  
* 远程root密码  
> `GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'WjPbASDWLPUAqwHj' ;`

* 创建远程用户  
> `CREATE USER 'renheanxin'@'%' IDENTIFIED BY 'tA1aS2lu!gj3PTg^';`  
> `CREATE USER 'renheanxintest'@'%' IDENTIFIED BY '00%v1@eAKQDURagg';`

* 分配数据库给该用户  
> `GRANT ALL ON test_tianjing_lt_video.* TO 'renheanxintest'@'%'  ;`  
> `flush privileges;`
### docker上所有的mysql账户名与密码都是统一的



