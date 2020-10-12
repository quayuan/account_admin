from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    # path('', views.IndexView.as_view()),
]