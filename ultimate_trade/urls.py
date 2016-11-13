from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'ultimate_trade.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
    url(r'^api/', include('trader.urls')),
]
