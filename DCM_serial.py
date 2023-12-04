import serial.tools.list_ports
import struct
from serial import Serial


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


def receive():
    Start = b'\x16'
    SYNC = b'\x22'
    Fn_set = b'\x55'
    mode = struct.pack("B", int(0))
    Signal_echo = Start + SYNC


    i=0
    while(i<15):
        Signal_echo = Signal_echo + struct.pack("B", 0)
        i = i+1

    with serial.Serial(frdm_port, 115200, timeout=1) as pacemaker:
        pacemaker.reset_input_buffer()
        pacemaker.reset_output_buffer()
        pacemaker.write(Signal_echo)

        data = pacemaker.read(16)
        ATR_signal = struct.unpack(">d", data[0:8])[0]
        VENT_signal = struct.unpack(">d", data[8:16])[0]
        print("finish reading")
        return ATR_signal,VENT_signal
    

