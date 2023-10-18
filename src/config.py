# import os
import yaml
# from dotenv import load_dotenv
from pathlib import Path

CONFIG = yaml.safe_load(Path('config.yml').read_text())

