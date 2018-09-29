from django.conf.urls import url
from . import views

app_name = 'clubs'

urlpatterns = [
	url(r'^home/$',views.index,name='home'),
	url(r'^signin/$',views.signin,name='signin'),
	url(r'^postsign/$',views.postsign,name='postsign'),
	url(r'^addclub/$',views.addclub,name='addclub'),	
]