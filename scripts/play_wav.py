# coding=utf-8
import datetime
import json
import os
import shutil
import time
import traceback
import wave
from time import sleep

import pyaudio
import sox


class _Player:
    def __init__(self):
        self.transformer = sox.Transformer()
        self.root = os.path.dirname(__file__)

    def play_wav(self, wav_name, need_voice_same=False):
        if need_voice_same:
            tmp_file_path = self.deal_voice(wav_name)
        else:
            tmp_file_path = shutil.copy(wav_name, self.root)
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

    def deal_voice(self, filename):
        dst_f = os.path.join(self.root, os.path.basename(filename))
        try:
            v_adjustment = float(self.transformer.stat(filename).get('Volume adjustment')) or 1.0
            print('voice increment:{0}, wav_path:{1}'.format(v_adjustment, filename))
            self.transformer.vol(v_adjustment)
            self.transformer.build(filename, dst_f)
            self.transformer.clear_effects()
            return dst_f
        except Exception as e:
            print('Failed to adjust volume, use origin wav. err: {0}, {1}'.format(e, traceback.format_exc()))
            if os.path.exists(dst_f):
                os.remove(dst_f)
            return shutil.copy(filename, self.root)


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
    # default_input = r'D:\code\AutoSpeechTest\scripts\bad_wav.json'
    default_input = r'\\192.168.1.8\corpus\project\modan_gtj\tts_test\tts_4_auto_test.json'
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
                player.play_wav(wav_p, True)
                print(format_time_4_log(), ' play end, aid:{0}'.format(aid))
                sleep(2)
                print('*' * 10, ' next ', '*' * 10)
                print('\n' * 1)
