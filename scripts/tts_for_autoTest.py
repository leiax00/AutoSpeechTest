# coding=utf-8
import json
import os
import re


def combine_path(base, *path1):
    r = base
    for p in path1:
        r = os.path.join(r, *re.split(r'[/\\]', p))
    return r


if __name__ == '__main__':
    remote = r'\\192.168.1.8'
    f = r'\\192.168.1.8\corpus\project\matong\tts_test\summary_info.txt'
    d = {}
    with open(f, 'r', encoding='utf-8') as rf:
        lines = rf.readlines()
        for line in lines:
            es = line.split('\t')
            d[es[0]] = d.get(es[0]) or []
            name = os.path.basename(es[1].strip()).replace('.wav', '')
            tmp = {'aid': name, 'content': es[0], 'source': combine_path(remote, es[1].strip())}
            d[es[0]].append(tmp.__str__())
    with open('tmp.json', 'w+', encoding='utf-8') as wf:
        json.dump(d, wf, indent=4, ensure_ascii=False)
