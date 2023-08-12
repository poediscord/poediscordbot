import unittest

from poediscordbot.util import shorten_number_string


class UtilTest(unittest.TestCase):

    def test_no_decimals(self):
        out = shorten_number_string(1550)
        self.assertEqual("2K", out)
        out = shorten_number_string(1550, 0)
        self.assertEqual("2K", out)
        out = shorten_number_string(1550, 1)
        self.assertEqual("1.6K", out)
        out = shorten_number_string(1550, 2)
        self.assertEqual("1.55K", out)
        out = shorten_number_string(1550, 3)
        self.assertEqual("1.550K", out)
        out = shorten_number_string(1550, 4)
        self.assertEqual("1.5500K", out)
