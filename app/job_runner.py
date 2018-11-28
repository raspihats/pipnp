from Queue import Queue
from threading import Thread
from time import sleep
from machine import Machine

machine = Machine()


class JobRunner(Thread):

    def __init__(self):
        super(JobRunner, self).__init__()
        self.running = True
        self.queue = Queue()

    def _execute_command(self, job):
        if 'home' in job['operation']:
            machine.home()
        if 'move' in job['operation']:
            machine.move(job['id'], {
                'x': job['x'], 'y': job['y']})
        if 'pick' in job['operation']:
            machine.pick(job['id'], {
                'x': job['x'], 'y': job['y']})
        if 'place' in job['operation']:
            machine.place(job['id'], {
                'x': job['x'], 'y': job['y']})

    def run(self):
        while self.running:
            if self.queue.empty():
                sleep(0.05)
            else:
                job = self.queue.get()
                self._execute_command(job)

    def stop(self):
        self.running = False
        self.join()
