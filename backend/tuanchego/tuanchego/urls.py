from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tuanchego.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin.old/', include(admin.site.urls)),
)

import xadmin

xadmin.autodiscover()

from django.conf import settings
from data.views import BaseView
urlpatterns = urlpatterns + patterns(
    '',
    url(r'admin/', include(xadmin.site.urls)),
    url(r'^$', BaseView.as_view(), name='base_view'),
    )

##=============api===============
import users.urls
urlpatterns = urlpatterns + patterns(
    '',
    url(r'api/user/', include(users.urls)),

)

import cars.urls
urlpatterns = urlpatterns + patterns(
    '',
    url(r'api/cars/', include(cars.urls)),

)

import activities.urls
urlpatterns = urlpatterns + patterns(
    '',
    url(r'api/acts/', include(activities.urls)),

)