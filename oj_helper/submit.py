import logging
import random
import re
import time

from oj_helper import config, session, username

__all__ = ['submit', 'SubmitInfo']

logger = logging.getLogger(__name__)

def submit(problem_id, filename):
    """Submit source code file to lambda OJ, return submit info.
    Currently only C & C++ are supported
    """
    language = _judge_language(filename)

    # Get csrt token from server
    csrf_token = _get_csrf_token()
    # Generate random qaptcha key
    qaptcha_key = _generate_key(32)
    # Send qaptcha key to server (simulate dragging)
    _send_qaptcha_key(qaptcha_key)
    # Submit
    info = _send_form(problem_id, language, filename, csrf_token, qaptcha_key)

    return info

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
    logger.debug('qaptcha key posted')

def _send_form(problem_id, language, filename, csrf_token, qaptcha_key):
    payload = {'csrf_token': csrf_token,
               'problem_id': problem_id,
               'language': language,
               qaptcha_key: ''}
    files = {'upload_file': open(filename)}
    r = session.post(config['submit_url'], data=payload, files=files)
    logger.info('Form submitted')

    # Find the latest submit of the user
    m = re.search(r'\b' + username + r'\b', r.text)
    # Find submit number of the next submit
    # Notice that this may fail when the previous submit is the last submit,
    # but this can't happen all the time anyway, sorry for the inconvenience.
    m = re.search(r'<span class="id">\s*(\d+)', r.text[m.end():])
    submit_num = int(m.group(1)) + 1
    logger.debug('Submit number got: %d', submit_num)

    return SubmitInfo(submit_num)


class SubmitInfo(object):
    """Result for a submit"""
    def __init__(self, submit_num):
        super(SubmitInfo, self).__init__()
        self.submit_num = submit_num

        url = config['submit_info_url'] % submit_num
        r = session.get(url)
        # Loop while we should wait
        while '<span class="sub-status-waiting">' in r.text:
            time.sleep(config['retry_interval'])
            r = session.get(url)  # re-get

        logger.debug('Result page got')
        # Set points
        m = re.search(r'<span class="status-\w+">(\d+)</span>', r.text)
        self.points = int(m.group(1))

        # Set samples
        self.samples = []
        self.__set_samples(r.text)

        logger.info('Submit info received')

    def __set_samples(self, text):
        matches = re.finditer(
            r'<td class="id">(\d+)</td>.*?'
            r'<span class="sub-status-\w+">(.*?)</span>.*?'
            r'<td class="time">(?:\s*<span .*?>(\d+)</span>)?.*?'
            r'<td class="memory">(?:\s*<span .*?>(\d+)</span>)?',
            text, flags=re.DOTALL)

        for m in matches:
            if m.group(3) is None:  # No time & memory info
                sample = (int(m.group(1)), m.group(2), None, None)
            else:
                sample = (int(m.group(1)),
                          m.group(2),
                          int(m.group(3)),
                          int(m.group(4)))
            self.samples.append(sample)

        logger.debug('Samples info read')

    def __str__(self):
        s = ('                       Total points: %d\n'
             'Sample           Status             Time      Memory\n'
             % self.points)

        for sample in self.samples:
            if sample[2] is not None:
                time_str = str(sample[2]) + ' ms'
                memory_str = str(sample[3]) + ' KiB'
            else:
                time_str = '    -   '
                memory_str = '     -    '

            s += '%4d   %s %8s %12s\n' % (sample[0],
                                          sample[1].center(26),
                                          time_str,
                                          memory_str)
        return s

if __name__ == '__main__':
    from sys import argv

    if len(argv) != 3:
        print('Usage: %s <problem_id> <filename>' % argv[0])
    else:
        print(submit(int(argv[1]), argv[2]))
