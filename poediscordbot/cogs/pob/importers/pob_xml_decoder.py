import base64
import re
import zlib

import defusedxml.ElementTree as ET

from poediscordbot.util.logging import log


def decode_base64_and_inflate(b64string):
    try:
        decoded_data = base64.b64decode(b64string)
        return zlib.decompress(decoded_data)
    except zlib.error as err:
        log.error(f"ZLib Error in paste: err={err}. Data={b64string}")
    except ValueError as err:
        log.error(f"Value Error in paste: err={err}")


def xml_byte_to_str(xml_bytes: bytes, encoding) -> str:
    xml_str = xml_bytes.decode(encoding)
    pattern = r'<Input name="customMods" string="(.*?)"\/>'
    match = re.search(pattern, xml_str, re.DOTALL)
    if match:
        original_string = match.group(1)
        # reduce newline+ to a single newline
        modified_string = re.sub(r'\n+', '\n',original_string)
        # newline is not valid in attribute, replace with xml newline escape: https://stackoverflow.com/a/2012277
        modified_string = modified_string.strip().replace('\n', '&#10;')
        subst = f"<Input name=\"customMods\" string=\"{modified_string}\" />"

        return re.sub(pattern, subst, xml_str, 1, re.DOTALL)


def decode_to_xml(enc, encoding='windows-1252'):
    enc = enc.replace("-", "+").replace("_", "/")
    xml_bytes = decode_base64_and_inflate(enc)
    xml_str = xml_byte_to_str(xml_bytes, encoding)
    log.debug(f"XML={xml_str}")
    xml = None
    try:
        xml = ET.fromstring(xml_str)
    except TypeError as err:
        log.debug(f"Could not parse the pastebin as xml msg={err}")

    return xml
