import sys
from datetime import datetime


def printLog(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sys.stdout.write(f"{now} - {msg}\n")
