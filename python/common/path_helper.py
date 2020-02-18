# coding=utf-8
import os
import re

from common.time_util import *
from conf.config import corpus_conf


def combine_path(base, *path1):
    r = base
    for p in path1:
        r = os.path.join(r, *re.split(r'[/\\]', p))
    return r


def get_cmder_path():
    return combine_path(corpus_conf.remote_base, corpus_conf.cmd_path)


def get_wav_path():
    return combine_path(corpus_conf.remote_base, corpus_conf.wav_path)


def get_remote_result_dir_name():
    template_name = '{0}_result_{1}'
    basename = template_name.format(corpus_conf.product, format_time(time_formatter=format_3))
    remote_root_dir = combine_path(corpus_conf.remote_base, corpus_conf.remote_result_dir)
    dst = os.path.join(remote_root_dir, basename)
    if os.path.exists(dst):
        dst = os.path.join(remote_root_dir,
                           template_name.format(corpus_conf.product, format_time(time_formatter=format_5)))
    return dst


if __name__ == '__main__':
    print(combine_path(corpus_conf.remote_base, corpus_conf.cmd_path))
