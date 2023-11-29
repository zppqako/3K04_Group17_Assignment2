import serial.tools.list_ports
import struct
from serial import Serial

# add default values for AA onwards

# this file is the one you spit data to send



frdm_port = "COM12"

ser = serial.Serial()
# ser.baudrate = 115200
# ser = serial.Serial('COM12', baudrate=115200)



def serial(lrl, url, aa, apw, arp, factor, threshold, mode):
    Start = b'\x16'

    # second bit

    SYNC = b'\x22'

    Fn_set = b'\x55'
    
    mode = struct.pack("B", int(mode))
    # rate = struct.pack("BB", 0, 1)
    rate = (lrl*2).to_bytes(2, byteorder='little')
    max = (url).to_bytes(2, byteorder='little')
    apl = (aa).to_bytes(2, byteorder='little')
    pw = (apw).to_bytes(2, byteorder='little')
    rp = (arp).to_bytes(2, byteorder='little') #ref period
    factor = (factor).to_bytes(2, byteorder='little')
    thre = (threshold).to_bytes(2, byteorder='little') #comp_pwm threshold
    
    
    signal_echo = Start + Fn_set + mode + rate + pw + apl + rp+ thre + max + factor
    print("test: ", signal_echo)

    with serial.Serial(frdm_port, 115200) as pacemaker:
        print("Connect")
        pacemaker.write(signal_echo)

    
