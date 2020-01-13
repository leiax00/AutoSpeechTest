# coding=utf-8
from conf.config import CorpusConf


class LogFilter:
    def __init__(self):
        self.keywords = CorpusConf.LOG_FILTER

    def need_filter(self, str):
        for k in self.keywords:
            if k in str:
                return True
        return False


log_filter = LogFilter()
