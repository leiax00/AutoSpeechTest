# coding=utf-8
import queue


class AsrQueue(queue.Queue):
    def send(self, o):
        self.put(o)

    def pop(self):
        if not self.empty():
            return self.get()

    def size(self):
        return self.qsize()


aq = AsrQueue()
