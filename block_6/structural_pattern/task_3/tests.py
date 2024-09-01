import unittest

from block_6.structural_pattern.task_3.implementation import Picture, Line, Circle, Rectangle, Text


class MyTestCase(unittest.TestCase):

    def test_picture(self):
        pic = Picture()
        pic.add(Line())
        pic.add(Circle())
        pic.add(Rectangle())
        pic.add(Text())
        pic.draw()

        line = pic.get_child(0)
        line.draw()  # Линия

        self.assertEqual(pic.get_child_count(), 4)
