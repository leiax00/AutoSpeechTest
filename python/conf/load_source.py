# coding=utf-8
import json
import os
import random

from common.logger import logger
from common.path_helper import get_cmder_path, get_wav_path, combine_path
from common.ssh_util import ssh_exec
from conf.config import corpus_conf
from obj.audio_obj import AudioObj


class LoadSource:
    def __init__(self):
        self.cmd_path = get_cmder_path()
        self.wav_path = get_wav_path()
        self.wav_schema = corpus_conf.wav_schema
        self.wav_mapping = {}

    def parse_wav(self, p, wav_count_one_cmd):
        self.wav_mapping.clear()
        try:
            if os.path.isdir(p):
                self.wav_path = p
                if corpus_conf.wav_load_mode == 1:
                    self.get_wav_mapping1()
                elif corpus_conf.wav_load_mode == 2:
                    self.get_wav_mapping()
                self.filter_wav_mapping(wav_count_one_cmd)
            else:
                with open(p, 'r+', encoding='utf-8') as f:
                    self.wav_mapping = json.load(f)
                    for k, v_l in self.wav_mapping.items():
                        tmp = []
                        for v in v_l:
                            tmp.append(json.loads(json.dumps(eval(v)), object_hook=AudioObj))
                        self.wav_mapping[k] = tmp
        except Exception as e:
            logger.error('failed to parse wav, err: {0}'.format(e))
        return self.wav_mapping

    def get_wav_mapping1(self):
        """
        通过语料根路径读取语料，增加schema,限定语料类型
        """
        wp = os.path.join(self.wav_path, 'auto_test_retrieve_info.json')
        with open(wp, 'r', encoding='utf-8') as wf:
            wav_info = json.load(wf)
            for cmd_str, wav_ps in wav_info.items():
                for wav_p in wav_ps:
                    aid = os.path.basename(wav_p).split('.')[0]
                    obj = AudioObj().set_v(aid, cmd_str, combine_path(corpus_conf.remote_base, wav_p))
                    self.wav_mapping[cmd_str] = self.wav_mapping.get(cmd_str) or []
                    self.wav_mapping[cmd_str].append(obj)

    def get_wav_mapping(self):
        """
        通过wav.scp 和 text文件读取语料对象
        """
        scp_path = os.path.join(self.wav_path, 'wav.scp')
        text_path = os.path.join(self.wav_path, 'text')

        def read_file(p):
            tmp = {}
            with open(p, 'r+', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if isinstance(line, str) and line != '':
                        eles = line.split(' ')
                        tmp[eles[0]] = eles[1].strip('\n')
            return tmp

        scp_d, text_d = read_file(scp_path), read_file(text_path)
        cmd_l = self.get_cmdstr_by_config()
        for aid, wav_source in scp_d.items():
            cmd_str = text_d.get(aid)
            if cmd_str in cmd_l:
                obj = AudioObj().set_v(aid, cmd_str, combine_path(corpus_conf.remote_base, wav_source))
                self.wav_mapping[cmd_str] = self.wav_mapping.get(cmd_str) or []
                self.wav_mapping[cmd_str].append(obj)

    def filter_wav_mapping(self, wav_count_one_cmd):
        for k, v in self.wav_mapping.items():
            count = wav_count_one_cmd
            if wav_count_one_cmd > len(v):
                logger.warn('wav num is not enough, use all wavs, cmd:{0}, len:{1}'.format(k, len(v)))
                count = len(v)
            index_l = random.sample(range(0, len(v)), count)
            tmp = []
            for i in index_l:
                tmp.append(v[i])
            self.wav_mapping[k] = tmp
