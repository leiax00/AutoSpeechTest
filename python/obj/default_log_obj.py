# coding=utf-8
import json
import os
from threading import Timer, Thread
from time import sleep

import schedule as schedule

from common.logger import logger
from common.time_util import format_time
from conf.config import CorpusConf
from obj.audio_obj import AudioObj


class DefaultLogIn:
    def __init__(self, obj_l):
        """
        :type obj_l: list
        """
        self.time = obj_l[0]
        self.com = obj_l[1]
        self.wav_obj = obj_l[2]
        self.log_l = obj_l[3:] if len(obj_l) > 3 else []

    def parse_log(self, r):
        for one_log in self.log_l:
            one_log = str(one_log)
            content = one_log.split('decode result is ')[1]
            eles = content.split(' ')
            tmp = r.get(eles[0]) or DefaultLogItem()
            tmp.word = eles[0]
            i = self.get_interval_index(eles[1].split(':')[0], CorpusConf.CONFIDENCE_LIST)
            tmp.confidence[i] = tmp.confidence[i] + 1
            i = self.get_interval_index(eles[2].split(':')[0], CorpusConf.LIKELIHOOD_LIST)
            tmp.likelihood[i] = tmp.likelihood[i] + 1
            i = self.get_interval_index(eles[2].split(':')[0], CorpusConf.SVM_LIST)
            tmp.svm[i] = tmp.svm[i] + 1
            tmp.count += 1
            r[tmp.word] = tmp

    @staticmethod
    def get_interval_index(v, interval_l):
        for i in range(0, len(interval_l)):
            inter = interval_l[i].split('-')
            if inter[0] == 'min' and inter[1] != 'max':
                if float(v) < float(inter[1]):
                    return i
            elif inter[0] != 'min' and inter[1] == 'max':
                if float(inter[0]) <= float(v):
                    return i
            elif inter[0] == 'min' and inter[1] == 'max':
                return 0
            else:
                if float(inter[0]) <= float(v) < float(inter[1]):
                    return i


class DefaultLogOut:
    def __init__(self):
        self.cmd = ''
        self.count = 0
        self.rate = 0
        self.items = {}
        self.__column_name = None

    def get_column_name(self):
        if self.__column_name is None:
            self.__column_name = ['命令词']
            if len(self.items) > 0:
                key0 = [key for key in self.items.keys()][0]
                self.__column_name.extend(self.items[key0].get_column_name())
            self.__column_name.extend(['总次数', '正确率'])
        return self.__column_name

    def get_right_count(self):
        o = self.items.get(self.cmd) or None
        if o is None:
            return 0
        return o.count


class DefaultLogItem:
    def __init__(self):
        self.count = 0
        self.word = ''
        self.confidence = [0 for _ in CorpusConf.CONFIDENCE_LIST]
        self.likelihood = [0 for _ in CorpusConf.LIKELIHOOD_LIST]
        self.svm = [0 for _ in CorpusConf.SVM_LIST]
        self.__column_name = None

    def get_column_name(self):
        if self.__column_name is None:
            c_l = ['CONFIDENCE:%s' % v for v in CorpusConf.CONFIDENCE_LIST]
            l_l = ['LIKELIHOOD:%s' % v for v in CorpusConf.LIKELIHOOD_LIST]
            s_l = ['SVM:%s' % v for v in CorpusConf.SVM_LIST]
            self.__column_name = ['识别词', *c_l, *l_l, *s_l, '次数']
        return self.__column_name


result_map = {}  # {com:{cmd:DefaultLogOut}}


def parse_default_log(obj_l):
    log_obj = DefaultLogIn(obj_l)
    com = log_obj.com
    cmd = log_obj.wav_obj.content
    result_map[com] = result_map.get(com) or {}
    r = result_map[com].get(cmd) or DefaultLogOut()
    r.cmd = cmd
    r.com = com
    r.count = r.count + 1
    log_obj.parse_log(r.items)
    r.rate = '%.4f' % float(r.get_right_count() / r.count)
    result_map[r.com][r.cmd] = r


def write_default_log_2_csv(can_write):
    while can_write:
        logger.info('start to write result.....')
        for com, obj in result_map.items():
            file_name = 'result_%s.csv' % com
            with open(os.path.join(CorpusConf.OUTPUT_PATH, file_name), 'w+', encoding='utf-8') as wf:
                rs = [v for _, v in dict(obj).items()]
                column_names = rs[0].get_column_name()

                row_format = ','.join(['%s' for _ in range(0, len(column_names))]) + '\n'
                wf.write(row_format % tuple(column_names))
                for r in rs:
                    index = 0
                    for _, v in r.items.items():
                        if index == 0:
                            wf.write(row_format % (
                                    (r.cmd, v.word) + tuple(v.confidence) + tuple(v.likelihood) + tuple(v.svm) + (
                            v.count, r.count, r.rate)))
                        else:
                            wf.write(row_format % (
                                    ('', v.word) + tuple(v.confidence) + tuple(v.likelihood) + tuple(v.svm) + (
                                v.count, '', '')))
                        index += 1
        sleep(10)


if __name__ == '__main__':
    aa = ['2020-01-14 14:55:24', 'COM5', AudioObj().set_v('a', '小美小美', 'w+'),
          'OK decode result is 小美小美 98.787186:40.000000 1.055722:0.520000 3.542980:-10.000000',
          'OK decode result is 小美小美1 98.787186:40.000000 1.055722:0.520000 3.542980:-10.000000']
    parse_default_log(aa)
    parse_default_log(aa)
    write_default_log_2_csv(True)
    while True:
        pass
