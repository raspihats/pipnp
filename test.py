import serial
import time


def send(port, command, timeout=10):
    start_time = time.time()
    port.reset_input_buffer()
    port.write((command + '\n').encode())
    response = ""
    while(True):
        time.sleep(0.001)

        while port.in_waiting > 0:
            response_bytes = port.read(port.in_waiting)
            response += str(response_bytes, 'utf-8')

        if "ok" in response:
            print("Duration: {}".format(time.time() - start_time))
            break

        if (time.time() - start_time) > timeout:
            raise Exception(
                'Timeout\ncommand: {}\nresponse: {}'.format(command, response))

    return response


def main():
    port = None
    try:
        port = serial.Serial(
            port="/dev/ttyAMA0", baudrate=115200, bytesize=8, parity='N', stopbits=1)
        response = send(port, "?")
        print(response)
    finally:
        if port is not None:
            port.close()


if __name__ == '__main__':
    main()
