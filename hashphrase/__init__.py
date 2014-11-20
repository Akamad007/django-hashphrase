VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))
from helpers import Hashlink
from django.conf import settings
from models import _import_from_string
import datetime
if hasattr(settings, 'HASHPHRASE_CURRENT_DATETIME_FUNCTION'):
    current_datetime_function = _import_from_string(settings.HASHPHRASE_CURRENT_DATETIME_FUNCTION)
    if not current_datetime_function:
        current_datetime_function = datetime.datetime.now()
else:
    current_datetime_function = datetime.datetime.now()
hashphrase_functions = Hashlink(current_datetime_function=current_datetime_function)

if hasattr(settings, 'HASHPHRASE_HANDLERS'):
    from models import _import_from_string
    for func_str in settings.HASHPHRASE_HANDLERS:
        #trigger parsing so they registered
        _import_from_string(func_str)

