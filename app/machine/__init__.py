import threading
from .grbl import Grbl
from .feeder import Feeder

DEFAULT_CONFIG = {
    'port': {
        'name': '/dev/ttyAMA0',
        'baudrate': 115200,
        'bytesize': 8,
        'parity': 'N',
        'stopbits': 1
    },
    'axis': [
        {
            'name': 'x',
            'limit': 450,
            'feed_rate': 25000,
            'acc': 600,
            'park': 5
        },
        {
            'name': 'y',
            'limit': 400,
            'feed_rate': 25000,
            'acc': 600,
            'park': 5
        },
        {
            'name': 'z',
            'limit': 120,
            'feed_rate': 25000,
            'acc': 600,
            'park': 59
        },
        {
            'name': 'a',
            'limit': 360,
            'feed_rate': 100,
            'acc': 100,
            'park': 0
        },
        {
            'name': 'b',
            'limit': 360,
            'feed_rate': 100,
            'acc': 100,
            'park': 0
        }
    ],
    'spindle': {
        'rpm': {
            'min': 0,
            'max': 10000
        }
    },
    'head': {
        'n1': {'type': 'nozzle', 'offset': {'x': 0, 'y': 0}},
        'n2': {'type': 'nozzle', 'offset': {'x': 34, 'y': 0}},
        'c1': {'type': 'camera', 'offset': {'x': 0, 'y': 50}}
    },
    'feeders': [
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '1206',
                'type': 'resistor',
                'value': '5.6K',
                'tolerance': '1%'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'end_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'capacitor',
                'value': '10nF',
                'tolerance': '10%',
                'voltage': 50
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'resistor',
                'value': '24K',
                'tolerance': '1%'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'resistor',
                'value': '18K',
                'tolerance': '1%'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'resistor',
                'value': '47K',
                'tolerance': '1%'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'end_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'capacitor',
                'value': '12pF',
                'tolerance': '5%',
                'voltage': 50
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'end_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'capacitor',
                'value': '1uF',
                'tolerance': '5%',
                'voltage': 50
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'end_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'capacitor',
                'value': '100nF',
                'tolerance': '5%',
                'voltage': 10
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'end_point': {
                'x': 39.000,
                'y': 136.500,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': 'sot23',
                'type': 'nmos',
                'value': 'BSS84'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'resistor',
                'value': '680R',
                'tolerance': '5%'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'resistor',
                'value': '10K',
                'tolerance': '1%'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'led',
                'value': 'OSG050603'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': 'sot23',
                'type': 'transistor',
                'value': 'PDTC114ET'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'resistor',
                'value': '0R',
                'tolerance': '1%'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'resistor',
                'value': '150R',
                'tolerance': '5%'
            }
        },
        {
            'type': 'strip',
            'start_point': {
                'x': 225.000,
                'y': 139.400,
                'z': 23,
            },
            'end_point': {
                'x': 37.925,
                'y': 141.600,
                'z': 23,
            },
            'increment': 3.98,
            'size': 48,
            'component': {
                'package': '0603',
                'type': 'diode',
                'value': 'LL4148',
                'tolerance': '5%'
            }
        },
    ]

}


