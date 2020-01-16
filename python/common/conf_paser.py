# coding=utf-8
import json
import random

from common.logger import logger
from common.path_helper import *
from conf.config import corpus_conf
from obj.audio_obj import AudioObj


def load_cmder(file_path):
    with open(file_path, 'r+', encoding='utf-8') as f:
        return json.load(f).get('words')


def get_cmdstr_by_config(file_path):
    tmp = []
    cmders = load_cmder(file_path)
    for item in cmders:
        tmp.append(item.get('word'))
    return tmp


def get_wav_mapping(wav_path=get_wav_path(), wav_count_one_cmd=corpus_conf.wav_count_one_cmder):
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
    cmd_l = get_cmdstr_by_config(get_cmder_path())
    for aid, wav_source in scp_d.items():
        cmd_str = text_d.get(aid)
        if cmd_str in cmd_l:
            obj = AudioObj().set_v(aid, cmd_str, combine_path(corpus_conf.remote_base, wav_source))
            mapping[cmd_str] = mapping.get(cmd_str) or []
            mapping[cmd_str].append(obj)

    filter_wav_mapping(mapping, wav_count_one_cmd)
    return mapping


def filter_wav_mapping(mapping, wav_count_one_cmd):
    for k, v in mapping.items():
        if wav_count_one_cmd > len(v):
            logger.warn('wav num is not enough, use all wavs, cmd:{0}, len:{1}'.format(k, len(v)))
            wav_count_one_cmd = len(v)
        index_l = random.sample(range(0, len(v)), wav_count_one_cmd)
        tmp = []
        for i in index_l:
            tmp.append(v[i])
        mapping[k] = tmp


def parse_wav(p, wav_count_one_cmd):
    mapping = {}
    try:
        if os.path.isdir(p):
            mapping = get_wav_mapping(p, wav_count_one_cmd)
        else:
            with open(p, 'r+', encoding='utf-8') as f:
                mapping = json.load(f)
                for k, v_l in mapping.items():
                    tmp = []
                    for v in v_l:
                        tmp.append(json.loads(json.dumps(eval(v)), object_hook=AudioObj))
                    mapping[k] = tmp
    except Exception as e:
        logger.error('failed to parse wav, err: %s', e)
    return mapping


if __name__ == '__main__':
    mapping1 = parse_wav(get_wav_path(), wav_count_one_cmd=200)
    print(mapping1)
