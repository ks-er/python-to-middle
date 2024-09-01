import abc


class Graphic(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        pass

    def add(self, obj):
        pass

    def remove(self, obj):
        pass

    def get_child(self, index):
        pass


class Line(Graphic):
    def draw(self):
        print('Линия')

class Circle(Graphic):
    def draw(self):
        print('Круг')

class Rectangle(Graphic):
    def draw(self):
        print('Прямоугольник')


class Text(Graphic):
    def draw(self):
        print('Текст')


class Picture(Graphic):
    def __init__(self):
        self._children = []

    def draw(self):
        print('Изображение')
        # вызываем отрисовку у вложенных объектов
        for obj in self._children:
            obj.draw()

    def add(self, obj):
        if isinstance(obj, Graphic) and not obj in self._children:
            self._children.append(obj)

    def remove(self, obj):
        index = self._children.index(obj)
        del self._children[index]

    def get_child(self, index):
        return self._children[index]

    def get_child_count(self):
        return len(self._children)