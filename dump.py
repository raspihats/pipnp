import json
feeders = [
    {
        'name': 'SripFeeder 1',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '1206',
            'type': 'resistor',
            'value': '5.6K',
            'tolerance': '1%'
        }
    },
    {
        'name': 'SripFeeder 2',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'capacitor',
            'value': '10nF',
            'tolerance': '10%',
            'voltage': '50V'
        }
    },
    {
        'name': 'SripFeeder 3',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'resistor',
            'value': '24K',
            'tolerance': '1%'
        }
    },
    {
        'name': 'SripFeeder 4',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'resistor',
            'value': '18K',
            'tolerance': '1%'
        }
    },
    {
        'name': 'SripFeeder 5',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'resistor',
            'value': '47K',
            'tolerance': '1%'
        }
    },
    {
        'name': 'SripFeeder 6',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'capacitor',
            'value': '12pF',
            'tolerance': '5%',
            'voltage': '50V'
        }
    },
    {
        'name': 'SripFeeder 7',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'capacitor',
            'value': '1uF',
            'tolerance': '5%',
            'voltage': '50V'
        }
    },
    {
        'name': 'SripFeeder 8',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'capacitor',
            'value': '100nF',
            'tolerance': '5%',
            'voltage': '10V'
        }
    },
    {
        'name': 'SripFeeder 9',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': 'SOT23',
            'type': 'nmos',
            'value': 'BSS84'
        }
    },
    {
        'name': 'SripFeeder 10',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'resistor',
            'value': '680R',
            'tolerance': '5%'
        }
    },
    {
        'name': 'SripFeeder 11',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'resistor',
            'value': '10K',
            'tolerance': '1%'
        }
    },
    {
        'name': 'SripFeeder 12',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'led',
            'value': 'OSG050603'
        }
    },
    {
        'name': 'SripFeeder 13',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': 'SOT23',
            'type': 'transistor',
            'value': 'PDTC114ET'
        }
    },
    {
        'name': 'SripFeeder 14',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'resistor',
            'value': '0R',
            'tolerance': '1%'
        }
    },
    {
        'name': 'SripFeeder 15',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': '0603',
            'type': 'resistor',
            'value': '150R',
            'tolerance': '5%'
        }
    },
    {
        'name': 'SripFeeder 16',
        'type': 'strip',
        'point': {
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
        'remaining': 48,
        'component': {
            'package': 'SOD80',
            'type': 'diode',
            'value': 'LL4148',
            'tolerance': '5%'
        }
    },
]

with open('feeders.json', 'w') as outfile:
    json.dump(feeders, outfile)
