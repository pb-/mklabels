import unittest

from ..main import ImpossibleLayout, TooManyLabels, layout, render


class MainTestCase(unittest.TestCase):
    def test_layout_normal(self):
        (rows, columns) = layout(297, 210, 15, 56, 13, 2, 1)
        self.assertEqual((rows, columns), (9, 4))

    def test_layout_maximal(self):
        (rows, columns) = layout(297, 210, 15, 261, 174, 2, 1)
        self.assertEqual((rows, columns), (1, 1))

    def test_layout_width_error(self):
        with self.assertRaises(ImpossibleLayout):
            (rows, columns) = layout(297, 210, 15, 262, 174, 2, 1)

    def test_layout_height_error(self):
        with self.assertRaises(ImpossibleLayout):
            (rows, columns) = layout(297, 210, 15, 261, 175, 2, 1)

    def test_render(self):
        render(['one'], 15, 261, 174, 2, 1)

        with self.assertRaises(TooManyLabels):
            render(['one', 'two'], 15, 261, 174, 2, 1)
