from django.conf.urls import url

from answer import views

urlpatterns = [
    url(r'', views.answer)
]