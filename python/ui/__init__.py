# coding=utf-8
# pyqt5的bug,需要添加这段代码才能找到pyqt5.dll, 以及源码运行，环境变量增加项目根路径
import os
import sys

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))