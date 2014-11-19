class Hashlink(object):
    def __init__(self, *args, **kwargs):
        import datetime
        self.current_datetime_function = kwargs.get('current_datetime_function', datetime.datetime.now)
        super(Hashlink, self).__init__()

        self.function_map ={}


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


