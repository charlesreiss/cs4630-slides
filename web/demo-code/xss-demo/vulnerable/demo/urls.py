from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^danger/?$', views.danger, name='danger'),
    re_path(r'^danger-framedeny/?$', views.danger_noframe, name='danger-framedeny'),
    re_path(r'^danger-nocsrf/?$', views.danger_nocsrf, name='danger-nocsrf'),
    re_path(r'^secret/?$', views.secret, name='secret'),
    re_path(r'^secret-framedeny/?$', views.secret_noframe, name='secret-framedeny'),
    re_path(r'^readable/?$', views.readable, name='readable'),
    re_path(r'^reset-danger/?$', views.reset_danger, name='danger'),
]
