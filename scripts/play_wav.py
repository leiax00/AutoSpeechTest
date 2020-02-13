# coding=utf-8
import datetime
import json
import os
import shutil
import time
import wave
from time import sleep

import numpy as np
import pyaudio
from scipy.io import wavfile


class _Player:
    def play_wav(self, wav_name, voice_same=False):
        if voice_same:
            tmp_file_path = self.deal_voice(wav_name)
        else:
            tmp_file_path = shutil.copy(wav_name, os.path.dirname(__file__))
        chunk = 1024
        p = pyaudio.PyAudio()
        wf = wave.open(tmp_file_path, 'rb')
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(chunk)
        while data != b'':
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()
        os.remove(tmp_file_path)

    @staticmethod
    def deal_voice(filename):
        dst_f = os.path.join(os.path.dirname(__file__), os.path.basename(filename))
        wav_l = list(wavfile.read(filename))
        normal_waves = np.array(wav_l[1] / np.max(wav_l[1]) * 32768, dtype=np.int16)
        wavfile.write(dst_f, wav_l[0], normal_waves)
        return dst_f


def read_json(p):
    with open(p, 'r', encoding='utf-8') as rf:
        return json.load(rf)


def format_time_4_log(time_long=None, time_formatter="%Y-%m-%d %H:%M:%S.%f"):
    """
    毫秒值时间格式化
    """
    if time_long is not None:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_long / 1000)) + '.' + str(int(time_long % 1000))
    else:
        return datetime.datetime.now().strftime(time_formatter)


def collect_log(com):
    while True:
        try:
            info = com.readline().decode(encoding='utf-8').strip('\r\n\t')
            if info != '':
                print('{0} {1}'.format(format_time_4_log(), info))
        finally:
            sleep(.001)


if __name__ == '__main__':
    player = _Player()
    default_input = r'\\U9wcu7c53reyco7\f\dev\tools\AutoTestTool\res\mt_penqiangyidang.json'
    print('请输入自动化测试结构的wav信息json文件, 不输入请修改py文件中的default_input的值。')
    in_p = input('json filepath:')
    if in_p is None or in_p == '':
        in_p = default_input
    if in_p is not None or in_p != '':
        for cmd_str, cmd_os in read_json(in_p).items():
            for cmd_o in cmd_os:
                cmd_o = json.loads(json.dumps(eval(cmd_o)))
                aid = cmd_o.get('aid')
                content = cmd_o.get('content')
                wav_p = cmd_o.get('source')
                print(format_time_4_log(), ' start paly:aid:{0}, content:{1}, source:{2}'.format(aid, content, wav_p))
                player.play_wav(wav_p)
                print(format_time_4_log(), ' play end, aid:{0}'.format(aid))
                sleep(2)
                print('*' * 10, ' next ', '*' * 10)
                print('\n' * 1)
