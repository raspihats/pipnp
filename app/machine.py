from time import sleep
from flask_socketio import send
from .grbl import Grbl, RT_COMMANDS


class Machine(object):
    HEAD = {
        'n1': {'type': 'nozzle', 'offset': {'x': 0, 'y': 0}},
        'n2': {'type': 'nozzle', 'offset': {'x': 34, 'y': 0}},
        'c1': {'type': 'camera', 'offset': {'x': 0, 'y': 50}}
    }

    AXIS = {
        'x': {'limit': 400, 'speed': 25000, 'park': 5},
        'y': {'limit': 400, 'speed': 25000, 'park': 5},
        'z': {'limit': 90, 'speed': 25000, 'park': 45},
        'a': {'limit': 360, 'speed': 25000, 'park': 0},
        'b': {'limit': 360, 'speed': 25000, 'park': 0}
    }

    def __init__(self, logger=None):
        self.grbl = Grbl()
        self.logger = logger
        self.vacuum_pump = False

    def open(self):
        self.grbl.open("/dev/ttyAMA0")
        self.logger.info(self.grbl.exec("?"))

    def start_vacuum_pump(self):
        self.logger.info("starting vacuum pump...")
        self.grbl.exec("M3 S1000")

    def stop_vacuum_pump(self):
        self.logger.info("stopping vacuum pump...")
        self.grbl.exec("M5")

    @property
    def position(self):
        token = 'MPos:'
        response = self.grbl.exec("?")
        if token not in response:
            raise Exception()
        else:
            # <Idle|MPos:0.000,0.000,0.000,0.000,0.000|FS:0,0> ok
            coord = response.split(token)[1].split('|')[0].split(',')
            return {
                'x': -float(coord[0]),
                'y': -float(coord[1]),
                'z': -float(coord[2]),
                'a': -float(coord[3]),
                'b': -float(coord[4])
            }

    def home(self):
        self.grbl.exec("$H", timeout=20)
        self.grbl.exec("G1F25000")
        self.grbl.exec("G1Z-45")

    def park(self, data):
        g_code = "G1"
        temp = []
        for axis in self.AXIS.keys():
            if axis in data['axis']:
                temp.append(axis)
                g_code += "{}{}".format(axis.upper(), -self.AXIS[axis]['park'])
        feed_rate = data['speed'] * self.AXIS[temp[0]]['speed'] / 100
        g_code += "F{}".format(feed_rate)
        self.grbl.exec(g_code)

    def jog(self, step):
        c_position = self.position
        g_code = "G1"
        for axis in self.AXIS.keys():
            if axis in step:
                temp = c_position[axis] + step[axis]
                if 0 <= temp <= self.AXIS[axis]['limit']:
                    g_code += "{}{}".format(axis.upper(), -temp)
                else:
                    raise Exception("Jog requested step:{} exceeds limits on {} axis, current: {}, requested: {}, max: {}".format(
                        step[axis], axis, c_position[axis], temp, self.AXIS[axis]['limit']))
        feed_rate = step['speed'] * self.AXIS[axis]['speed'] / 100
        g_code += "F{}".format(feed_rate)
        self.grbl.exec(g_code)

    def move(self, id, coord):
        x = coord['x'] - self.HEAD[id]['offset']['x']
        y = coord['y'] - self.HEAD[id]['offset']['y']
        self.grbl.exec("G1X{}Y{}".format(-x, -y))

    def park_xy(self):
        self.move('n1', {'x': 5, 'y': 5})

    def park_z(self):
        self.move('n1', {'x': 5, 'y': 5})

    def pick(self, id, coord):
        self.move(id, coord)
        if 'n1' in id:
            self.grbl.exec("G1Z-85F1000")   # nozzle down
            self.grbl.exec("G4 P0.300")     # pause
            self.grbl.exec("M8")            # enable nozzle vacuum
            self.grbl.exec("G4 P0.300")     # pause
            self.grbl.exec("G1Z-45F25000")  # nozzle up
        if 'n2' in id:
            self.grbl.exec("G1Z-5F25000")
            self.grbl.exec("M7")
            self.grbl.exec("G1Z-45")

    def place(self, id, coord):
        self.move(id, coord)
        if 'n1' in id:
            self.grbl.exec("G1Z-85F1000")   # nozzle down
            self.grbl.exec("G4 P0.300")     # pause
            self.grbl.exec("M9")            # disable nozzle vacuum
            self.grbl.exec("G4 P0.300")     # pause
            self.grbl.exec("G1Z-45F25000")
        if 'n2' in id:
            self.grbl.exec("G1Z-5")
            self.grbl.exec("G1Z-45")

    def _determine_origin(self, job):
        origin = {'x': 0, 'y': 0}
        origins = [step for step in job['steps'] if step['type'] == 'origin']
        if len(origins) == 0:
            self.logger.warning(
                "Origin point not found in job '{}'. Using origin point {}".format(job['name'], origin))
        elif len(origins) >= 2:
            origin = {'x': origins[0]['x'], 'y': origins[0]['y']}
            self.logger.warning(
                "More than one origin point were found in job '{}'. Using origin point {}".format(job['name'], origin))
        else:
            origin = {'x': origins[0]['x'], 'y': origins[0]['y']}
            self.logger.info(
                "Using origin point {}".format(origin))
        return origin

    def _determine_fiducials(self, job):
        fiducials = [step for step in job['steps']
                     if step['type'] == 'fiducial']
        if len(fiducials) == 0:
            self.logger.warning(
                "No fiducials found in job '{}'.".format(job['name']))
        else:
            for fiducial in fiducials:
                self.logger.info(
                    "Using fiducial point {}".format(fiducial))
        return fiducial

    def run_job(self, name):
        self.logger.info("Starting job '{}'".format(name))
        job = {
            'name': name,
            # 'steps': get_job(name)
            'steps': []
        }

        origin = self._determine_origin(job)
        fiducials = self._determine_fiducials(job)

        try:
            # self.start_vacuum_pump()
            steps = [step for step in job['steps']
                     if step['type'] == 'component']
            for step in steps:
                # determine feeder
                # self.pick('n1', {'x': 10, 'y': 10})
                place_point = {'x': origin['x'] +
                               step['x'], 'y': origin['y'] + step['y']}
                # self.place('n1', place_point)
        finally:
            # self.stop_vacuum_pump()
            # self.move('n1', {'x': 5, 'y': 5})
            pass

    def close(self):
        self.grbl.close()


machine = Machine()
