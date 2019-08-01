# -*- coding: utf-8 -*-
import logging
import sys
import unittest

from poediscordbot.pob_xml_parser.tree.poe_tree import PoeTree
from poediscordbot.pob_xml_parser.tree.poe_tree_codec import codec

payload = 'AAAABAMDAQQHBLMGSQj0Dc0OPA5cES0UIBRxFScWbxhWGF0YkRo4HM4c3CSqJy8o-itQLJwy0TWSNuk6UjpYOuE8LUGHRARFR0V-RZ1Ms025TeNQR' \
          '1NSVcZZ81qRXz9mnmebaGVodGpDaqxq-mvbcg9yqXasfIN99YIHgseDX4PMg9uFYIhAjLGOvo8akDOQVZLBmK2a4JuKogCmV6asqH2qxKyYrKqtja' \
          '3xrj6vp7c-uJO8n7zqvk_AZsT2xq7MvM9-0B_Tj9P72L3ZXtl82mLfsONq5FHqGOvu7IPsiu8O7-vwH_JF8933MvfX-Ov56PrS_Ev-Cv5U_oH-jw=='
decoded = (4, 3, 3, 1, [1031, 1203, 1609, 2292, 3533, 3644, 3676, 4397, 5152, 5233, 5415, 5743, 6230, 6237, 6289,
                        6712,
                        7374, 7388, 9386, 10031, 10490, 11088, 11420, 13009, 13714, 14057, 14930, 14936, 15073,
                        15405,
                        16775, 17412, 17735, 17790, 17821, 19635, 19897, 19939, 20551, 21330, 21958, 23027, 23185,
                        24383,
                        26270, 26523, 26725, 26740, 27203, 27308, 27386, 27611, 29199, 29353, 30380, 31875, 32245,
                        33287,
                        33479, 33631, 33740, 33755, 34144, 34880, 36017, 36542, 36634, 36915, 36949, 37569, 39085,
                        39648,
                        39818, 41472, 42583, 42668, 43133, 43716, 44184, 44202, 44429, 44529, 44606, 44967, 46910,
                        47251,
                        48287, 48362, 48719, 49254, 50422, 50862, 52412, 53118, 53279, 54159, 54267, 55485, 55646,
                        55676,
                        55906, 57264, 58218, 58449, 59928, 60398, 60547, 60554, 61198, 61419, 61471, 62021, 62429,
                        63282,
                        63447, 63723, 63976, 64210, 64587, 65034, 65108, 65153, 65167])
tree = PoeTree(decoded[0], decoded[1], decoded[2], decoded[3], decoded[4], payload)

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_encode(self):
        result = codec.encode_hashes(tree)
        print(result)
        print(payload)
        self.assertEqual(result, payload)

    def test_decode(self):
        result = codec.decode_url(payload)
        self.assertEqual(tree.version, result.version)
        self.assertEqual(tree.payload, result.payload)
        self.assertEqual(tree.full_screen, result.full_screen)
        self.assertEqual(tree.ascendancy, result.ascendancy)
        self.assertEqual(tree.character, result.character)
        self.assertEqual(tree.nodes, result.nodes)

    def test_keystones(self):
        self.assertTrue(len(codec.keystones) > 0)
        keystones = tree.get_keystones(codec.keystones)
        self.assertTrue(1, len(keystones))
        self.assertTrue(keystones[0]['name'] == "Elemental Equilibrium")


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.level = logging.DEBUG
    stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)
    unittest.main()
