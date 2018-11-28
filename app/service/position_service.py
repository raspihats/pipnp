from ..machine import machine


def get_position():
    return machine.position


def set_position(position):
    machine.move('n1', position)
