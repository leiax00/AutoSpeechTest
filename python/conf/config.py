# coding=utf-8
import os

import yaml


class CorpusConf:
    # 无上限为max, 无下限为min
    SVM_LIST = [
        '0-10',
        '10-max'
    ]
    LIKELIHOOD_LIST = [
        '0-10',
        '10-max'
    ]
    CONFIDENCE_LIST = [
        '0-10',
        '10-max'
    ]
    REMOTE_BASE = r'\\192.168.1.8'
    BASE_PATH = r'\corpus\project\mddc'  # 项目路径
    CMD_PATH = r'/res/config.json'
    WAV_PATH = 'train_mini'
    WAV_COUNT_ONE_CMDER = 2
    REPEAT_PLAY_COUNT = 1
    PLAY_SEPARATOR = 2  # 语音播报间隔
    LOG_FILTER = ['agc handler']  # 过滤掉包含关键字的日志
    SOFT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
    OUTPUT_PATH = os.path.join(SOFT_ROOT, 'output')

    @staticmethod
    def load_conf(path=os.path.join(SOFT_ROOT, 'res', 'application.yml')):
        with open(path, 'r', encoding='utf-8') as rf:
            conf = yaml.load(rf.read())
        if conf is None:
            return
        CorpusConf.SVM_LIST = conf['app']['interval']['svm']
        CorpusConf.LIKELIHOOD_LIST = conf['app']['interval']['likelihood']
        CorpusConf.CONFIDENCE_LIST = conf['app']['interval']['confidence']

        CorpusConf.REMOTE_BASE = conf['app']['path']['remote_base']
        CorpusConf.BASE_PATH = conf['app']['path']['base_path']
        CorpusConf.CMD_PATH = conf['app']['path']['cmd_path']
        CorpusConf.WAV_PATH = conf['app']['path']['wav_path']

        CorpusConf.WAV_COUNT_ONE_CMDER = conf['app']['controller']['wav_count_one_cmder']
        CorpusConf.REPEAT_PLAY_COUNT = conf['app']['controller']['repeat_play_count']
        CorpusConf.PLAY_SEPARATOR = conf['app']['controller']['play_separator']

        CorpusConf.LOG_FILTER = conf['app']['log']['log_filter']
        print('success to load application.yml')


if __name__ == '__main__':
    CorpusConf.load_conf()
