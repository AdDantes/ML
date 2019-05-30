
from django.conf.urls import url
from .views import *
#
urlpatterns = [
    url('^$',login),
    url('^register/$', register_show),
    url('^register_handle/$', register_handle),
    url('^login_check/$', login_check),

]
