VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))
from helpers import Hashlink
from django.conf import settings
from models import _import_from_string
import datetime
if hasattr(settings, 'HASHLINK_CURRENT_DATETIME_FUNCTION'):
    current_datetime_function = _import_from_string(settings.HASHLINK_CURRENT_DATETIME_FUNCTION)
    if not current_datetime_function:
        current_datetime_function = datetime.datetime.now()
else:
    current_datetime_function = datetime.datetime.now()
hashlink_functions = Hashlink(current_datetime_function=current_datetime_function)


def hashlink_register(*setting_args, **setting_kwargs):
    """
    """
    no_args = False
    function = None
    if len(setting_args) == 1 \
        and not setting_kwargs \
        and callable(setting_args[0]):
        # We were called without args
        function = setting_args[0]
        no_args = True
        raise "Needs at least one parameter - category name"
    else:
        category_name = setting_args[0]
    def second_wrapper(function):
        from functools import wraps
        from . import hashlink_functions
        hashlink_functions.register(category_name, function)
        @wraps(function)
        def third_wrapper(request, *args, **kwargs):
            return function(request, *args, **kwargs)
        return third_wrapper
    if no_args: #it's different with or without arguments
        return second_wrapper(function)
    else:
        return second_wrapper
