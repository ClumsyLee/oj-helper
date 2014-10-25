import json
import re
import requests

__all__ = ['config', 'session', 'submit', 'SubmitInfo', 'username']

# Import config
config = json.load(open('config.json'))

# Create session
session = requests.Session()
_r = session.get(config['profile_url'], cookies=config['cookies'])
_m = re.search(r'<h2>(\w+)\b', _r.text)
username = _m.group(1)

from .submit import submit, SubmitInfo
