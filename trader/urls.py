from django.conf.urls import url
from webshop import settings


urlpatterns = [
	url(r'^register/$', 'trader.views.register_view'),
	url(r'^my_account/$', 'my_account_view'),
	url(r'^orders_info/$', 'order_info_view'),
	url(r'^blog/$', AllCategories.as_view()),
	url(r'^blog/(?P<slug>[-\w]+)/$', CategoryList.as_view()),
]

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^login/$', 'login', {'template_name': 'registration/login.html', 'SSL': settings.ENABLE_SSL },
		name='login'),
)