from django.conf.urls import patterns, url
from webshop import settings


urlpatterns = patterns('webshop.accounts.views',
	# Форма регистрации
	url(r'^register/$', 'register_view',
		{'template_name': 'registration/register.html' }, # , 'SSL': settings.ENABLE_SSL
		name='register'),
	# Просмотр аккаунта пользователя
	url(r'^my_account/$', 'my_account_view',
		{'template_name': 'registration/my_account.html'},
		name='my_account'),
	url(r'^orders_info/$', 'order_info_view',
		{'template_name': 'registration/order_info.html'},
		name='order_info'),
	url(r'^blog/$', AllCategories.as_view()),
	url(r'^blog/(?P<slug>[-\w]+)/$', CategoryList.as_view()),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^login/$', 'login', {'template_name': 'registration/login.html', 'SSL': settings.ENABLE_SSL },
		name='login'),
)