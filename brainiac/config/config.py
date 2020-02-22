import pathlib

import yaml

CONFIG_FILE = pathlib.Path(__file__).parent / 'config.yaml'

with open(CONFIG_FILE, 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        config = {}
