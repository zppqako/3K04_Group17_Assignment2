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
    
    mode = struct.pack("B", 1)
    rate1 = struct.pack("B", 6)
    rate2= struct.pack("B", 0)
    # rate = bytearray(60)
    pulsewitdth = struct.pack("B", 3)
    
    #aplitude
    apl1 = struct.pack("B", 8)
    apl2= struct.pack("B", 0)
    
    #ref time
    ref1 = struct.pack("B", 15)
    ref2= struct.pack("B", 0)
    
    ref_factor1 = struct.pack("B", 2)
    ref_factor2 = struct.pack("B", 0)
    # pacing_ref_pwm = struct.pack("B", 100)
    signal_echo = Start + Fn_set + mode + rate1 + rate2 + pulsewitdth + apl1 + apl2 + ref1 + ref2 + ref_factor1 + ref_factor2

    print("test: ", signal_echo)

    with serial.Serial(frdm_port, 115200) as pacemaker:
        print("Connect")
        pacemaker.write(signal_echo)
        
test()