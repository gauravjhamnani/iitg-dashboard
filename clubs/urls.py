from django.conf.urls import url
from . import views

app_name = 'clubs'

urlpatterns = [
	url(r'^home/$',views.index,name='home'),
	url(r'^signin/$',views.signin,name='signin'),
	url(r'^postsign/$',views.postsign,name='postsign'),
	url(r'^addclub/$',views.addclub,name='addclub'),	
	url(r'^club/(?P<pk>[a-zA-Z]+)/$',views.displayclub,name='displayclub'),
	url(r'^club/(?P<pk>[a-zA-Z]+)/desc/$',views.desc,name="desc"),
	url(r'^club/(?P<pk>[a-zA-Z]+)/addannouncement/$',views.addannouncement,name="addannouncement"),
	url(r'^club/(?P<pk>[a-zA-Z]+)/addevent/$',views.addevent,name="addevent"),
	url(r'^club/(?P<pk>[a-zA-Z]+)/addresource/$',views.addresource,name="addresource"),
]
