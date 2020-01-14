# coding=utf-8
import wave
from time import sleep

import pyaudio
from pydub import AudioSegment

from obj.audio_obj import AudioObj
from audio_identify.emit.emiter import observer
from conf.config import CorpusConf


class Player:
    def __init__(self):
        self.player = Player._Player()
        self.__is_play = True

    def play(self, o, cmd_str=''):
        while not self.__is_play:
            pass

        print('play cmd:{0}, and wav:{1}'.format(cmd_str, o))
        if isinstance(o, AudioObj):
            audio_duration = len(AudioSegment.from_wav(o.source)) / 1000
            print('audio_duration:', audio_duration)
            self.player.play_wav(o.source)
        else:
            print('audio source may be error, type:', type(o))
        sleep(CorpusConf.PLAY_SEPARATOR)
        observer.notify(o)

    def play_batch(self, o_list, cmd_str='', repeat_play_count=CorpusConf.REPEAT_PLAY_COUNT):
        while repeat_play_count > 0:
            for o in o_list:
                self.play(o, cmd_str)
            repeat_play_count -= 1

    def play_all(self, o_dict, repeat_play_count=CorpusConf.REPEAT_PLAY_COUNT):
        """
        :type o_dict: dict
        :param o_dict: 命令词：音频列表
        :param repeat_play_count: 单条命令重复次数（每次的音频不一样，内容一样）
        :return:
        """
        for cmd_str, wav_list in o_dict.items():
            self.play_batch(wav_list, cmd_str, repeat_play_count)

    class _Player:
        @staticmethod
        def play_wav(wav_name):
            wf = wave.open(wav_name, 'rb')
            max_len = 1024
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            data = wf.readframes(max_len)
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(max_len)

            stream.stop_stream()
            stream.close()
            p.terminate()

    def set_play(self, bol):
        self.__is_play = bool(bol)

    def is_play(self):
        return self.__is_play


player = Player()
if __name__ == '__main__':
    player.play(r'\\192.168.1.8/corpus/train/wavs/A1001/A1001_4244.wav')
    player.play(AudioObj(source=r'\\192.168.1.8/corpus/train/wavs/A1001/A1001_4244.wav'))
