# coding=utf-8
import os
import sys


def init_env():
    custom_paths = []
    # pyqt5的bug,需要添加这段代码才能找到pyqt5.dll
    if hasattr(sys, 'frozen'):
        os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

    base_path = os.getcwd()
    # 源码运行，环境变量增加项目根路径
    source_p = os.path.join(base_path, '..')
    custom_paths.append(source_p)

    # sox增加环境变量
    # sox_path = os.path.join(base_path, '..', 'res', 'sox-14-4-2')
    # custom_paths.append(sox_path)

    sys.path.extend(custom_paths)


if __name__ == '__main__':
    init_env()
    from ui.ast_ui import main

    main()
