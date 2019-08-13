from django.conf.urls import url
from user_manage import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^logout', views.logout),
    url(r'^info/$', views.info),
    url(r'^order/$', views.order),
    url(r'^user_order(\d+)/$', views.user_center_order),
    url(r'^site/$', views.site),
]
