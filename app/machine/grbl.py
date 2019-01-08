import threading
import time
import serial
from enum import Enum

ERROR_CODES = {
    "1": "G-code words consist of a letter and a value. Letter was not found.",
    "2": "Numeric value format is not valid or missing an expected value.",
    "3": "Grbl '$' system command was not recognized or supported.",
    "4": "Negative value received for an expected positive value.",
    "5": "Homing cycle is not enabled via settings.",
    "6": "Minimum step pulse time must be greater than 3usec.",
    "7": "EEPROM read failed. Reset and restored to default values.",
    "8": "Grbl '$' command cannot be used unless Grbl is IDLE. Ensures smooth operation during a job.",
    "9": "G-code locked out during alarm or jog state.",
    "10": "Soft limits cannot be enabled without homing also enabled.",
    "11": "Max characters per line exceeded. Line was not processed and executed.",
    "12": "(Compile Option) Grbl '$' setting value exceeds the maximum step rate supported.",
    "13": "Safety door detected as opened and door state initiated.",
    "14": "(Grbl-Mega Only) Build info or startup line exceeded EEPROM line length limit.",
    "15": "Jog target exceeds machine travel. Command ignored.",
    "16": "Jog command with no '=' or contains prohibited g-code.",
    "17": "Laser mode requires PWM output.",
    "20": "Unsupported or invalid g-code command found in block.",
    "21": "More than one g-code command from same modal group found in block.",
    "22": "Feed rate has not yet been set or is undefined.",
    "23": "G-code command in block requires an integer value.",
    "24": "Two G-code commands that both require the use of the XYZ axis words were detected in the block.",
    "25": "A G-code word was repeated in the block.",
    "26": "A G-code command implicitly or explicitly requires XYZ axis words in the block, but none were detected.",
    "27": "N line number value is not within the valid range of 1 - 9,999,999.",
    "28": "A G-code command was sent, but is missing some required P or L value words in the line.",
    "29": "Grbl supports six work coordinate systems G54-G59. G59.1, G59.2, and G59.3 are not supported.",
    "30": "The G53 G-code command requires either a G0 seek or G1 feed motion mode to be active. A different motion was active.",
    "31": "There are unused axis words in the block and G80 motion mode cancel is active.",
    "32": "A G2 or G3 arc was commanded but there are no XYZ axis words in the selected plane to trace the arc.",
    "33": "The motion command has an invalid target. G2, G3, and G38.2 generates this error, if the arc is impossible to generate or if the probe target is the current position.",
    "34": "A G2 or G3 arc, traced with the radius definition, had a mathematical error when computing the arc geometry. Try either breaking up the arc into semi-circles or quadrants, or redefine them with the arc offset definition.",
    "35": "A G2 or G3 arc, traced with the offset definition, is missing the IJK offset word in the selected plane to trace the arc.",
    "36": "There are unused, leftover G-code words that aren't used by any command in the block.",
    "37": "The G43.1 dynamic tool length offset command cannot apply an offset to an axis other than its configured axis. The Grbl default axis is the Z-axis."
}

ALARM_CODES = {
    "1": "Hard limit triggered. Machine position is likely lost due to sudden and immediate halt. Re-homing is highly recommended.",
    "2": "G-code motion target exceeds machine travel. Machine position safely retained. Alarm may be unlocked.",
    "3": "Reset while in motion. Grbl cannot guarantee position. Lost steps are likely. Re-homing is highly recommended.",
    "4": "Probe fail. The probe is not in the expected initial state before starting probe cycle, where G38.2 and G38.3 is not triggered and G38.4 and G38.5 is triggered.",
    "5": "Probe fail. Probe did not contact the workpiece within the programmed travel for G38.2 and G38.4.",
    "6": "Homing fail. Reset during active homing cycle.",
    "7": "Homing fail. Safety door was opened during active homing cycle.",
    "8": "Homing fail. Cycle failed to clear limit switch when pulling off. Try increasing pull-off setting or check wiring.",
    "9": "Homing fail. Could not find limit switch within search distance. Defined as 1.5 * max_travel on search and 5 * pulloff on locate phases."
}

STATUS_REPORT_START = '<'
STATUS_REPORT_END = '>'
TERMINATOR = "\r\n"


class RT_COMMANDS(Enum):
    TOGGLE_COOLANT_FLOOD = 0xA0
    TOGGLE_COOLANT_MIST = 0xA1


class Status(object):

    def __init__(self, report, axis):
        self.axis = axis
        if STATUS_REPORT_START in report \
                and STATUS_REPORT_END in report:
            start_index = report.index(STATUS_REPORT_START)
            end_index = report.index(STATUS_REPORT_END)
            fields = report[start_index + 1: end_index].split('|')
            self._parseFields(fields)
        else:
            raise Exception("Unable to parse status report: {}".format(report))

    def _parseFields(self, fields):
        self.state = fields[0]
        for field in fields:
            if field.startswith("MPos:"):
                self._parseMpos(field)
            # elif field.startswith("A:"):
            #     if 'F' in field:
            #         self._coolant_flood = True
            #     if 'M' in field:
            #         self._coolant_mist = True

    def _parseMpos(self, field):
        field = field.replace("MPos:", "")
        coord = [-float(x) for x in field.split(",")]
        mpos = {}
        i = 0
        for axis in self.axis:
            mpos[axis['name']] = coord[i]
            i += 1
        self.mpos = mpos


