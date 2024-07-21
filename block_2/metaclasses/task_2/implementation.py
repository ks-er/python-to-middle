class LazyMeta(type):

    def __call__(cls, expression, *args):
        expression_result = expression()
        new_cls = LazyMeta.__new__(
            LazyMeta,
            cls.__name__,
            (type(expression_result),),
            { expression.__name__: expression }
        )

        instance = super().__call__(new_cls, expression, expression_result, *args)

        return instance

    def __new__(self, cls_name, expression_result, dict):
        new_cls = super().__new__(
            self,
            cls_name,
            expression_result,
            dict)

        return new_cls


class Lazy(metaclass=LazyMeta):

    def __new__(self, cls_instance, expression, expression_result, *args):
        # Проверка на class
        if hasattr(expression_result, '__module__'):
            res = cls_instance.__new__(
                cls_instance
            )
        else:
            res = cls_instance.__new__(
                cls_instance,
                expression_result,
                *args
            )

        return res
