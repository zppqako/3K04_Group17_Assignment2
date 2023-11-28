import serial.tools.list_ports
import struct
from serial import Serial

# add default values for AA onwards

# this file is the one you spit data to send



frdm_port = "COM12"

Start = b'\x16'

# second bit

SYNC = b'\x22'

Fn_set = b'\x55'

ser = serial.Serial()
# ser.baudrate = 115200
# ser = serial.Serial('COM12', baudrate=115200)


def test():
    Start = b'\x16'

    # second bit

    SYNC = b'\x22'

    Fn_set = b'\x55'
    
    m_input = 4
    r_input = 100
    pw_input = 2
    aplitude_input = 100
    ref_period = 150
    #detect threshold
    threshold_input = 80 
    max_input = 150
    factor_input = 30
    
    mode = struct.pack("B", int(m_input))
    # rate = struct.pack("BB", 0, 1)
    rate = (r_input).to_bytes(2, byteorder='little')
    pw = (pw_input).to_bytes(2, byteorder='little')
    apl = (aplitude_input).to_bytes(2, byteorder='little')
    #ref period
    rp = (ref_period).to_bytes(2, byteorder='little')
    #comp_pwm threshold
    thre = (threshold_input).to_bytes(2, byteorder='little')
    max = (max_input).to_bytes(2, byteorder='little')
    factor = (factor_input).to_bytes(2, byteorder='little')
    
    
    signal_echo = Start + Fn_set + mode + rate+ pw + apl + rp+ thre + max + factor
    print("test: ", signal_echo)

    with serial.Serial(frdm_port, 115200) as pacemaker:
        print("Connect")
        pacemaker.write(signal_echo)

    
        
test()