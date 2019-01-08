class Feeder(object):

    @staticmethod
    def loadConfig(config):
        feeders = []
        for f in config['feeders']:
            try:
                if f['type'] == 'strip':
                    feeder = StripFeeder(f)
                else:
                    raise Exception(
                        'Unsupported feeder type: {}'.format(f['type']))
                feeders.append(feeder)
            except:
                pass
        return feeders

    def __init__(self, config):
        self._config = config


class StripFeeder(Feeder):
    def __init__(self, config):
        super().__init__(config)
        self.count = self._config['size']

    @property
    def component(self):
        return self._config['component']

    @property
    def size(self):
        return self._config['size']

    def empty(self):
        return self.count == 0

    @property
    def pick_point(self):
        if self.empty():
            raise Exception('Feeder is empty!')
        x = self._config['x'] + \
            ((self.size - self.count) * self._config['increment'])
        return {
            'x': x,
            'y': self._config['y'],
            'z': self._config['z'],
        }

    def advance(self):
        if self.empty():
            raise Exception('Feeder is empty!')
        self.count -= 1
