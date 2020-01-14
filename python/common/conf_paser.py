# coding=utf-8
import json
import random

from audio_identify.audio_obj import AudioObj
from common.path_helper import *


def load_cmder(file_path=get_cmder_path()):
    with open(file_path, 'r+', encoding='utf-8') as f:
        return json.load(f).get('words')


def get_cmdstr_by_config(file_path=get_cmder_path()):
    tmp = []
    cmders = load_cmder(file_path)
    for item in cmders:
        tmp.append(item.get('word'))
    return tmp


def get_wav_mapping(wav_path=get_wav_path(), wav_count_one_cmd=CorpusConf.WAV_COUNT_ONE_CMDER):
    scp_path = os.path.join(wav_path, 'wav.scp')
    text_path = os.path.join(wav_path, 'text')

    def read_file(p):
        tmp = {}
        with open(p, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if isinstance(line, str) and line != '':
                    eles = line.split(' ')
                    tmp[eles[0]] = eles[1].strip('\n')
        return tmp

    mapping = {}
    scp_d, text_d = read_file(scp_path), read_file(text_path)
    cmd_l = get_cmdstr_by_config()
    for aid, wav_source in scp_d.items():
        cmd_str = text_d.get(aid)
        if cmd_str in cmd_l:
            obj = AudioObj(aid, cmd_str, combine_path(CorpusConf.REMOTE_BASE, wav_source))
            mapping[cmd_str] = mapping.get(cmd_str) or []
            mapping[cmd_str].append(obj)

    filter_wav_mapping(mapping, wav_count_one_cmd)
    return mapping


def filter_wav_mapping(mapping, wav_count_one_cmd):
    for k, v in mapping.items():
        tmp = []
        t_count = wav_count_one_cmd
        while t_count > 0:
            index = random.randint(0, len(v))
            tmp.append(v[index])
            t_count -= 1
        mapping[k] = tmp


def parse_wav(p=get_wav_path(), wav_count_one_cmd=CorpusConf.WAV_COUNT_ONE_CMDER):
    if os.path.isdir(p):
        mapping = get_wav_mapping(p, wav_count_one_cmd)
    else:
        with open(p, 'r+', encoding='utf-8') as f:
            mapping = json.load(f)
    return mapping


if __name__ == '__main__':
    mapping1 = parse_wav(wav_count_one_cmd=3)
    print(mapping1)
