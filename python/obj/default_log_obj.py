# coding=utf-8
import os
import traceback
from time import sleep

from common.logger import logger
from common.time_util import format_time, parse_time, format_3, format_2
from conf.config import corpus_conf, cmd_mapping
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
            items = one_log.split('decode result is ')
            if len(items) < 2:
                return
            content = items[1]
            eles = content.split(' ')
            tmp = r.get(eles[0]) or DefaultLogItem()
            tmp.word = eles[0]
            i = self.get_interval_index(eles[1].split(':')[0], corpus_conf.confidence_list)
            tmp.confidence[i] = tmp.confidence[i] + 1
            i = self.get_interval_index(eles[2].split(':')[0], corpus_conf.likelihood_list)
            tmp.likelihood[i] = tmp.likelihood[i] + 1
            i = self.get_interval_index(eles[2].split(':')[0], corpus_conf.svm_list)
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
            self.__column_name = ['命令词', '正确率', '总次数']
            if len(self.items) > 0:
                key0 = [key for key in self.items.keys()][0]
                self.__column_name.extend(self.items[key0].get_column_name())
        return self.__column_name

    def exist_items(self):
        return len(self.items) > 0

    def get_right_count(self):
        o = self.items.get(cmd_mapping.get(self.cmd) or self.cmd) or None
        if o is None:
            return 0
        return o.count


class DefaultLogItem:
    def __init__(self):
        self.count = 0
        self.word = ''
        self.confidence = [0 for _ in corpus_conf.confidence_list]
        self.likelihood = [0 for _ in corpus_conf.likelihood_list]
        self.svm = [0 for _ in corpus_conf.svm_list]
        self.__column_name = None

    def get_column_name(self):
        if self.__column_name is None:
            c_l = ['CONFIDENCE:%s' % v for v in corpus_conf.confidence_list]
            l_l = ['LIKELIHOOD:%s' % v for v in corpus_conf.likelihood_list]
            s_l = ['SVM:%s' % v for v in corpus_conf.svm_list]
            self.__column_name = ['识别词', '次数', *c_l, *l_l, *s_l]
        return self.__column_name


result_map = {}  # {com:{cmd:DefaultLogOut}}


def parse_default_log(obj_l):
    log_obj = DefaultLogIn(obj_l)
    com = log_obj.com
    cmd = log_obj.wav_obj.content
    result_map[com] = result_map.get(com) or {}
    log_output = result_map[com].get(cmd) or DefaultLogOut()
    log_output.cmd = cmd
    log_output.com = com
    log_output.count = log_output.count + 1
    log_obj.parse_log(log_output.items)
    log_output.rate = '%.4f' % float(log_output.get_right_count() / log_output.count)
    result_map[log_output.com][log_output.cmd] = log_output


def write_default_log_2_csv(service):
    """
    :type service: audio_identify.identify.AudioIdentify
    """
    while service.can_write:
        for com, com_result_d in result_map.items():
            if len(com_result_d) == 0:
                continue
            file_name = '{0}_{1}_{2}.csv'.format(corpus_conf.log_name_by_serial.get(com),
                                                 corpus_conf.wav_count_one_cmder,
                                                 format_time(parse_time(corpus_conf.start_time, format_2), format_3)
                                                 )
            try:
                with open(os.path.join(corpus_conf.output_path, file_name), 'w+', encoding='utf-8') as wf:
                    cmds_result = [v for _, v in dict(com_result_d).items()]
                    row_format = write_csv_header(cmds_result, wf)
                    for cmd_result in cmds_result:
                        write_one_cmd_log(cmd_result, row_format, wf)
            except Exception as e:
                logger.error('Failed to write test result, err: %s, %s' % (e, traceback.format_exc()))
        sleep(30)


def write_csv_header(cmds_result, wf):
    # 最大程度获取列名
    column_names = get_cloumn_names(cmds_result)
    row_format = ','.join(['%s' for _ in range(0, len(column_names))]) + '\n'
    wf.write(row_format % tuple(column_names))
    return row_format


def write_one_cmd_log(cmd_result, row_format, wf):
    index = 0
    log_items = sorted(cmd_result.items.items(), key=lambda k: k[1].count, reverse=True)
    for _, v in log_items:
        if index == 0:
            items = ((cmd_result.cmd, cmd_result.rate, cmd_result.count, v.word, v.count)
                     + tuple(v.confidence) + tuple(v.likelihood) + tuple(v.svm))
            # logger.info('pick bug: {0} ---- {1}'.format(row_format, items))
            wf.write(row_format % items)
        else:
            items = (('', '', '', v.word, v.count) + tuple(v.confidence)
                     + tuple(v.likelihood) + tuple(v.svm))
            # logger.info('pick bug1: {0} ---- {1}'.format(row_format, items))
            wf.write(row_format % items)
        index += 1


def get_cloumn_names(cmds_result):
    item = cmds_result[-1]
    for cmd_result in cmds_result:
        if cmd_result.exist_items():
            item = cmd_result
            break
    column_names = item.get_column_name()
    return column_names


if __name__ == '__main__':
    aa = ['2020-01-14 14:55:24', 'COM5',
          AudioObj().set_v('O1051_5461', '打开空调', '\\\\192.168.1.8\\corpus\\train\\wavs\\O1051\\O1051_5461.wav'),
          'OK decode result is 小美小美 98.372200:40.000000 0.769101:0.520000 2.835265:-10.000000',
          'OK decode result is 打开空调 97.535637:30.000000 0.885568:0.300000 3.179217:-10.000000']
    bb = ['2020-01-14 14:55:24', 'COM5',
          AudioObj().set_v('O1051_5461', '关闭空调', '\\\\192.168.1.8\\corpus\\train\\wavs\\O1051\\O1051_5461.wav')]
    parse_default_log(aa)
    parse_default_log(bb)
