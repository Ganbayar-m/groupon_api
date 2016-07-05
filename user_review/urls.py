from django.conf.urls import url

from user_review import views

urlpatterns = [
    url(r'', views.user_review)
]