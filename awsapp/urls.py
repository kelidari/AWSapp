from django.urls import path, include
from .  import views
from django.conf.urls import url
import sys

app_name= 'aws'
urlpatterns= [
    path('upload/', views.file_upload , name='upload'),
    path('', views.file_download , name='download'),
    path('delete/', views.file_delete , name='delete'),



]


