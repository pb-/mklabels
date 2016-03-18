import unittest

from ..main import layout


class MainTestCase(unittest.TestCase):
    def test_layout_normal(self):
        (rows, columns) = layout(297, 210, 15, 56, 13, 2, 1)
        self.assertEqual((rows, columns), (9, 4))
