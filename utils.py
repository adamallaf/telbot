import sys


__token = None


def readToken():
    global __token
    try:
        with open('token', 'r') as f:
            __token = f.readline().replace('\n', '')
        status = True
    except FileNotFoundError:
        sys.stderr.write("Can\'t load token!")
        status = False
    return status


def getToken():
    return __token
