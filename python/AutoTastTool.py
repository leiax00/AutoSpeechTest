# coding=utf-8
import os
import sys

if __name__ == '__main__':
    # pyqt5的bug,需要添加这段代码才能找到pyqt5.dll, 以及源码运行，环境变量增加项目根路径
    if hasattr(sys, 'frozen'):
        os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from ui.aca_main import main

    main()
