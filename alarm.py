import serial
import time


class Alarm(object):
    def __init__(self):
        self.__port = serial.Serial("/dev/ttyUSB0", baudrate=9600)

    def __del__(self):
        self.__port.close()

    def arm(self):
        self.__port.write(b'51')
        time.sleep(0.5)
        self.__port.write(b'50')
        return 'ARMING!'

    def disarm(self):
        self.__port.write(b'41')
        time.sleep(0.5)
        self.__port.write(b'40')
        return 'Disarming!'


if __name__ == '__main__':
    s = Alarm()
    time.sleep(4)
    s.disarm()
    del s
