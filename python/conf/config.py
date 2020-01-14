# coding=utf-8
import os


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
    PLAY_SEPARATOR = 5  # 语音播报间隔
    LOG_FILTER = ['agc handler']  # 过滤掉包含关键字的日志
    SOFT_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
    OUTPUT_PATH = os.path.join(SOFT_ROOT, 'output')
