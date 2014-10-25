import json
import requests

__all__ = ['config', 'session', 'submit']

# Import config
config = json.load(open('config.json'))

# Create session
session = requests.Session()
_r = session.get(config['index_url'], cookies=config['cookies'])
_r.raise_for_status()

from .submit import submit
