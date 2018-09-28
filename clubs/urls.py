from django.conf.urls import url
from . import views

app_name = 'clubs'

urlpatterns = [
	url(r'^home/$',views.index,name='home'),
]