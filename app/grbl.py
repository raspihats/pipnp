import serial
import time
from enum import Enum

TERMINATOR = "\r\n"


class RT_COMMANDS(Enum):
    TOGGLE_COOLANT_FLOOD = 0xA0
    TOGGLE_COOLANT_MIST = 0xA1


class Grbl(object):
    def __init__(self):
        self.port = None

    def open(self, port, baudrate=115200, bytesize=8, parity='N', stopbits=1):
        self.port = serial.Serial(
            port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits)

    def close(self):
        if self.port is not None:
            self.port.close()             # close port

    def exec(self, command, expected="ok", timeout=3):
        start_time = time.time()
        self.port.reset_input_buffer()
        self.port.write((command + '\n').encode())
        response = ""
        while(True):
            time.sleep(0.001)

            while self.port.in_waiting > 0:
                response_bytes = self.port.read(self.port.in_waiting)
                response += str(response_bytes, 'utf-8')

            if "ok" in response:
                # print("Duration: {}".format(time.time() - start_time))
                break

            if (time.time() - start_time) > timeout:
                raise Exception(
                    'Timeout\ncommand: {}\nresponse: {}'.format(command, response))

        return response

    def exec_rt(self, command):
        self.port.write(command.value.to_bytes(1, 'big'))
