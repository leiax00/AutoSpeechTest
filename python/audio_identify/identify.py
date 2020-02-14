# coding=utf-8
import codecs
import json
import os
from threading import Thread

from audio_identify.analyzer import Analyzer
from audio_identify.collector import Collector
from audio_identify.emit.emiter import observer
from audio_identify.wav_player import Player
from common.logger import logger
from common.path_helper import get_wav_path
from common.serial_util import get_com_devices
from common.time_util import format_time
from conf.config import corpus_conf
from conf.load_source import LoadSource
from obj.default_json_decoder import DefaultDecoder
from obj.default_log_obj import write_default_log_2_csv


class AudioIdentify:
    def __init__(self):
        self.player = Player()
        self.com_devices = get_com_devices()
        self.collectors = []
        self.analyzers = []
        self.wav_mapping = {}
        self.w_thread = None
        self.can_write = True
        self.__init_default()

    def __init_default(self):
        self.register_collector_by_com()
        self.register_analyzer(Analyzer())
        self.start_write_result_thread()

    def start_write_result_thread(self, f=write_default_log_2_csv):
        self.w_thread = Thread(target=f, args=(self,))  # 写线程不能启动为精灵线程
        self.w_thread.start()

    def register_collector(self, c):
        """
        :type c: audio_identify.collector.Collector
        """
        if isinstance(c, Collector):
            # c.start()  # 播放与采集同线程时，不启动
            self.collectors.append(c)
        else:
            logger.warn('invalid collector..., c:{0}'.format(c))

    def remove_collector(self, c):
        """
        :type c: audio_identify.collector.Collector
        """
        if isinstance(c, Collector):
            c.remove()
            observer.remove(c)
            self.collectors.remove(c)
        else:
            logger.warn('invalid collector..., c:{0}'.format(c))

    def register_collector_by_com(self):
        for device in self.com_devices:
            self.register_collector(Collector(device))

    def replace_collectors_by_com(self, com_l):
        """
        修改串口后，更新设置日志收集器
        :param com_l: 新的串口列表
        """
        start_coms = [c.com_device for c in self.collectors]
        start_collectors = {c.com_device: c for c in self.collectors}
        for com in com_l:
            if com not in start_coms:
                self.register_collector(Collector(com))
            else:
                start_coms.remove(com)
        # 移除未选中的串口
        for com in start_coms:
            self.remove_collector(start_collectors.get(com))

    def register_analyzer(self, a):
        """
        :type a: audio_identify.collector.Analyzer
        """
        if isinstance(a, Analyzer):
            a.start()
            self.analyzers.append(a)
        else:
            logger.warn('invalid analyzer..., Analyzer::{0}'.format(a))

    def remove_analyzer(self, a):
        """
        :type a: audio_identify.collector.Analyzer
        """
        if isinstance(a, Analyzer):
            a.remove()
            self.analyzers.remove(a)
        else:
            logger.warn('invalid analyzer..., Analyzer::{0}'.format(a))

    def release(self):
        for collector in self.collectors:
            collector.remove()
        for analyzer in self.analyzers:
            analyzer.remove()
        self.player.set_play(False)
        self.can_write = False

    def process(self):
        try:
            if corpus_conf.play_mode == 3:
                count = corpus_conf.repeat_play_count
                while count > 0:
                    count -= 1
                    self.player.play_all(self.wav_mapping, 1)
            else:
                self.player.play_all(self.wav_mapping, corpus_conf.repeat_play_count)
        except Exception as e:
            logger.error('error happen: %s' % e)

    def output_wav_text(self):
        new_wav_mapping = LoadSource().parse_wav(get_wav_path(), corpus_conf.wav_count_one_cmder)
        for k, v in new_wav_mapping.items():
            old_v = self.wav_mapping.get(k)
            if old_v is not None:
                if len(old_v) >= corpus_conf.wav_count_one_cmder:
                    new_wav_mapping[k] = old_v[:corpus_conf.wav_count_one_cmder]
                else:
                    new_wav_mapping[k] = old_v + v[:(corpus_conf.wav_count_one_cmder - len(old_v))]
        self.wav_mapping = new_wav_mapping
        file_name = '{0}_{1}_{2}.json'.format(corpus_conf.product, format_time(time_formatter="%y%m%d"),
                                              corpus_conf.wav_count_one_cmder)
        with codecs.open(os.path.join(corpus_conf.output_path, file_name), 'w+', encoding='utf-8') as wf:
            json.dump(self.wav_mapping, wf, cls=DefaultDecoder, indent=4, ensure_ascii=False)
        logger.info('export end, file name:{0}'.format(file_name))


if __name__ == '__main__':
    wav_path = r'D:\code\myTools\python\lehua_matong_tts_10.json'
    corpus_conf.load_conf()
    ai = AudioIdentify()
    ai.wav_mapping = LoadSource().parse_wav(wav_path, corpus_conf.wav_count_one_cmder)
    ai.process()
