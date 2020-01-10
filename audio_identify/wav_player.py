# coding=utf-8
import random
import wave
from time import sleep

import pyaudio
from pydub import AudioSegment

from audio_identify.asr_queue import aq
from audio_identify.audio_obj import AudioObj
from audio_identify.emit.emiter import observer
from common.time_util import format_time
from conf.config import CorpusConf


class Player:
    def __init__(self):
        self.player = Player._Player()

    def play(self, o):
        if isinstance(o, AudioObj):
            audio_duration = len(AudioSegment.from_wav(o.source)) / 1000
            print('audio_duration:', audio_duration)
            self.player.play_wav(o.source)
        else:
            print('audio source may be error, type:', type(o))
        sleep(CorpusConf.PLAY_SEPARATOR)
        observer.notify()

    def play_batch(self, o_list, max_count=CorpusConf.WAV_COUNT_ONE_CMDER):
        while max_count > 0:
            max_count -= 1
            self.play(o_list[random.randint(0, len(o_list))])

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


player = Player()
if __name__ == '__main__':
    player.play(r'\\192.168.1.8/corpus/train/wavs/A1001/A1001_4244.wav')
    player.play(AudioObj(source=r'\\192.168.1.8/corpus/train/wavs/A1001/A1001_4244.wav'))
