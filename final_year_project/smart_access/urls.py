from django.conf.urls import patterns, url
from smart_access import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^validate/', views.validate, name='validate'),
    url(r'^fileUpload/$', views.upload_dataset, name='upload_dataset'),
    url(r'^/add/$', views.add_dataset, name='add_dataset'),
    url(r'^verify/$', views.verify_user, name='verify_user'),
    url(r'^granted/$', views.access_granted, name='access_granted'),
    url(r'^sendMail/$', views.send_email, name='send_email'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^passkey/$', views.passkey_auth, name='passkey_auth'),
    url(r'^admin/$', views.admin_panel, name='admin_panel'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    )
