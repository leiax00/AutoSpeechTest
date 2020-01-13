# coding=utf-8


class AudioObj:
    def __init__(self, aid=None, content=None, source=None):
        self.aid = aid
        self.content = content
        self.source = source


if __name__ == '__main__':
    print(AudioObj().content)
