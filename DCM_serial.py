import serial.tools.list_ports
import struct
from serial import Serial
import time

# add default values for AA onwards

# this file is the one you spit data to send



frdm_port = "COM12"

Start = b'\x16'

# second bit

SYNC = b'\x22'

Fn_set = b'\x55'

# ser = serial.Serial()
# ser.baudrate = 115200
# ser = serial.Serial('COM12', baudrate=115200)


# def input():
def input(lrl, url, aa, apw, arp, factor, threshold, mode):
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
    
    mode = struct.pack("B", int(mode))
    # rate = struct.pack("BB", 0, 1)
    rate = int(lrl*2).to_bytes(2, byteorder='little')
    max = int(url).to_bytes(2, byteorder='little')
    apl = int(aa).to_bytes(2, byteorder='little')
    pw = int(apw).to_bytes(2, byteorder='little')
    rp = int(arp).to_bytes(2, byteorder='little') #ref period
    factor = int(factor).to_bytes(2, byteorder='little')
    thre = int(threshold).to_bytes(2, byteorder='little') #comp_pwm threshold
    
    
    signal_echo = Start + Fn_set + mode + rate+ pw + apl + rp+ thre + max + factor
    print("test: ", signal_echo)

    with serial.Serial(frdm_port, 115200) as pacemaker:
        print("Connect")
        pacemaker.write(signal_echo)

# input()

# def receive():
#     Start = b'\x16'
#     SYNC = b'\x22'
#     Fn_set = b'\x55'
#     # Signal_echo = b'\x16\x22'# + b'\00' * 17
#     Signal_echo = Start + SYNC
#     # i=0
#     # while(i<72):
#     #     Signal_echo = Signal_echo + struct.pack("B", 0)
#     #     i = i+1

#     with serial.Serial(frdm_port, 115200) as pacemaker:
#         try:
#             print("reading")
#             pacemaker.write(Signal_echo)
#             time.sleep(0.1)
#             print("keep reading")
            
#             data = pacemaker.read(16)
#             print("afer reading")
#             ATR_signal = struct.unpack("d", data[0:8])[0]
#             VENT_signal = struct.unpack("d", data[8:16])[0]
            
#             print("finish reading")
#             return [ATR_signal,VENT_signal]
#         except Exception as e:
#             print("wrong")
    
# receive()

# print(result)

