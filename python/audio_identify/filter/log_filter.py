# coding=utf-8


class LogFilter:
    def __init__(self, keywords=None):
        if keywords is None:
            keywords = []
        self.keywords = keywords

    def need_filter(self, str):
        for k in self.keywords:
            if k in str:
                return True
        return False
