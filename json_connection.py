import serial
import time
import json

# Define serial port and baud rate
serial_port = "COM10"  # Replace with the actual port name
baud_rate = 115200

# Open serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def send_data(data):
    ser.write(data.encode())

def receive_data():
    return ser.readline().decode().strip()

def set_programmable_parameters(parameters):
    command = f"SET_PARAMETERS {json.dumps(parameters)}"
    send_data(command)
    response = receive_data()
    if response == "PARAMETERS_SET_SUCCESS":
        print("Parameters set successfully.")
    else:
        print("Failed to set parameters.")

def get_programmable_parameters():
    send_data("GET_PARAMETERS")
    response = receive_data()
    return response

# Example parameters (adjust based on your requirements)
example_parameters = {"RATE": 60, "MODE": 2}

# Set programmable parameters
set_programmable_parameters(example_parameters)

# Wait for a moment (simulating some time passing)
time.sleep(1)

# Get and verify programmable parameters
received_parameters = get_programmable_parameters()

# Parse the received JSON string in your Simulink model
parsed_parameters = json.loads(received_parameters)

# Assign individual parameters to Simulink variables
rate_variable = parsed_parameters["RATE"]
mode_variable = parsed_parameters["MODE"]

# Use rate_variable and mode_variable in your Simulink model
print("Rate:", rate_variable)
print("Mode:", mode_variable)

# Close serial connection
ser.close()
