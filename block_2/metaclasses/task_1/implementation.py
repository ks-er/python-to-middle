class Updateable(type):

    __newCls = None

    def __new__(cls, name, bases, kwargs):
        if not cls.__newCls:
            cls.__newCls = type.__new__(cls, name, bases, kwargs)
        return cls.__newCls

    def __init__(self, name, bases, kwargs):
        attrs = ((name, value) for name, value in kwargs.items() if not name.startswith('__'))

        for name, value in attrs:
            setattr(self, name, value)
