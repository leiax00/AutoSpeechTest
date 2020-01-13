# coding=utf-8
from serial.tools import list_ports


def get_com_devices():
    ports = list_ports.comports()
    return [port.device for port in ports]  # return ['COM2', 'COM3']
