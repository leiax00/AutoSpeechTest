# coding=utf-8
import json
import re
from json import JSONEncoder


class AudioObj:
    def __init__(self, d=None):
        self.aid = ''
        self.content = ''
        self.source = ''
        if d is not None:
            self.__dict__ = d

    def set_v(self, aid=None, content=None, source=None):
        self.aid = aid
        self.content = content
        self.source = source
        return self

    def __str__(self):
        return self.__dict__.__str__()

    def __eq__(self, other):
        return self.aid == other.aid

    def __format__(self, format_spec):
        if format_spec is not None and format_spec != '':
            return format_spec.format(self)
        return self.__str__()


class DefaultDecoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, AudioObj):
            return o.__str__()


class LogParse:
    def __init__(self, log_path, play_wp):
        self.play_wp = play_wp
        self.play_wd = {}
        self.log_path = log_path
        self.log_info = {}
        self.crst = {}
        self.load_play_wav()

    def parse_log(self):
        with open(self.log_path, 'r', encoding='utf-8') as rf:
            for line in rf:
                re_str = r'cmd_info: (.*):(.*) -> log: (.*)'
                rst = re.match(re_str, line)
                if rst is not None:
                    play_cmd = rst.group(1)
                    wav_name = rst.group(2)
                    log_info = rst.group(3)
                    logs = log_info.split(' && ')
                    rc_list = []
                    for log in logs:
                        log_re_str = r'.*decode result is ([^ ]*) ([\d.-]*):[^ ]* ([\d.-]*):[^ ]* ([\d.-]*):[^ ]*'
                        log_rst = re.match(log_re_str, log)
                        if log_rst is not None:
                            rc_list.append(log_rst.group(1))
                    if play_cmd not in rc_list:
                        self.crst[play_cmd] = self.crst.get(play_cmd) or []
                        if self.play_wd.get(wav_name) not in self.crst[play_cmd]:
                            self.crst[play_cmd].append(self.play_wd.get(wav_name))

    def write_no_match_wav(self):
        with open('bad_wav.json', 'w+', encoding='utf-8') as wf:
            json.dump(self.crst, wf, cls=DefaultDecoder, indent=4, ensure_ascii=False)

    def load_play_wav(self):
        with open(self.play_wp, 'r', encoding='utf-8') as rf:
            tmp = json.load(rf)
            for k, vs in tmp.items():
                for v in vs:
                    obj = json.loads(json.dumps(eval(v)), object_hook=AudioObj)
                    self.play_wd[obj.aid] = obj

    def filter_not_match_wav(self):
        pass

    def process(self):
        self.parse_log()
        self.write_no_match_wav()


if __name__ == '__main__':
    wp = r'D:\code\myTools\python\lehua_matong_tts_10.json'
    lp = r'C:\Users\Administrator\Desktop\tmp\matong_0207_tdnnf_white_test_log.log'
    LogParse(lp, wp).parse_log()
