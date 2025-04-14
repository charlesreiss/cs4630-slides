from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^danger/?$', views.danger, name='danger'),
    url(r'^danger-framedeny/?$', views.danger_noframe, name='danger-framedeny'),
    url(r'^danger-nocsrf/?$', views.danger_nocsrf, name='danger-nocsrf'),
    url(r'^secret/?$', views.secret, name='secret'),
    url(r'^secret-framedeny/?$', views.secret_noframe, name='secret-framedeny'),
    url(r'^readable/?$', views.readable, name='readable'),
    url(r'^reset-danger/?$', views.reset_danger, name='danger'),
]
