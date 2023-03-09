celery -A DELLINK worker -P gevent

celery -A DELLINK beat -l INFO


if we need to run on another <IP> just change it to be like ... py manage.py runserver <IP>
and change websocket on FrontEnd to be <IP> 

D09
10.195.220.7
9000

CN08
10.195.220.30
5000

CN05
10.195.220.21
5000

CNBU : Control networking business unit
DCBU : Direct current business unit.

docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management

noVNC run on nginx **command > start ngnix <**
nginx -s quit

@maximegris/node-websockify    to proxy single server connection
@sukkis/node-multi-websockify   to proxy multiple server connection