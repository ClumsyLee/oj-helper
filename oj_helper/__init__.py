import json
import logging
import re
import requests

__all__ = ['config', 'session', 'submit', 'SubmitInfo', 'username']

logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
config = json.load(open('config.json'))
logger.info('Configuration loaded')

# Create session
session = requests.Session()
_r = session.get(config['profile_url'], cookies=config['cookies'])
logger.info('Profile page got')

_m = re.search(r'<h2>(\w+)\b', _r.text)
username = _m.group(1)
logger.info('User name read: %s', username)

from .submit import submit, SubmitInfo
