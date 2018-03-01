import defusedxml
from defusedxml import ElementTree


def generate_output(pob_xml: ElementTree):
    print(ElementTree.tostring(pob_xml))

    return None
