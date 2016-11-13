from django.conf.urls import include, url
from . import views
from trader.views import ROUTER

urlpatterns = [
	url(r'^', include(ROUTER.urls)),
	url(r'^register/$', views.register_view),
	url(r'^login/$', views.login_view),
	url(r'^my_account/$', views.my_account_view),
	url(r'^orders_info/$', views.order_info_view),
]
