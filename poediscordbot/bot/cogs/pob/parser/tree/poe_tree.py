class PoeTree:
    def __init__(self, version, character, ascendancy, full_screen, nodes, payload):
        """
        Construct a wrapper object for poe tree data
        :param version: version
        :param character: character in the tree
        :param ascendancy: ascendancy of the char
        :param full_screen: was the tree used in fullscreen
        :param nodes: list of nodes
        :param payload: original tree payload
        """
        self.version = version
        self.character = character
        self.ascendancy = ascendancy
        self.full_screen = full_screen
        self.nodes = nodes
        self.payload = payload

    def get_keystones(self, keystones: dict) -> list:
        """
        From a nodelist, obtain a list of picked keystones
        :param node_list: last param in the tuple of the decode_url func
        :return: list of textual representation of keystones
        """
        contained_keystone = [keystones.get(node) for node in self.nodes if node in keystones]
        return contained_keystone
