import base64
from io import BytesIO

import struct


def encode_hashes(version: int, starting_class: int, ascendency: int, fullscreen: int, hashes: list) -> str:
    """
    Creates a valid poe skilltree url payload
    :param version:
    :param starting_class:
    :param ascendency:
    :param fullscreen:
    :param hashes:
    :return:
    """
    # [ver,charclass,asc,[4byte ints]]
    bytes = bytearray(struct.pack('>ibbb', version, starting_class, ascendency, fullscreen))
    for tmpHash in hashes:
        for byte in struct.pack('>H', tmpHash):
            bytes.append(byte)
    return base64.urlsafe_b64encode(bytes).decode("utf-8")


def decode_url(payload: str) -> tuple:
    """
    Decodes a poe skilltree url to a tuple
    :param payload: string after the last slash or complete url.
    :return: tuple that contains version, char, ascendency, fullscreen, nodes[]
    """

    if payload.strip().startswith("https"):
        payload = payload[(payload.rindex('/') + 1):]

    print(">>>" + payload)
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
    return ver, char, ascendency, fullscreen, nodes


def decode_keystones(node_list: list) -> list:
    """
    From a nodelist, obtain a list of picked keystones
    :param node_list: last param in the tuple of the decode_url func
    :return: list of textual representation of nodes.
    """
    keystones = {41970: {'name': 'Ancestral Bond', 'abbrev': 'AB'},
                 54307: {'name': 'Acrobatics', 'abbrev': 'Acro'},
                 42178: {'name': 'Point Blank', 'abbrev': 'PB'},
                 14914: {'name': 'Phase Acrobatics', 'abbrev': 'Phase Acro'},
                 22088: {'name': 'Elemental Overload', 'abbrev': 'EO'},
                 40907: {'name': 'Unwavering Stance'},
                 10808: {'name': 'Vaal Pact', 'abbrev': 'VP'},
                 18663: {'name': 'Minion Instability', 'abbrev': 'MI'},
                 24426: {'name': 'Ghost Reaver', 'abbrev': 'GR'},
                 23407: {'name': 'Perfect Agony', 'abbrev': 'PA'},
                 39085: {'name': 'Elemental Equilibrium', 'abbrev': 'EE'},
                 54922: {'name': 'Arrow Dancing', 'abbrev': 'AD'},
                 56075: {'name': 'Eldritch Battery', 'abbrev': 'EB'},
                 12926: {'name': 'Iron Grip', 'abbrev': 'IG'},
                 23540: {'name': 'Conduit'},
                 45175: {'name': 'Necromantic Aegis', 'abbrev': 'NA'},
                 10661: {'name': 'Iron Reflexes', 'abbrev': 'IR'},
                 44941: {'name': 'Avatar of Fire', 'abbrev': 'AoF'},
                 31703: {'name': 'Pain Attunement', 'abbrev': 'PA'},
                 31961: {'name': 'Resolute Technique', 'abbrev': 'RT'},
                 11455: {'name': 'Chaos Inoculation', 'abbrev': 'CI'},
                 57279: {'name': 'Blood Magic', 'abbrev': 'BM'},
                 34098: {'name': 'Mind Over Matter', 'abbrev': 'MoM'},
                 63425: {'name': "Zealot's Oath", 'abbrev': 'ZO'},
                 17818: {'name': 'Crimson Dance', 'abbrev': 'CD'},
                 42343: {'name': 'Runebinder', 'abbrev': 'RB'}}
    contained_keystone = [keystones.get(node) for node in node_list if node in keystones]
    return contained_keystone
