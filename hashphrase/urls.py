import hashphrase.views as hashphrase_view
from django.conf.urls import url

urlpatterns = [
    url(r'^test/', hashphrase_view.hash_link_test),
    url(r'^(?P<key>.*)/$', hashphrase_view.hash_link),
]
