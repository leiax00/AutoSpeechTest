# coding=utf-8
import json

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


def get_wav_mapping(wav_path=get_wav_path()):
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
    return mapping


if __name__ == '__main__':
    mapping1 = get_wav_mapping()
    print(mapping1)
