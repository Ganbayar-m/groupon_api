
from django.conf.urls import url, include
from django.contrib import admin

from organisation import views

urlpatterns = [
    url(r'', views.organisation),
]
