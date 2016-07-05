from django.conf.urls import url

from question import views

urlpatterns = [
    url(r'',views.question),
]