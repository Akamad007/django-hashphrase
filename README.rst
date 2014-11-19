=====
django-hashlink
=====

Hashlink is a django module that facilitates the process that
users click on a link in an email and django handles the click.
Hashlink makes it easy to generate such a link, authenticate it or not,
calls a custom function or not, etc.

Quick start
-----------

1. Add "hashlink" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'hashlink',
    )

2. Include the hashlink URLconf in your project urls.py like this::

    url(r'^hl/', include('hashlink.urls')),

3. ...