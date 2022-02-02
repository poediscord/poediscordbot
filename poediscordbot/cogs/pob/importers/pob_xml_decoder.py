import base64
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


def decode_to_xml(enc, encoding='windows-1252'):
    enc = enc.replace("-", "+").replace("_", "/")
    xml_str = decode_base64_and_inflate(enc)
    log.debug(f"XML={xml_str}")
    xml = None
    try:
        xml = ET.fromstring(xml_str.decode(encoding))
    except TypeError as err:
        log.debug(f"Could not parse the pastebin as xml msg={err}")

    return xml