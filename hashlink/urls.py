from django.conf.urls import *

urlpatterns = patterns('',
    (r'^test/', 'hashlink.views.hash_link_test'),
    (r'^(?P<key>.*)/$', 'hashlink.views.hash_link'),
)