# coding=utf-8
from time import sleep

from audio_identify.analyzer import Analyzer
from audio_identify.collector import Collector
from audio_identify.wav_player import Player
from common.conf_paser import get_wav_mapping
from common.serial_util import get_com_devices


class AudioIdentify:
    def __init__(self):
        self.player = Player()
        self.com_devices = get_com_devices()
        self.collectors = []
        self.analyzers = []
        self.wav_mapping = get_wav_mapping()

    def register_collector_by_com(self):
        for device in self.com_devices:
            self.register_collector(Collector(device))

    def register_collector(self, c):
        """
        :type c: audio_identify.collector.Collector
        """
        if isinstance(c, Collector):
            c.start()
            self.collectors.append(c)
        else:
            print('invalid collector..., c:', c)

    def remove_collector(self, c):
        """
        :type c: audio_identify.collector.Collector
        """
        if isinstance(c, Collector):
            c.remove()
            self.collectors.remove(c)
        else:
            print('invalid collector..., c:', c)

    def register_analyzer(self, a):
        """
        :type a: audio_identify.collector.Collector
        """
        if isinstance(a, Analyzer):
            a.start()
            self.analyzers.append(a)
        else:
            print('invalid analyzer..., Analyzer:', a)

    def remove_analyzer(self, a):
        """
        :type a: audio_identify.collector.Collector
        """
        if isinstance(a, Analyzer):
            a.remove()
            self.analyzers.remove(a)
        else:
            print('invalid analyzer..., Analyzer:', a)


if __name__ == '__main__':
    ai = AudioIdentify()
    # ai.register_collector(Collector('COM1'))
    ai.register_collector_by_com()
    ai.register_analyzer(Analyzer())
    ai.player.play_batch(ai.wav_mapping.get('打开空调'))
    while True:
        print('running....')
        sleep(10)
