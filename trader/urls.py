from django.conf.urls import url
from . import views
from trader.views import AllCategories

urlpatterns = [
	url(r'^register/$', views.register_view),
	url(r'^my_account/$', views.my_account_view),
	url(r'^orders_info/$', views.order_info_view),
	# url(r'^blog/$', AllCategories.as_view()),
	# url(r'^blog/(?P<slug>[-\w]+)/$', CategoryList.as_view()),
]

urlpatterns += [
	url(r'^login/$', views.login),
]