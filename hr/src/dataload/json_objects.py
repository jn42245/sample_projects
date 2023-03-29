import json


def load_json(path: str, mode: str):
    with open(path, mode) as f:
        x = json.load(f)
    return x
