oj-helper
=========

Make it more easy to use LambdaOJ: http://lambda.cool/oj

## Motivation
**Submiting on LambdaOJ is really a painful experience.**

## Usage
under folder oj-helper, type

    $ python -m oj_helper.submit <problem_id> <code_file> [stay]

`stay` means not to quit after submit & be ready to submit again

e.g., use

    $ python -m oj_helper.submit 4 lab4.c

to submit lab4.c to problem 4. The output may look like this:

                           Total points: 100
    Sample           Status             Time      Memory
       1            Accepted              0 ms      556 KiB
       2            Accepted              0 ms      560 KiB
       3            Accepted              0 ms      556 KiB
       4            Accepted              0 ms      556 KiB
       5            Accepted              0 ms      560 KiB
       6            Accepted              0 ms      560 KiB
       7            Accepted              0 ms      560 KiB
       8            Accepted             20 ms      556 KiB
       9            Accepted             84 ms      560 KiB
      10            Accepted            436 ms      556 KiB

## Dependence
### Install python

https://www.python.org/downloads/

### Install pip
Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

Then run the following (which may require administrator access):

    python get-pip.py

### Install Requests

    $ pip install requests
