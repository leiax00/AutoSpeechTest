# coding=utf-8
import paramiko

from conf.config import corpus_conf


def ssh_exec(cmd=None):
    try:
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname=corpus_conf.remote_host, port=corpus_conf.remote_port,
                  username=corpus_conf.remote_username,
                  password=corpus_conf.remote_password)
        if cmd is None:
            cmd = corpus_conf.retrieve_script
        res = c.exec_command(cmd)
        symbol = res[1].read().decode().strip('\r\n\t')
        if symbol != 'finish':
            return
    finally:
        c.close()
