# coding=utf-8
import os

import yaml


class CorpusConf:
    def __init__(self):
        # 无上限为max, 无下限为min
        self.svm_list = [
            '0-10',
            '10-max'
        ]
        self.likelihood_list = [
            '0-10',
            '10-max'
        ]
        self.confidence_list = [
            '0-10',
            '10-max'
        ]
        self.remote_base = r'\\192.168.1.8'
        self.base_path = r'\corpus\project\mddc'  # 项目路径
        self.cmd_path = r'/res/config.json'
        self.wav_path = 'train_mini'
        self.wav_count_one_cmder = 2
        self.repeat_play_count = 1
        self.play_separator = 2  # 语音播报间隔
        self.log_filter = ['agc handler']  # 过滤掉包含关键字的日志
        self.soft_root = os.path.join(os.path.dirname(__file__), '..', '..')
        self.output_path = os.path.join(self.soft_root, 'output')
        self.temp_path = os.path.join(self.soft_root, 'temp')
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        self.log_name_by_serial = {}

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

        self.remote_base = conf['app']['path']['remote_base']
        self.base_path = conf['app']['path']['base_path']
        self.cmd_path = conf['app']['path']['cmd_path']
        self.wav_path = conf['app']['path']['wav_path']

        self.wav_count_one_cmder = conf['app']['controller']['wav_count_one_cmder']
        self.repeat_play_count = conf['app']['controller']['repeat_play_count']
        self.play_separator = conf['app']['controller']['play_separator']

        self.log_filter = conf['app']['log']['log_filter']
        serials = conf['app']['mapping']['serial']
        versions = conf['app']['mapping']['version']
        for i in range(0, len(serials)):
            self.log_name_by_serial[serials[i]] = versions[i]
        print('success to load application.yml')


corpus_conf = CorpusConf()
if __name__ == '__main__':
    corpus_conf.load_conf()