class Machine(threading.Thread):

    def __init__(self, logger=None):
        super().__init__()
        self.grbl = Grbl()
        self.logger = logger
        self.vacuum_pump = False
        self._job = None
        self._stop_job = False
        self._job_lock = threading.Lock()
        self._running = True
        self.start()

    def open(self, config=DEFAULT_CONFIG):
        self.config = config
        self.grbl.open(config)
        self.home()

    def start_vacuum_pump(self):
        self.logger.info("starting vacuum pump...")
        self.grbl.spindle = True

    def stop_vacuum_pump(self):
        self.logger.info("stopping vacuum pump...")
        self.grbl.spindle = False

    @property
    def position(self):
        return self.grbl.position

    def home(self):
        self.grbl.home()
        self.park('z')
        self.park('xy')
        self.park('ab')

    def park(self, axis_names, speed_factor=1):
        coord = {}
        min_feed_rate = None
        for axis in self.config['axis']:
            axis_name = axis['name']
            if axis_name in axis_names and 'park' in axis:
                coord[axis_name] = axis['park']
                if min_feed_rate is None or axis['feed_rate'] < min_feed_rate:
                    min_feed_rate = axis['feed_rate']

        feed_rate = speed_factor * min_feed_rate
        self.grbl.move(coord, feed_rate)

    def jog(self, step):
        c_position = self.position
        for axis in self.config['axis']:
            axis_name = axis['name']
            if axis_name in step:
                temp = c_position[axis_name] + step[axis_name]
                if 0 <= temp <= axis['limit']:
                    feed_rate = step['speed_factor'] * axis['feed_rate']
                    self.grbl.move({axis_name: temp}, feed_rate)
                else:
                    raise Exception("Jog requested step:{} exceeds limits on {} axis, current: {}, requested: {}, max: {}".format(
                        step[axis_name], axis_name, c_position[axis_name], temp, axis['limit']))

    def move(self, id, coord):
        x = coord['x'] - self.config['head'][id]['offset']['x']
        y = coord['y'] - self.config['head'][id]['offset']['y']
        self.grbl.move({'x': x, 'y': y}, self.config['axis'][0]['feed_rate'])
        if 'n1' in id and 'a' in coord:
            self.grbl.move({'a': coord['a'], },
                           self.config['axis'][3]['feed_rate'])

    def move_xy(self, id, coord):
        x = coord['x'] - self.config['head'][id]['offset']['x']
        y = coord['y'] - self.config['head'][id]['offset']['y']
        self.grbl.move({'x': x, 'y': y}, self.config['axis'][0]['feed_rate'])

    def move_z(self, id, coord):
        z = coord['z'] + 5
        self.grbl.move({'z': z}, self.config['axis'][2]['feed_rate'])
        z = coord['z']
        self.grbl.move({'z': z}, self.config['axis'][2]['feed_rate'])

    def rotate_ab(self, id, coord):
        if 'n1' in id:
            self.grbl.move({'a': coord['a']},
                           self.config['axis'][3]['feed_rate'])
        if 'n2' in id:
            self.grbl.move({'b': coord['b']},
                           self.config['axis'][4]['feed_rate'])

    def pick(self, id, coord):
        self.move_xy(id, coord)
        if 'n1' in id:
            self.move_z(id, coord)            # nozzle down
            self.grbl.pause(0.500)            # pause
            self.grbl.coolant_mist = True    # enable nozzle vacuum
            self.grbl.pause(0.500)            # pause
            self.park('z')                    # nozzle up

    def place(self, id, coord):
        self.move_xy(id, coord)
        if 'n1' in id:
            self.rotate_ab(id, coord)         # nozzle rotate
            self.move_z(id, coord)            # nozzle down
            self.grbl.pause(0.500)            # pause
            self.grbl.coolant_mist = False   # enable nozzle vacuum
            self.grbl.pause(0.500)            # pause
            self.park('z')                    # nozzle up
            self.park('a')                    # nozzle rotate

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

    def run(self):
        import time
        # print('th running ' + str(threading.get_ident()))

        while self._running:
            with self._job_lock:
                if self._job is not None:
                    self._run_job()
            time.sleep(0.1)
            # print('th ' + str(threading.get_ident()))
        # print('th stopped ' + str(threading.get_ident()))

    def _run_job(self):
        self.logger.info("Starting job '{}'".format(self._job['name']))

        feeders = Feeder.loadConfig(self.config)

        self.rotate_ab('n1', {'a': 360})
        self.park('a')

        origin = self._determine_origin(self._job)
        fiducials = self._determine_fiducials(self._job)

        try:
            self.start_vacuum_pump()
            steps = [step for step in self._job['steps']
                     if step['type'] == 'component']
            for step in steps:
                # determine feeder
                feeder = feeders[0]
                self.park('ab')
                self.pick('n1', feeder.pick_point)
                print(feeder.pick_point)
                feeder.advance()

                place_point = {
                    'x': origin['x'] + step['x'],
                    'y': origin['y'] + step['y'],
                    'z': 10,
                    'a': step['angle']
                }
                self.place('n1', place_point)

                if self._stop_job:
                    self.logger.info(
                        "Stopping job '{}'".format(self._job['name']))
                    self._stop_job = False
                    self._job = None
                    return

            self.logger.info(
                "Job '{}' completed.".format(self._job['name']))
            self._job = None
        finally:
            self.stop_vacuum_pump()
            # self.move('n1', {'x': 5, 'y': 5})
            self.park('z')
            self.park('xy')
            self.park('ab')

    def start_job(self, job):
        with self._job_lock:
            if self._job is None:
                self._stop_job = False
                self._job = job
            else:
                raise Exception(
                    "Job {} is in progress".format(self._job['name']))

    def stop_job(self):
        self._stop_job = True

    def close(self):
        self._stop_job = True
        self._running = False
        if self.is_alive():
            self.join()
        self.grbl.close()


machine = Machine()
