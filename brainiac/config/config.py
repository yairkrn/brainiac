import pathlib
import sys

import yaml
from ..utils import logger

CONFIG_FILE_NAME = 'config.yaml'

try:
    with open(pathlib.Path(__file__).parent / CONFIG_FILE_NAME, 'r') as stream:
        config = yaml.safe_load(stream)
except Exception as exc:
    logger.exception(f"unable to parse config file {CONFIG_FILE_NAME}", exc_info=False)
    sys.exit(-1)
