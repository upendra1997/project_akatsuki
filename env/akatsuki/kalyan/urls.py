from django.conf.urls import url
from kalyan import views

urlpatterns = [
    url(r'^$', views.index, name='kalyan_index'),
 	url(r'^register$', views.register, name='kalyan_register'),
 	url(r'^register/accept$', views.accept, name='kalyan_register_accept'),
 	url(r'^login$', views.login, name='kalyan_login'),
 	url(r'^about$', views.about, name='kalyan_about'),
 	url(r'^feedback$', views.feedback, name='kalyan_feedback'),
 	url(r'^scomplain$', views.scomplain, name='kalyan_scomplain'),
 	url(r'^logout$', views.logout, name='kalyan_logout'),
 	url(r'^public_views/(?P<vtype>[\w\-]+)/(?P<ctype>[\w\-]+)/$', views.public_views, name='kalyan_public_views'),
 	url(r'^view_detail/(?P<vtype>[\w\-]+)/(?P<id>\d+)/$', views.public_view_detail, name='kalyan_public_view_detail'),

]