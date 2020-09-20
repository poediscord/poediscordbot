import json
import os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def load_file_as_string(path):
    with open(TEST_DIR + os.sep + path, "r") as file:
        return file.read()


def load_json_file(path):
    return json.loads(load_file_as_string(path))

def get_test_path(file):
    return os.path.join(TEST_DIR, file)