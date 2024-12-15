from logging.config import dictConfig
from pathlib import Path

import yaml

logging_yaml_config = Path(__file__).parent / 'logging.config.yaml'

# Load the config file
with open(logging_yaml_config, 'rt') as f:
    dictConfig(yaml.safe_load(f.read()))

