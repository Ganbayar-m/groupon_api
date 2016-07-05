
from django.conf.urls import url, include
from django.contrib import admin

from user_register import views

urlpatterns = [
    url(r'', views.user_register),
]
