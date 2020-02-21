# coding=utf-8
import os
import shutil
import traceback
import wave
from time import sleep

import pyaudio
import sox
from pydub import AudioSegment

from audio_identify.emit.emiter import observer
from common.logger import logger
from conf.config import corpus_conf
from obj.audio_obj import AudioObj


class Player:
    def __init__(self):
        self.player = Player._Player()
        self.count = 0
        self.__is_play = True

    def play(self, o, cmd_str=''):
        while not self.__is_play:
            pass

        logger.info('play cmd:{0}, and wav:{1}'.format(cmd_str, o))
        if isinstance(o, AudioObj):
            audio_duration = len(AudioSegment.from_wav(o.source)) / 1000
            self.player.play_wav(o.source, corpus_conf.amplify_volume)
            logger.info('start to collect log and audio_duration:{0}'.format(audio_duration))
            sleep(corpus_conf.play_separator)
            observer.notify_end(o)
            logger.info('play cmd:{0} finish...'.format(cmd_str))
        else:
            logger.info('audio source may be error, type:{0}'.format(type(o)))

    def play_batch_mode1(self, o_list, cmd_str='', repeat_play_count=corpus_conf.repeat_play_count):
        while repeat_play_count > 0:
            for o in o_list:
                self.play(o, cmd_str)
            repeat_play_count -= 1

    def play_batch_mode2(self, o_list, cmd_str='', repeat_play_count=corpus_conf.repeat_play_count):
        for o in o_list:
            count = repeat_play_count
            while count > 0:
                self.play(o, cmd_str)
                count -= 1

    def play_batch(self, o_list, cmd_str='', repeat_play_count=corpus_conf.repeat_play_count):
        if corpus_conf.play_mode == 1:
            self.play_batch_mode1(o_list, cmd_str, repeat_play_count)
        elif corpus_conf.play_mode == 2:
            self.play_batch_mode2(o_list, cmd_str, repeat_play_count)
        elif corpus_conf.play_mode == 3:
            self.play_batch_mode1(o_list, cmd_str, repeat_play_count)  # repeat_play_count === 1

    def play_all(self, o_dict, repeat_play_count):
        """
        :type o_dict: dict
        :param o_dict: 命令词：音频列表
        :param repeat_play_count: 单条命令重复次数（每次的音频不一样，内容一样）
        :return:
        """
        wake_wav = ''
        if corpus_conf.first_read is not None and corpus_conf.first_read != '':
            try:
                wake_wav = o_dict.pop(corpus_conf.first_read)
                self.play_batch(wake_wav, corpus_conf.first_read, repeat_play_count)
            except KeyError:
                pass

        for cmd_str, wav_list in o_dict.items():
            self.play_batch(wav_list, cmd_str, repeat_play_count)

        if wake_wav != '':
            o_dict[corpus_conf.first_read] = wake_wav

    class _Player:
        def __init__(self):
            self.transformer = sox.Transformer()

        def play_wav(self, wav_name, need_voice_same=False):
            if need_voice_same:
                tmp_file_path = self.deal_voice(wav_name)
            else:
                tmp_file_path = shutil.copy(wav_name, corpus_conf.temp_path)
            chunk = 1024
            p = pyaudio.PyAudio()
            wf = wave.open(tmp_file_path, 'rb')
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            data = wf.readframes(chunk)
            while data != b'':
                stream.write(data)
                data = wf.readframes(chunk)

            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()
            os.remove(tmp_file_path)

        def deal_voice(self, filename):
            dst_f = os.path.join(corpus_conf.temp_path, os.path.basename(filename))
            try:
                v_adjustment = float(self.transformer.stat(filename).get('Volume adjustment')) or 1.0
                logger.info('voice increment:{0}, wav_path:{1}'.format(v_adjustment, filename))
                self.transformer.vol(v_adjustment)
                self.transformer.build(filename, dst_f)
                self.transformer.clear_effects()
                return dst_f
            except Exception as e:
                logger.warn('Failed to adjust volume, use origin wav. err: {0}, {1}'.format(e, traceback.format_exc()))
                if os.path.exists(dst_f):
                    os.remove(dst_f)
                return shutil.copy(filename, corpus_conf.temp_path)

    def set_play(self, bol):
        self.__is_play = bool(bol)

    def is_play(self):
        return self.__is_play


player = Player()
if __name__ == '__main__':
    # player.play(r'\\192.168.1.8/corpus/train/wavs/A1001/A1001_4244.wav')
    # player.play(AudioObj({'source': r'\\192.168.1.8/corpus/train/wavs/A1001/A1001_4244.wav'}))
    asd = {'a': 'a1', 'b': 'b1'}
    print(asd.pop('a'))
    try:
        print(asd.pop('c'))
    except KeyError:
        pass
    print(asd)
