from django.urls import path, include
from checklist.views import *
from django.contrib.auth import views as auth_views

app_name = 'checklist'
urlpatterns = [
    #task list,add,update,delete
    path('taskall', TaskView.as_view(), name="AllTask"),
    path('taskadd', TaskView.as_view(), name="TaskAdd"),
    path('taskupdate/<str:pk>', TaskView.as_view(), name="TaskUpdate"),
    path('taskdelete/<str:pk>', TaskView.as_view(), name="TaskDelete"),
    #check list,add,update,delete

    path('checkall', CheckView.as_view(), name="CheckLisk"),
    path('checkadd', CheckView.as_view(), name="CheckAdd"),
    path('checkupdate/<str:pk>', CheckView.as_view(), name="CheckUpdate"),
    path('checkdelete/<str:pk>', CheckView.as_view(), name="CheckDelete"),
]