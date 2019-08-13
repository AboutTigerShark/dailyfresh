from django.conf.urls import url
from goods_manage import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^(\d+)/$', views.detail),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.list),
]


