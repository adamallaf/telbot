from logging import getLogger


__token = None
__logger = getLogger("utils")


def readToken():
    global __token
    try:
        with open('token', 'r') as f:
            __token = f.readline().replace('\n', '')
        __logger.info("Token read successfully")
        status = True
    except FileNotFoundError:
        __logger.error("Couldn\'t read token!")
        status = False
    return status


def getToken():
    return __token
