# coding=utf-8
"""
脚本用于语音合成，并进行拆分
"""
import json
import os
import sys
import urllib

import requests
from pydub import AudioSegment
from pydub.silence import split_on_silence

url_template = 'http://yyapi.bilianshu.com/api?type=a&text={0}&speaker={1}' \
               '&speed=0&token=kFjRSxdPnBFV5gbPxkjjpxCjO3DuclRB'


def synthesis_audio(cmd_l, output_path=os.path.dirname(__file__), speaker='Siqi', cmd_count_of_one_req=5):
    """
    :param output_path: 输出路径
    :param cmd_count_of_one_req: 一次请求的命令词数量
    :param speaker:
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
        req_url = url_template.format(text, speaker)
        resp = requests.get(req_url)
        remaining_times = json.loads(json.dumps(dict(resp.headers))).get('Total-count')
        if int(remaining_times) <= 1000:
            print('*' * 30, '\nremaining_times is not enough, times:{0}, url:{1}'.format(remaining_times, req_url),
                  '*' * 30)
        output_file = os.path.join(output_path, '{0}_{1}.wav'.format(speaker.lower(), i + 1))
        urllib.request.urlretrieve(req_url, output_file)
        split_wav(tmp, output_file, speaker, i * cmd_count_of_one_req)


def split_wav(cmd_words, wav_file, speaker, index):
    wav_root_dir = os.path.join(os.path.dirname(wav_file), '..', 'wav')
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
            wav_p = os.path.join(wav_root_dir, '{0}_{1}.wav'.format(speaker.lower(), cmd_words[i]))
            new.export(wav_p, format='wav')
            with open(wav_p.replace('.wav', '.txt'), 'w+', encoding='utf-8') as wf:
                wf.write(cmd_words[i])
            wfs.write('{0}\t{1}\n'.format(cmd_words[i], wav_p))
            wfs.flush()


def get_cmd_list(fp):
    with open(fp, 'r+', encoding='utf-8') as rf:
        lines = rf.readlines()
    return [line.strip('\r\t\n') for line in lines]


if __name__ == '__main__':
    # python3 /corpus/common/script-new/tts_audio_synthesis_4_corpus.py /corpus/project/matong/corpus.txt /corpus/project/matong/tts_test speaker1&speaker2&....
    num = len(sys.argv)
    file_path = sys.argv[1] if num >= 2 else ''
    op = sys.argv[2] if num >= 3 else os.path.dirname(__file__)
    spk_l = sys.argv[3].split('&') if num >= 4 else ['Xiaoyun', 'Siqi', 'Amei', 'Aixia', 'Xiaogang', 'Xiaowei',
                                                     'Aicheng', 'Aida', 'Sitong', 'Aitong']
    c_l = get_cmd_list(file_path)
    for spk in spk_l:
        synthesis_audio(c_l, op, speaker=spk)
