import abc


class Shape(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        pass


class ShapeDecorator(Shape, metaclass=abc.ABCMeta):

    def __init__(self, decoratedShape):
        self._decoratedShape = decoratedShape

    def draw(self):
        self._decoratedShape.draw();


class BorderShapeDecorator(ShapeDecorator):

    def draw(self):
        self._decoratedShape.draw()
        self.setRedBorder()

    @abc.abstractmethod
    def setRedBorder(self):
        pass


class RedShapeDecorator(BorderShapeDecorator):

    def setRedBorder(self):
        print('Цвет границы: красный')


class GreenShapeDecorator(BorderShapeDecorator):

    def setRedBorder(self):
        print('Цвет границы: зеленый')


class Circle(Shape):

    def draw(self):
        print('Я круг!')


class Rectangle(Shape):

    def draw(self):
        print('Я прямоугольник!')

class Triangle(Shape):

    def draw(self):
        print('Я треугольник!')


if __name__ == '__main__':
    circle = Circle()
    redCircle = RedShapeDecorator(Circle())
    greenRectangle = GreenShapeDecorator(Rectangle())
    redTriangle = RedShapeDecorator(Triangle())

    circle.draw()
    redCircle.draw()
    greenRectangle.draw()
    redTriangle.draw()