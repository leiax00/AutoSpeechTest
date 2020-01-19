# coding=utf-8


class AudioObj:
    def __init__(self, d=None):
        self.aid = ''
        self.content = ''
        self.source = ''
        if d is not None:
            self.__dict__ = d

    def set_v(self, aid=None, content=None, source=None):
        self.aid = aid
        self.content = content
        self.source = source
        return self

    def __str__(self):
        return self.__dict__.__str__()

    def __format__(self, format_spec):
        if format_spec is not None and format_spec != '':
            return format_spec.format(self)
        return self.__str__()


if __name__ == '__main__':
    obj = AudioObj().set_v('a', 'b', 'c')
    print(obj.__dict__)
    print(format(obj))
    print(obj)
