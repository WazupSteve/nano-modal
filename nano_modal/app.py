"""
User Facing API : "App" class is the entrypoint for using this library
App class is a container.
It holds the name of the application.
It holds the registry of all the functions that belong to the application.
"""
# Usage of double decorator

from .function import Function


class App:
    def __init__(self, name):
        self.name = name
        self.functions = {}

    def function(self, image=None):
        def decorator(func):
            wrapped = Function(func, image=image)
            self.functions[func.__name__] = wrapped
            return wrapped

        return decorator
