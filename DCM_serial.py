# import serial

import serial.tools.list_ports

import struct

from serial import Serial

# add default values for AA onwards

# this file is the one you spit data to send

frdm_port = "COM10"

Start = b'\x16'

# second bit

SYNC = b'\x22'

Fn_set = b'\x55'


def test():
    Start = b'\x16'

    # second bit

    SYNC = b'\x22'

    Fn_set = b'\x55'

    mode = struct.pack("B", 0)

    signal_echo = Start + Fn_set + mode

    print("test: ", signal_echo)

    with serial.Serial(frdm_port, 115200) as pacemaker:
        pacemaker.write(signal_echo)