# coding=utf-8


class RealMonitor:
    format_str = '''
  播放进度：{d.cur_num} / {d.total_num}
  已播时长：{d.duration}
  播放内容：{d.play_content}
  识别内容：{d.distinguish_content}
实时准确率: {d.accuracy}
'''

    def __init__(self):
        self.cur_num = 0
        self.total_num = 0
        self.duration = 0
        self.play_content = ''
        self.distinguish_content = ''
        self.accuracy = 1

    def __format__(self, format_spec=None):
        return self.format_str.format(d=self)


if __name__ == '__main__':
    m = RealMonitor()
    m.total_num = 100
    print(format(m))
