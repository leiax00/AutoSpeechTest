# coding: utf-8
import datetime
import time

one_second = 1 * 1000
one_minute = 60 * one_second
one_hour = 60 * one_minute
one_day = 24 * one_hour
format_1 = "%Y-%m-%d %H:%M:%S"
format_2 = "%Y%m%d%H%M%S"
format_3 = "%y%m%d"
format_4 = "%Y-%m-%d %H:%M:%S.%f"


def parse_time(time_str, time_formatter=format_1):
    """
    获取时间字符串的毫秒值
    """
    return time.mktime(time.strptime(time_str, time_formatter)) * 1000


def format_time_4_log(time_long=None, time_formatter=format_4):
    """
    毫秒值时间格式化
    """
    if time_long is not None:
        return time.strftime(format_1, time.localtime(time_long / 1000)) + '.' + str(int(time_long % 1000))
    else:
        return datetime.datetime.now().strftime(time_formatter)


def format_time(time_long=None, time_formatter=format_1):
    """
    毫秒值时间格式化
    """
    t = time.localtime() if time_long is None else time.localtime(time_long / 1000)
    return time.strftime(time_formatter, t)


def cur_time_str(time_formatter="%Y-%m-%d %H:%M:%S"):
    return time.strftime(time_formatter, time.localtime())


def get_zero_today():
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    return time.mktime(zero_today.timetuple()) * one_second


def compare_time_by_ymd(time1, time2=get_zero_today()):
    """
    通过年月日，比较时间，是否是同一天
    :param time1: 秒值
    :param time2: 秒值
    :return:
    """
    return 0 <= time1 - time2 < one_day


if __name__ == '__main__':
    now1 = datetime.datetime.now()
    zeroToday = now1 - datetime.timedelta(hours=now1.hour, minutes=now1.minute, seconds=now1.second,
                                          microseconds=now1.microsecond)
    print(time.mktime(zeroToday.timetuple()) * one_second)
    print(zeroToday.timetuple())
    print(format_time(1578585600000.0))
    print(format_time())
