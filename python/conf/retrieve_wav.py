# coding=utf-8
import json
import os
import sys


def retrieve_train_wav(wav_path, wav_schema, cmd_path):
    result = {}
    cmd_l = get_cmdstr_by_config(cmd_path)
    dirs = os.listdir(wav_path)
    for d in dirs:
        if d[0:1] not in wav_schema:
            continue
        dir_path = os.path.join(wav_path, d)
        file_l = os.listdir(dir_path)
        for f in file_l:
            wav_p = os.path.join(dir_path, '{0}.{1}'.format(f.split('.')[0], 'wav'))
            f_path = os.path.join(dir_path, f)
            if os.path.isdir(f_path) or not f.endswith('.txt'):
                continue
            with open(f_path, 'r', encoding='utf-8') as rf:
                cmd = rf.readlines()[0].strip('\r\t\n')
                if cmd in cmd_l:
                    result[cmd] = result.get(cmd) or []
                    result[cmd].append(wav_p)
    write_result_2_file(wav_path, result)


def load_cmder(cmd_path):
    with open(cmd_path, 'r+', encoding='utf-8') as f:
        return json.load(f).get('words')


def get_cmdstr_by_config(cmd_path):
    tmp = []
    cmders = load_cmder(cmd_path)
    for item in cmders:
        tmp.append(item.get('word'))
    return tmp


def write_result_2_file(wav_path, content):
    with open(os.path.join(wav_path, 'auto_test_retrieve_info.json'), 'w+', encoding='utf-8') as wf:
        json.dump(content, wf, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    wp = r'\corpus\train\wavs'
    ws = r'A'
    cp = r'\corpus\project\mddc\res\config.json'
    argv = [wp.replace('\\', '/'), ws.split('&'), cp.replace('\\', '/')]
    for i in range(1, len(sys.argv)):
        argv[i-1] = sys.argv[i]
    retrieve_train_wav(argv[0], argv[1], argv[2])
    print('finish')
