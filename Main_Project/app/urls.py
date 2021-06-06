
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',home , name = "home"),
    path('register/',signup , name = "signup"),
    path('login/',signin , name = "signin"),
    path('profile/',profile , name = "profile"),
    path('profile/<key>/',seeprofile , name = "seeprofile"),

    # path('userprofile/',userprofile , name = "userprofile"),
    path('edit-profile/',editprofile , name = "editprofile"),
    # path('edit-worker-profile/',editworkerprofile , name = "editworkerprofile"),

    path('logout/' , logout , name = 'logout'),

    path('about/',about , name = "about"),
    path('search/',search , name = "search"),
    path('myworks/',myworks , name = "myworks"),

    path('work/description/<id>', workDescription , name = "workDescription"),



    path('search',search , name = "search"),










]
