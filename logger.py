import logging
from logging.handlers import RotatingFileHandler


class LoggerBlacklist(logging.Filter):
    def __init__(self, *name_list):
        self.__name_list = [logging.Filter(name) for name in name_list]

    def filter(self, record):
        return any(not f.filter(record) for f in self.__name_list)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

fh = RotatingFileHandler('telbot.log', maxBytes=2 ** 20, backupCount=21, encoding="utf-8")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(name)-16s %(levelname)-8s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger_filter = LoggerBlacklist("telegram")

fh.addFilter(logger_filter)
ch.addFilter(logger_filter)

logger.addHandler(fh)
logger.addHandler(ch)
