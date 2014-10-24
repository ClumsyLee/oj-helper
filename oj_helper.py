import random
import re
import requests

__all__ = ['submit', 'submit_url', 'qaptcha_key_url']

submit_url = 'http://lambda.cool/oj/submit'
qaptcha_key_url = 'http://lambda.cool/oj/qaptcha/key'
cookies = {'remember_token': ''}  # Find it in your browser

def submit(problem_id, filename):
    """Submit source code file to lambda OJ
    currently language can be 'C' or 'C++'

    """
    language = _judge_language(filename)

    s = requests.Session()
    # Get csrt token from server
    csrf_token = _get_csrf_token(s)
    # Generate random qaptcha key
    qaptcha_key = _generate_key(32)
    # Send qaptcha key to server (simulate dragging)
    _send_qaptcha_key(s, qaptcha_key)
    # Submit
    _send_form(s, problem_id, language, filename, csrf_token, qaptcha_key)


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

def _get_csrf_token(session):
    r = session.get(submit_url, cookies=cookies)
    m = re.search(r'csrf.*value="(.*)"', r.text)
    return m.group(1)

def _send_qaptcha_key(session, key):
    payload = dict(action='qaptcha', qaptcha_key=key)
    session.post(qaptcha_key_url, data=payload)

def _send_form(session, problem_id, language, filename, csrf_token, qaptcha_key):
    payload = {'csrf_token': csrf_token,
               'problem_id': problem_id,
               'language': language,
               qaptcha_key: ''}
    files = {'upload_file': open(filename)}
    session.post(submit_url, data=payload, files=files)


if __name__ == '__main__':
    from sys import argv

    if len(argv) != 3:
        print('Usage: %s <problem_id> <filename>' % argv[0])
    else:
        submit(int(argv[1]), argv[2])
