import datetime
from django.conf import settings

class Hashlink(object):
    def __init__(self, *args, **kwargs):
        import datetime
        self.current_datetime_function = kwargs.get('current_datetime_function', datetime.datetime.now)
        super(Hashlink, self).__init__()

        self.function_map = dict(default_action=("hashphrase.views","default_action_on_error"),
            default_action2=("hashphrase.views","test_success"))


    def register(self, category_name, function):
        self.register_function(function.__module__,
                               function.__name__,
                               function.__doc__, category_name)

    def register_function(self, module, name, doc, category_name):
        """
        Register function at 'module' depth
        """
        if category_name in self.function_map:
            return

        self.function_map[category_name] = (module, name)

    def get_category_names(self):
        """
        """
        return self.function_map.keys()

    def get_module_and_function(self, category_name):
        return self.function_map.get(category_name, (None,None))


def _correct_import(name):
    m = __import__(name)
    for n in name.split(".")[1:]:
        m = getattr(m, n)
    return m

def _import_from_string(long_name, file_only=False):
    try:
        last_dot = long_name.rfind('.')
        module_name = long_name[:last_dot]
        function_name = long_name[last_dot+1:]
        module = _correct_import(module_name)
        if not file_only:
            func = vars(module)[function_name]
        else:
            func = None
    except Exception, ex:
        func = None
    return func


def init_package():
    if hasattr(settings, 'HASHPHRASE_CURRENT_DATETIME_FUNCTION'):
        current_datetime_function = _import_from_string(settings.HASHPHRASE_CURRENT_DATETIME_FUNCTION)
        if not current_datetime_function:
            current_datetime_function = datetime.datetime.now()
    else:
        current_datetime_function = datetime.datetime.now()
    return Hashlink(current_datetime_function=current_datetime_function)

hashphrase_functions = init_package()

def hashphrase_register(*setting_args, **setting_kwargs):
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
        hashphrase_functions.register(category_name, function)
        @wraps(function)
        def third_wrapper(request, *args, **kwargs):
            return function(request, *args, **kwargs)
        return third_wrapper
    if no_args: #it's different with or without arguments
        return second_wrapper(function)
    else:
        return second_wrapper

try:
    from importlib import import_module
except:
    from django.utils.importlib import import_module

LOADING_HASHPHRASE = False
def hashphraseviews_autodiscover():
    """
    Auto-discover INSTALLED_APPS hashphraseviews.py modules and fail silently when
    not present. NOTE: dajaxice_autodiscover was inspired/copied from
    django.contrib.admin autodiscover
    """
    global LOADING_HASHPHRASE
    if LOADING_HASHPHRASE:
        return
    LOADING_HASHPHRASE = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:

        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('hashphraseviews', app_path)
        except ImportError:
            continue

        import_module("%s.hashphraseviews" % app)

    LOADING_HASHPHRASE = False
