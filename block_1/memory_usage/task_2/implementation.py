import weakref


class MyObject:

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


def cache(func):
    """
    Обертка, помещающая объект в кэш
    """
    def wrapper(myObjectName):

        if not hasattr(wrapper, '_cache'):
            wrapper._cache = weakref.WeakValueDictionary()

        if (myObjectName not in wrapper._cache):
            value = func(myObjectName)
            wrapper._cache[myObjectName] = value

        return wrapper._cache[myObjectName]

    return wrapper


@cache
def create_object(name):
    return MyObject(name)
