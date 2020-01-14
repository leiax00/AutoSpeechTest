# coding=utf-8


class AudioObj:
    def __init__(self, aid=None, content=None, source=None):
        self.aid = aid
        self.content = content
        self.source = source

    def __str__(self):
        return self.__dict__.__str__()


if __name__ == '__main__':
    obj = AudioObj('a', 'b', 'c')
    print(obj.__dict__)
    print(obj)
