# coding=utf-8
from abc import abstractmethod, ABCMeta


class Receiver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_notify(self):
        raise NotImplementedError


class Observer:
    def __init__(self):
        self.receivers = []

    def register(self, o):
        if issubclass(type(o), Receiver):
            self.receivers.append(o)
        else:
            raise TypeError

    def notify(self):
        for receiver in self.receivers:
            receiver.on_notify()


observer = Observer()
if __name__ == '__main__':
    class As(Receiver):
        def on_notify(self):
            print('aaaaa')
    observer.register(As())
    observer.notify()
