pip install uwsgi
#  测试uwsgi启动django,注意http后面是有空格的--http :8000
uwsgi --http :8000 --module mysite.wsgi

#/etc/nginx/conf.d新建一个mysite.conf文件，插入下面内容

# the upstream component nginx needs to connect to
upstream django {
# server unix:///path/to/your/mysite/mysite.sock; # for a file socket
server 127.0.0.1:8000; # for a web port socket (we'll use this first)
}
# configuration of the server

server {

listen      8081;  # 监听端口
server_name 192.168.0.111 ; # 绑定域名或者ip
charset     utf-8;

# max upload size
client_max_body_size 75M;   # adjust to taste

# Django media
location /media  {
    alias /home/panda/all_envs/Mysite/mysite/media;  # 指向django的media目录
}
# 指向django的static目录
location /static {
    alias /home/panda/all_envs/Mysite/mysite/static; # 
}

# Finally, send all non-media requests to the Django server.
location / {
    uwsgi_pass  django;
    include     uwsgi_params; # the uwsgi_params file you installed
}
}
上面nginx的意思是当访问192.168.0.111:8081的时候，会吧所有的请求转发到127.0.0.1:8000，也就是
upstream django(上游路由)，而django路由是uwsgi启动的，所以下面配置uwsgi启动是要配置scoket为127.0.0.1:8000端口，
不然和nginx配置不一致也不行,会暴露502 bad request请求错误

setting.py配置如下：
	# nginx静态文件目录
	STATIC_ROOT = os.path.join(BASE_DIR,"static/")
	还得吧STATICFILES_DIRS注释掉，因为这两个是不能同时存在的
-----------------------------------------------------------------------------------------------------
以配置文件的方式启动uwsgi,在项目下创建一个uwsgi.ini文件，插入一下内容：

新建uwsgi.ini 配置文件， 内容如下：

# mysite_uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)　项目根目录
chdir           = /home/panda/all_envs/Mysite/mysite
# Django's wsgi file　django项目wsgi文件路径
module          = mysite.wsgi
# the virtualenv (full path)

# process-related settings
# master　开启主进程
master          = true
# maximum number of worker processes　10个子进程
processes       = 10
# the socket (use the full path to be safe　8000端口
socket          = 127.0.0.1:8000
# ... with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum          = true
# 虚拟环境
virtualenv = /home/panda/all_envs/Mysite
# 日志文件目录
logto = /tmp/mylog.log
--------------------------
注：
    chdir： 表示需要操作的目录，也就是项目的目录
    module： wsgi文件的路径
    processes： 进程数
    virtualenv：虚拟环境的目录
    如果配置了logto选项，启动uwsgi可能会一直卡在uwsgi初始化那里，因为日志文件被重定向了，看不到日志，实际上已经启动了。
配置好后，启动虚拟环境，执行uwsgi命令
workon mxonline
uwsgi -i 你的目录/Mxonline/conf/uwsgi.ini &

# uwsgi重启
pkill -f uwsgi 这样杀死进程uwsgi今后会自动重启