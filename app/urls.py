from django.urls import include, path
from . import views
from .views import View
urlpatterns = [
    path('', views.home_view , name='home_view'),
    path('line_view/pt<str:pt>ln<str:ln>/', views.line_view, name='line_view'),
]