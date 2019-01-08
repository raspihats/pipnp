from app.grbl import Grbl
import logging
import time


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():

    grbl = Grbl()
    try:
        grbl.open()
        grbl.exec("$H", timeout=20)
        grbl.exec("G1F25000")
        grbl.exec("G1Z-45")
        # grbl.spindle = True
        # time.sleep(3)
        # grbl.coolant_flood = True
        # time.sleep(3)
        # grbl.coolant_mist = True
        # time.sleep(10)
        # grbl.coolant_mist = False
        # time.sleep(10)
        i = 0
        while i < 30:
            time.sleep(0.1)
            print(grbl.state)
            print(grbl.position)
            i += 1
    except Exception as e:
        print(e)
    finally:
        grbl.close()


if __name__ == '__main__':
    main()
