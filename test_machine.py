from app.machine import machine
import logging


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    # offset = {'x': 95.8, 'y': 23.5}

    # components = """LD1,47.47,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD2,48.97,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD3,50.48,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD4,51.99,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD5,53.50,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD6,55.01,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD7,56.52,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD8,58.02,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD9,65.09,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD10,66.60,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD11,68.10,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD12,69.61,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD13,71.12,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD14,72.63,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD15,74.14,3.97,180,OSG50603C1E,CHIPLED_0603
    #   LD16,75.64,3.97,180,OSG50603C1E,CHIPLED_0603"""

    # job = []
    # lines = components.split('\n')
    # for line in lines:
    #     data = line.split(',')
    #     job.append({'name': data[0], 'x': float(data[1]), 'y': float(data[2])})

    try:
        machine.logger = logger
        machine.open()
        machine.home()
        machine.run_job("DI16ac-top")
    finally:
        machine.close()


if __name__ == '__main__':
    main()
