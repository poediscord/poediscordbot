from defusedxml import ElementTree
from marshmallow import Schema, fields, pprint


def generate_output(pob_xml: ElementTree):
    print(ElementTree.tostring(pob_xml))

    return None
