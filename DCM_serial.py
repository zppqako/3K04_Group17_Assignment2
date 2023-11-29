import serial.tools.list_ports
import struct
from serial import Serial
import time

# add default values for AA onwards

# this file is the one you spit data to send

frdm_port = "COM3"


ser = serial.Serial()

def input(lrl, url, amplitude, pw, rp, factor_input, threshold, mode):
    Start = b'\x16'
    print("here")
    # second bit

    SYNC = b'\x22'

    Fn_set = b'\x55'
    
    mode = struct.pack("B", int(mode))
    # rate = struct.pack("BB", 0, 1)
    rate = int(lrl*2).to_bytes(2, byteorder='little')
    max = int(url).to_bytes(2, byteorder='little')
    apl = int(amplitude).to_bytes(2, byteorder='little')
    pw = int(pw).to_bytes(2, byteorder='little')
    rp = int(rp).to_bytes(2, byteorder='little') #ref period
    factor = int(factor_input).to_bytes(2, byteorder='little')
    thre = int(threshold).to_bytes(2, byteorder='little') #comp_pwm threshold
    
    
    signal_echo = Start + Fn_set + mode + rate + pw + apl + rp+ thre + max + factor
    print("test: ", signal_echo)

    with serial.Serial(frdm_port, 115200) as pacemaker:
        print("Connect")
        pacemaker.write(signal_echo)



