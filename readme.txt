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