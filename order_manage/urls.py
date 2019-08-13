from django.conf.urls import url

from order_manage import views

urlpatterns = [
   url(r'^$', views.order),
   url(r'^order_handle/$', views.order_handle),
]
