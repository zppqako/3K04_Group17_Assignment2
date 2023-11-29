import serial.tools.list_ports
import struct
from serial import Serial
import time

# add default values for AA onwards

# this file is the one you spit data to send

frdm_port = "COM12"


ser = serial.Serial()

def input(lrl, url, amplitude, pw, rp, factor_input, threshold, mode):
    Start = b'\x16'
    print("here")
    # second bit

    SYNC = b'\x22'

    Fn_set = b'\x55'
    
    # offset = 2
    # m_input = 6
    # r_input = 60
    # pw_input = 2
    # aplitude_input = 100
    # ref_period = 150
    # #detect threshold
    # threshold_input = 80 
    # max_input = 150
    # factor_input = 30
    
    # mode = 5
    # lrl = 60
    # url = 150
    # amplitude = 80
    # pw = 2
    # rp = 150
    # factor_input = 10
    # threshold = 80
    
    
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
    # signal_echo = Start + SYNC + mode + rate + pw + apl + rp+ thre + max + factor
    
    print("test: ", signal_echo)

    with serial.Serial(frdm_port, 115200) as pacemaker:
        print("Connect")
        pacemaker.write(signal_echo)

    
# input()


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
        
        
        # print("reading")
        pacemaker.write(Signal_echo)
        # time.sleep(1)

        data = pacemaker.read(16)
        # print(data[0])
        # print("afer reading")
        # mode = struct.unpack("b", data[0])
        # print(mode)
        # rate = struct.unpack("B", data[1:2])
        # print(rate)
        ATR_signal = struct.unpack(">d", data[0:8])[0]
        # print(ATR_signal)
        VENT_signal = struct.unpack(">d", data[8:16])[0]

        # sig1 = ATR_signal
        # sig2 = VENT_signal
        
        print("finish reading")
        # return [sig1,sig2]
        return ATR_signal,VENT_signal
    

# input()
# receive()
# i = 0
# while i < 100:
#     print(receive())
#     i+=1
# print(result)
