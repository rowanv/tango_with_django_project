from django.conf.urls import include, url, patterns
from django.contrib import admin
from rango import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
)