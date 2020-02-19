# coding=utf-8
"""
脚本用于语音合成，并进行拆分
"""
import json
import os
import re
import sys
import traceback
import urllib

import requests
from pydub import AudioSegment
from pydub.silence import split_on_silence

url_template = 'http://yyapi.bilianshu.com/api?type={0}&text={1}&speaker={2}' \
               '&token=kFjRSxdPnBFV5gbPxkjjpxCjO3DuclRB'
# 不包括英音
type_a = [
    'Xiaoyun',  # 标准女声
    'Xiaogang',  # 标准男声 ********
    'Xiaomeng',  # 标准女声
    'Xiaowei',  # 标准男声
    'Ruoxi',  # 温柔女声
    'Siqi',  # 温柔女声
    'Sijia',  # 标准女声
    'Sicheng',  # 标准男声 ********
    'Aiqi',  # 温柔女声
    'Aijia',  # 标准女声
    'Aicheng',  # 标准男声 ********
    'Aida',  # 标准男声 ********
    'Ninger',  # 标准女声
    'Ruilin',  # 标准女声 ********
    'Amei',  # 甜美女声
    'Xiaoxue',  # 温柔女声
    'Siyue',  # 温柔女声
    'Aiya',  # 严厉女声
    'Aixia',  # 亲和女声
    'Aimei',  # 甜美女声
    'Aiyu',  # 自然女声
    'Aiyue',  # 温柔女声 ********
    'Aijing',  # 严厉女声 ********
    'Xiaomei',  # 甜美女声
    'Aina',  # 浙普女声 ********
    'Yina',  # 浙普女声
    'Sijing',  # 严厉女声
    'Sitong',  # 儿童音
    'Xiaobei',  # 萝莉女声
    'Aitong',  # 儿童音
    'Aiwei',  # 萝莉女声 ********
    'Aibao',  # 萝莉女声 ********
]

type_b = [
    0,  # 女声
    1,  # 男声
    2,  # 男声
    4,  # 女声
    5,  # 女声
    6,  # 男声
    1000,  # 男声
    1001,  # 女声
    1002,  # 女声
    1003,  # 女声
    1050,  # 英文男声
    1051,  # 英文女声
]

type_c = [
    0,  # 标准女声
    1,  # 标准男声
    3,  # 情感男声
    4,  # 情感女声
    5,  # 情感女声
    103,  # 儿童音
    106,  # 情感男声
    110,  # 儿童音
    111,  # 情感女声
]

auto_test_spks = [
    'Xiaogang',
    'Sicheng',
    'Aicheng',
    'Aida',
    'Ruilin',
    'Aiyue',
    'Aijing',
    'Aina',
    'Aiwei',
    'Aibao',
]


def synthesis_audio(cmd_l, output_path=os.path.dirname(__file__), spk_type='a', speaker='Siqi', cmd_count_of_one_req=5):
    """
    :param output_path: 输出路径
    :param cmd_count_of_one_req: 一次请求的命令词数量
    :param spk_type: 说话人类型
    :param speaker: 说话人
    :type cmd_l: list
    """
    output_path = os.path.join(output_path, 'origin')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    count = int(len(cmd_l) / cmd_count_of_one_req)
    if len(cmd_l) % cmd_count_of_one_req != 0:
        count = count + 1
    for i in range(0, count):
        if i + 1 == count:
            tmp = cmd_l[i * cmd_count_of_one_req:]
        else:
            tmp = cmd_l[i * cmd_count_of_one_req: (i + 1) * cmd_count_of_one_req]
        text = urllib.request.quote('<break time="500ms"/>'.join(tmp))
        req_url = url_template.format(spk_type, text, speaker)
        resp = requests.get(req_url)
        remaining_times = json.loads(json.dumps(dict(resp.headers))).get('Total-count')
        if int(remaining_times) <= 1000:
            print('*' * 30, '\nremaining_times is not enough, times:{0}, url:{1}'.format(remaining_times, req_url),
                  '*' * 30)
        if spk_type == 'a':
            filename = '{0}_{1}.wav'.format(speaker.lower(), i + 1)
        else:
            filename = '{0}{1}_{2}.wav'.format(spk_type, speaker, i + 1)
        output_file = os.path.join(output_path, filename)
        urllib.request.urlretrieve(req_url, output_file)
        if os.path.exists(output_file):
            split_wav(tmp, output_file, speaker, i * cmd_count_of_one_req)
        else:
            print('failed to synthesis wav. cmd:{0}, file:{1}'.format(tmp, output_file))


def split_wav(cmd_words, wav_file, speaker, index):
    print('start to split wav:{0}'.format(wav_file))
    try:
        wav_root_dir = os.path.join(os.path.dirname(os.path.dirname(wav_file)), 'wav')
        if not os.path.exists(wav_root_dir) or not os.path.isdir(wav_root_dir):
            os.mkdir(wav_root_dir)
        sound = AudioSegment.from_wav(wav_file)
        print('start to split wav:{0}, sound.dBFS:{1}'.format(wav_file, sound.dBFS))
        # min_silence_len 最小静音长度
        # silence_thresh 音量阈值，越高声音越大
        chunks = split_on_silence(sound, min_silence_len=300, silence_thresh=-50)
        print('end to split wav, count:{0}'.format(len(chunks)))

        with open(os.path.join(wav_root_dir, '..', 'summary_info.txt'), 'a', encoding='utf-8') as wfs:
            for i in range(len(chunks)):
                index += 1
                new = chunks[i]
                wav_p = os.path.join(wav_root_dir, '{0}_{1}.wav'.format(speaker.lower(), index))
                new.export(wav_p, format='wav')
                with open(wav_p.replace('.wav', '.txt'), 'w+', encoding='utf-8') as wf:
                    wf.write(cmd_words[i])
                wfs.write('{0}\t{1}\n'.format(cmd_words[i], wav_p))
                wfs.flush()
    except Exception as e:
        print('error happen: {0}, detail:{1}'.format(e, traceback.format_exc()))


