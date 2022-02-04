import base64
import json
import struct

from instance import config

from .poe_tree import PoeTree


class PoeTreeCodec:
    POE_TREE_JSON = 'resources/tree_3_17.json'

    def __init__(self):
        tree_data = json.load(open(config.ROOT_DIR + '/' + PoeTreeCodec.POE_TREE_JSON))
        node_data = tree_data['nodes']

        # construct a dict containing the id of the node as key and the required attribs as value dict
        # {<id>:{name:<n>,abbrev:<abbrev>}} - {14914: {'name': 'Phase Acrobatics', 'abbrev': 'PA'}}
        self.keystones = {
            node_data[node]['skill']:
                {'name': node_data[node]['name'], 'abbrev': self.extract_abbrev(node_data[node]['name'])}
            for node in node_data if 'isKeystone' in node_data[node]}

    @staticmethod
    def encode_hashes(tree: PoeTree) -> str:
        """
        Creates a valid poe skilltree url payload
        :param tree: class holding all tree infos such as version char ascendancy and tree
        :return:
        """
        # [ver,charclass,asc,[4byte ints]]
        bytes = bytearray(struct.pack('>ibbb', tree.version, tree.character, tree.ascendancy, tree.full_screen))
        for node in tree.nodes:
            for byte in struct.pack('>H', node):
                bytes.append(byte)
        return base64.urlsafe_b64encode(bytes).decode("utf-8")

    @staticmethod
    def decode_url(payload: str) -> PoeTree:
        """
        Decodes a poe skilltree url to a tuple
        :param payload: string after the last slash or complete url.
        :return: tuple that contains version, char, ascendency, fullscreen, nodes[]
        """

        if payload.strip().startswith("https"):
            payload = payload[(payload.rindex('/') + 1):]

        bytes = base64.urlsafe_b64decode(payload)
        # bytes 0-3 contain the version
        ver = struct.unpack(">i", bytes[0:4])[0]
        # bytes4-6 contain the class, ascendency and fullscreen status
        char, ascendency, fullscreen = struct.unpack("bbb", bytes[4:7])
        start = 7
        offset = 2
        # rest of the bytes contain the hashes
        nodes = []
        for count in range(start, len(bytes), 2):
            nodes.append(struct.unpack(">H", bytes[count:count + offset])[0])
        return PoeTree(ver, char, ascendency, fullscreen, nodes, payload)

    @staticmethod
    def extract_abbrev(node_dn):
        return ''.join([x[0] for x in node_dn.split()])


codec = PoeTreeCodec()