class Grbl(threading.Thread):
    def __init__(self):
        super().__init__()
        self._port = None
        self._running = False
        self._port_lock = threading.Lock()

        self._status_lock = threading.Lock()
        self._state = None
        self._position = None

        self._coolant_flood = False
        self._coolant_mist = False

    def open(self, config):
        self.config = config
        self._port = serial.Serial(
            port=self.config['port']['name'],
            baudrate=self.config['port']['baudrate'],
            bytesize=self.config['port']['bytesize'],
            parity=self.config['port']['parity'],
            stopbits=self.config['port']['stopbits']
        )

        # self.exec("M09")   # deactivate all coolant
        self._coolant_flood = False
        self._coolant_mist = False

        self._running = True
        self.start()

    def run(self):
        while self._running:
            time.sleep(0.1)
            status = None
            try:
                response = self.exec("?", timeout=0.5)
                status = Status(response, self.config['axis'])
            except:
                status = None
            finally:
                with self._status_lock:
                    if status is None:
                        self._state = None
                        self._position = None
                    else:
                        self._state = status.state
                        self._position = status.mpos

    def exec(self, command, expected="ok", timeout=5):
        with self._port_lock:
            # if '?' not in command:
            #     print(command)
            start_time = time.time()
            self._port.reset_input_buffer()
            self._port.write((command + '\n').encode())
            response = ""
            while(True):
                time.sleep(0.001)

                while self._port.in_waiting > 0:
                    response_bytes = self._port.read(self._port.in_waiting)
                    response += str(response_bytes, 'utf-8')

                if "ok" in response:
                    # print("Duration: {}".format(time.time() - start_time))
                    break
                elif "error" in response:
                    code = response.strip().replace("error:", "")
                    description = ERROR_CODES.get(
                        code, "No description for error code: {}".format(code))
                    raise Exception(
                        'Error\ncommand: {}\nresponse: {}({})'.format(command.strip(), response.strip(), description))

                if (time.time() - start_time) > timeout:
                    raise Exception(
                        'Timeout\ncommand: {}\nresponse: {}'.format(command.strip(), response.strip()))

            # print("grbl    command: {}    response {}".format(command, response))
            return response

    def exec_rt(self, command):
        with self._port_lock:
            self._port.write(command.value.to_bytes(1, 'big'))

    @property
    def state(self):
        with self._status_lock:
            return self._state

    @property
    def position(self):
        with self._status_lock:
            return self._position

    def home(self):
        self.exec("$H", timeout=20)

    def pause(self, interval):
        self.exec("G4P{}".format(interval))

    def move(self, coord, feed_rate):
        g_code = "G1"
        for axis in coord:
            g_code += "{}{}".format(axis, -coord[axis])
        g_code += "F{}".format(feed_rate)
        # print(g_code)
        self.exec(g_code)

    @property
    def spindle(self):
        pass

    @spindle.setter
    def spindle(self, value):
        if value:
            self.exec("M03S1000")   # cw
            # self.exec("M04S1000")   # ccw
        else:
            self.exec("M05")

    @property
    def coolant_flood(self):
        return self._coolant_flood

    @coolant_flood.setter
    def coolant_flood(self, value):
        if value != self._coolant_flood:
            if value:
                self.exec("M08")    # activate coolant flood
                self._coolant_flood = True
            else:
                if self._coolant_mist:
                    self.exec("M09")    # deactivate all coolant
                    self._coolant_flood = False
                    self._coolant_mist = False
                    self.exec("M07")    # re-activate coolant mist
                    self._coolant_mist = True

                else:
                    self.exec("M09")    # deactivate all coolant
                    self._coolant_flood = False

    @property
    def coolant_mist(self):
        return self._coolant_mist

    @coolant_mist.setter
    def coolant_mist(self, value):
        if value != self._coolant_mist:
            if value:
                self.exec("M07")    # activate coolant mist
                self._coolant_mist = True
            else:
                if self._coolant_flood:
                    self.exec("M09")    # deactivate all coolant
                    self._coolant_flood = False
                    self._coolant_mist = False
                    self.exec("M08")    # re-activate coolant flood
                    self._coolant_flood = True
                else:
                    self.exec("M09")    # deactivate all coolant
                    self._coolant_mist = False

    def close(self):
        self.spindle = False
        self.coolant_flood = False
        self.coolant_mist = False
        self._running = False
        if self._port is not None:
            self._port.close()             # close port
        if self.is_alive():
            self.join()
