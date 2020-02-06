# coding=utf-8
import threading
from abc import abstractmethod, ABCMeta


class Receiver(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()
        observer.register(self)

    @abstractmethod
    def on_notify(self, *o):
        raise NotImplementedError

    @abstractmethod
    def notify_start(self, *o):
        raise NotImplementedError

    @abstractmethod
    def notify_end(self, *o):
        raise NotImplementedError


class Observer:
    def __init__(self):
        self.receivers = []

    def register(self, o):
        if issubclass(type(o), Receiver):
            self.receivers.append(o)
        else:
            raise TypeError

    def remove(self, o):
        if issubclass(type(o), Receiver):
            self.receivers.remove(o)

    def on_notify(self, *o):
        for receiver in self.receivers:
            receiver.on_notify(*o)

    def notify_start(self, *o):
        for receiver in self.receivers:
            receiver.notify_start(*o)

    def notify_end(self, *o):
        for receiver in self.receivers:
            receiver.notify_end(*o)


observer = Observer()
if __name__ == '__main__':
    class As(Receiver):
        def __init__(self):
            print('aaa')
            super().__init__()
            print('aaa11')

        def on_notify(self):
            print('aaaaa')


    observer.register(As())
    observer.on_notify()
