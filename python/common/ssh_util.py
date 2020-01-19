# coding=utf-8
import paramiko

from conf.config import corpus_conf


def ssh_exec(cmd=None):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        c.connect(hostname=corpus_conf.remote_host, port=corpus_conf.remote_port,
                  username=corpus_conf.remote_username,
                  password=corpus_conf.remote_password)
        if cmd is None:
            cmd = corpus_conf.retrieve_script
        res = c.exec_command(cmd)
        symbol = res[1].read().decode().strip('\r\n\t')
        if 'finish' not in symbol:
            print(symbol)
            return False
        return True
    finally:
        c.close()


if __name__ == '__main__':
    corpus_conf.remote_host = '192.168.1.8'
    corpus_conf.remote_port = 22
    corpus_conf.remote_username = 'root'
    corpus_conf.remote_password = 'root'
    corpus_conf.retrieve_script = 'python3 /corpus/common/script-new/retrieve_wav.py /corpus/train/wavs A /corpus/project/matong/res/config.json'
    print(ssh_exec())
