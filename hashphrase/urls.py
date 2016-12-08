import hashphrase.views as hashphrase_view

urlpatterns = [
    (r'^test/', hashphrase_view.hash_link_test),
    (r'^(?P<key>.*)/$', hashphrase_view.hash_link),
]
