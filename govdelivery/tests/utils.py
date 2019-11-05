import codecs
from os import path


testdata_dir = path.join(path.dirname(__file__), 'test_api_responses')


def load_data(filename):
    full_path = path.join(testdata_dir, filename)
    f = codecs.open(full_path, encoding="utf8")
    return f.read()
