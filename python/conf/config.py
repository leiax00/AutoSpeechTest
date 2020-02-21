# coding=utf-8
import os

import yaml

from audio_identify.filter.log_filter import LogFilter
from common.time_util import format_time, format_2


class CorpusConf:
    def __init__(self):
        # 无上限为max, 无下限为min
        self.svm_list = []
        self.likelihood_list = []
        self.confidence_list = []
        self.remote_host = r''
        self.remote_port = 22
        self.remote_username = ''
        self.remote_password = ''

        self.remote_base = r''
        self.remote_result_dir = r''
        self.cmd_path = r''

        self.wav_path = r''
        self.wav_schema = []
        self.wav_load_mode = 1
        self.retrieve_script = ''

        self.wav_count_one_cmder = 1
        self.play_mode = 1
        self.repeat_play_count = 1
        self.amplify_volume = True
        self.play_separator = 2  # 语音播报间隔
        self.first_read = ''

        self.log_filter = LogFilter()  # 过滤掉包含关键字的日志
        self.soft_root = os.path.join(os.path.dirname(__file__), '..', '..')
        self.output_path = os.path.join(self.soft_root, 'output')
        self.temp_path = os.path.join(self.soft_root, 'temp')
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        self.log_name_by_serial = {}
        self.product = ''

        self.start_time = format_time(time_formatter=format_2)

    def load_conf(self, p=None):
        if p is None:
            p = os.path.join(self.soft_root, 'res', 'application.yml')
        with open(p, 'r', encoding='utf-8') as rf:
            conf = yaml.load(rf.read(), Loader=yaml.FullLoader)
        if conf is None:
            return
        self.svm_list = conf['app']['interval']['svm']
        self.likelihood_list = conf['app']['interval']['likelihood']
        self.confidence_list = conf['app']['interval']['confidence']

        self.remote_base = conf['app']['remote_base']
        self.remote_result_dir = conf['app']['remote_result_dir']
        self.cmd_path = conf['app']['cmd_path']
        self.wav_path = conf['app']['wav']['wav_path']
        self.wav_schema = conf['app']['wav']['wav_schema']
        self.wav_load_mode = int(conf['app']['wav']['load_mode'])
        self.retrieve_script = conf['app']['wav']['retrieve_script'].format(self.wav_path.replace('\\', '/'),
                                                                            '&'.join(self.wav_schema),
                                                                            self.cmd_path.replace('\\', '/'))

        self.first_read = conf['app']['controller']['first_read']
        self.wav_count_one_cmder = conf['app']['controller']['wav_count_one_cmder']
        self.repeat_play_count = conf['app']['controller']['repeat_play_count']
        self.play_mode = conf['app']['controller']['play_mode']
        self.amplify_volume = bool(conf['app']['controller']['amplify_volume'])
        self.play_separator = conf['app']['controller']['play_separator']

        self.log_filter = LogFilter(conf['app']['log']['log_filter'])
        self.product = conf['app']['mapping']['product']
        serials = conf['app']['mapping']['serial']
        versions = conf['app']['mapping']['version']
        for i in range(0, len(serials)):
            self.log_name_by_serial[serials[i]] = versions[i]

        self.remote_host = conf['app']['remote']['host']
        self.remote_port = int(conf['app']['remote']['port'])
        self.remote_username = conf['app']['remote']['username']
        self.remote_password = conf['app']['remote']['password']
        print('success to load application.yml')


# 命令词映射， eg: 晚安:晚安安
cmd_mapping = {

}

corpus_conf = CorpusConf()
if __name__ == '__main__':
    corpus_conf.load_conf()
