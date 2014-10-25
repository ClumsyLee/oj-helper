import random
import re

from oj_helper import config, session

__all__ = ['submit']

def submit(problem_id, filename):
    """Submit source code file to lambda OJ
    currently only C & C++ are supported
    """
    language = _judge_language(filename)

    # Get csrt token from server
    csrf_token = _get_csrf_token()
    # Generate random qaptcha key
    qaptcha_key = _generate_key(32)
    # Send qaptcha key to server (simulate dragging)
    _send_qaptcha_key(qaptcha_key)
    # Submit
    _send_form(problem_id, language, filename, csrf_token, qaptcha_key)


def _judge_language(filename):
    dot_pos = filename.rfind('.')
    if dot_pos < 0:  # Not found
        raise ValueError('Failed to judge language from filename: "%s" does '
                         'not have a suffix')
    suffix = filename[dot_pos + 1:]

    if suffix == 'c':  # C
        return 0
    elif suffix in ['cc', 'cpp', 'cxx', 'C', 'c++']:  # C++
        return 1
    else:
        raise ValueError('Unknown suffix: .%s' % suffix)

def _generate_key(length):
    chars = 'azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN_-#@'
    key = ''
    for i in range(length):
        key += random.choice(chars)
    return key

def _get_csrf_token():
    r = session.get(config['submit_url'])
    m = re.search(r'csrf.*value="(.*)"', r.text)
    return m.group(1)

def _send_qaptcha_key(key):
    payload = dict(action='qaptcha', qaptcha_key=key)
    session.post(config['qaptcha_key_url'], data=payload)

def _send_form(problem_id, language, filename, csrf_token, qaptcha_key):
    payload = {'csrf_token': csrf_token,
               'problem_id': problem_id,
               'language': language,
               qaptcha_key: ''}
    files = {'upload_file': open(filename)}
    session.post(config['submit_url'], data=payload, files=files)


if __name__ == '__main__':
    from sys import argv

    if len(argv) != 3:
        print('Usage: %s <problem_id> <filename>' % argv[0])
    else:
        submit(int(argv[1]), argv[2])
