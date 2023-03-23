# from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
]