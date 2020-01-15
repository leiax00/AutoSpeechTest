# coding=utf-8
import os
import re

from conf.config import corpus_conf


def combine_path(base, *path1):
    r = base
    for p in path1:
        r = os.path.join(r, *re.split(r'[/\\]', p))
    return r


def get_cmder_path():
    return combine_path(corpus_conf.remote_base, corpus_conf.base_path, corpus_conf.cmd_path)


def get_wav_path():
    if corpus_conf.wav_path.strip() == '':
        return corpus_conf.wav_path.strip()
    return combine_path(corpus_conf.remote_base, corpus_conf.base_path, corpus_conf.wav_path)


if __name__ == '__main__':
    print(combine_path(corpus_conf.remote_base, corpus_conf.base_path, corpus_conf.cmd_path))