def get_cmd_list(project_root):
    if os.path.isfile(project_root):  # 针对corpus.txt格式的语音合成
        cmd_l = get_cmd_from_corpus(project_root)
    else:  # 针对传入project根路径的语音合成
        cmd_l = get_cmd_from_project(project_root)
    return cmd_l


def get_cmd_from_project(project_root):
    cmd_l = []
    conf = os.path.join(project_root, 'res', 'config.json')
    with open(conf, 'r+', encoding='utf-8') as rf:
        tmp = json.load(rf)
        for item in tmp.get('words'):
            if item.get('type') == 'cmd':
                cmd_l.append(item.get('word'))
    return cmd_l


def get_cmd_from_corpus(project_root):
    with open(project_root, 'r+', encoding='utf-8') as rf:
        cmd_l = [line.strip('\r\t\n') for line in rf.readlines()]
    return cmd_l


def combine_path(base, *path1):
    r = base
    for p in path1:
        r = os.path.join(r, *re.split(r'[/\\]', p))
    return r


def generate_auto_test_wav_file(rp, summary_info_dir):
    d = {}
    with open(os.path.join(summary_info_dir, 'summary_info.txt'), 'r', encoding='utf-8') as rf:
        lines = rf.readlines()
        for line in lines:
            es = line.split('\t')
            d[es[0]] = d.get(es[0]) or []
            name = os.path.basename(es[1].strip()).replace('.wav', '')
            tmp = {'aid': name, 'content': es[0], 'source': combine_path(rp, es[1].strip())}
            d[es[0]].append(tmp.__str__())
    with open(os.path.join(summary_info_dir, 'tts_4_auto_test_all.json'), 'w+', encoding='utf-8') as wf:
        json.dump(d, wf, indent=4, ensure_ascii=False)


def synthesis_all_spk_wav(cmd_l, output_p):
    for speaker in type_a:
        synthesis_audio(cmd_l, output_p, spk_type='a', speaker=str(speaker))
    # for speaker in type_b:
    #     synthesis_audio(cmd_l, output_p, spk_type='b', speaker=str(speaker))
    # for speaker in type_c:
    #     synthesis_audio(cmd_l, output_p, spk_type='c', speaker=str(speaker))


def is_auto_test_spk(aid, spks):
    new_spks = [speaker.lower() for speaker in spks]
    real_spk = aid.split('_')[0]
    rm = re.match(r'[bc](\d*)', real_spk)
    if rm is not None:
        real_spk = int(rm.group(1))
    return True if real_spk in new_spks else False


def mkdir(base_p, relative_p):
    dst = combine_path(base_p, relative_p)
    if not os.path.exists(dst):
        os.makedirs(dst)
    return dst


def filter_4_auto_test(rp, src, dst):
    dst = mkdir(dst, 'tts_test')
    src_file = os.path.join(src, 'summary_info.txt')
    rst = {}
    lines = []
    with open(src_file, 'r', encoding='utf-8') as rf:
        for line in rf:
            kvs = line.split('\t')
            cmd = kvs[0].strip('\r\t\n')
            basename = os.path.basename(kvs[1].strip('\r\t\n'))
            aid = basename.replace('.wav', '')
            if is_auto_test_spk(aid, auto_test_spks):
                wav = combine_path(rp, kvs[1].strip('\r\t\n'))
                tmp = {'aid': aid, 'content': cmd, 'source': wav}
                rst[cmd] = rst.get(cmd) or []
                rst[cmd].append(tmp.__str__())
                lines.append(line)
    with open(os.path.join(dst, 'summary_info_4_test.txt'), 'w+', encoding='utf-8') as wf:
        wf.writelines(lines)
    with open(os.path.join(dst, 'tts_4_auto_test.json'), 'w+', encoding='utf-8') as wf:
        json.dump(rst, wf, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # python3 /corpus/common/script-new/tts_audio_synthesis.py
    #   /corpus/project/matong    /corpus/project/matong/tts_test    speaker1&speaker2&...
    num = len(sys.argv)
    remote_path = r'\\192.168.1.8'
    project_dir = sys.argv[1] if num >= 2 else ''
    c_l = get_cmd_list(project_dir)
    op = sys.argv[2] if num >= 3 else os.path.dirname(__file__)
    # ================= tts语音合成 ==================
    if num >= 4:
        for spk in sys.argv[3].split('&'):
            synthesis_audio(c_l, op, speaker=spk)
    else:
        synthesis_all_spk_wav(c_l, op)

    flag = input(r'是否生成自动化测试所用的测试语料集[Y/N]:')
    if flag is not None and flag.lower() == 'y':
        # ================= 生成所有speaker的tts语音的测试语料集 ==================
        generate_auto_test_wav_file(remote_path, op)

        # ================= 生成指定speaker的tts语音的测试语料集 ==================
        # ================= 测试语料选中speaker修改变量: auto_test_spks ===========
        filter_4_auto_test(remote_path, op, project_dir)
