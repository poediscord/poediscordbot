# http://poeurl.com/api/?shrink={%22url%22:%22https://www.pathofexile.com/passive-skill-tree/AAAABAMBAHpwm6FR-zeDAx7quvfX0PW2-o5kpys3ZsMJ62PviLmT8h3v66EvGyUfQR1PDkiMNkuutUjbXq6zBUJJUZEHQnrsGNfPlS6-iocTf8ZFfjQKDXxfalgHj0ZwUvrSjun3wVF0b57G93gvOw3B86aZES-TJx0UzRYBb9-K0NBGcRhq8NUXL21sgKSQ1hV-D8QsnL46lSCDCYnTdwcOXL6Au_wtH0yzLL9JsUGWtAycpI_6NbmsmMEAsZC4yqKjXGuEb6brV8kRD9lb96YRUOv1VdYrCsNtUDAfGIt6avp88JJ0ZOf5N9AfhEjndG0ZO3zpAioLBx4spl3yfOXK0-L3EZbUQvVLLag=%22}
import json
import urllib.request

from poediscordbot.util.logging import log


def shrink_tree_url(tree):
    """
    Shrink url with poeurl
    :param tree:
    :return: valid poeurl if possible else raise a value error
    """
    # sanitize
    tree = tree.strip()

    # build requesturl
    param = f'{{"url":"{tree}"}}'
    url = f'http://poeurl.com/api/?shrink={param}'
    log.debug(f"Poeurl payload={url}")

    contents = urllib.request.urlopen(url).read().decode('utf-8')
    log.debug(f"Poeurl contents={contents}")

    contents = json.loads(contents)
    log.debug(f"Got json content from poeurl ... {contents}")
    if contents['url']:
        return f"http://poeurl.com/{contents['url']}"
    else:
        raise ValueError("Unable to retrieve URL")
