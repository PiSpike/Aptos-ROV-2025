# Activate Python environment
#source my_env/bin/activate

import socket
import pickle
import board
import adafruit_pca9685
from adafruit_servokit import ServoKit
import time

# Initialize socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5000))
s.listen(1)
print("Server is now running")
connection, client_address = s.accept()

# Initialize hardware components
i2c = board.I2C()
pca = adafruit_pca9685.PCA9685(i2c)

kit = ServoKit(channels=16)

pca.frequency = 50

# Motor and Servo configurations
motor_1 = 4
motor_2 = 6
motor_3 = 0
motor_4 = 2
motor_5 = 5
motor_6 = 3
motor_7 = 7
motor_8 = 1

claw_open = 15
claw_rotate = 14

# Define function to convert joystick inputs to PWM values
def convert(x):
    throttle_multiplier = 0.2  # Number between 0 and 1
    max_duty_cycle = 5240 + throttle_multiplier * 1640
    min_duty_cycle = 5240 - throttle_multiplier * 1640
    mapped_value = round((((x + 1) / 2) * (max_duty_cycle - min_duty_cycle)) + min_duty_cycle)
    return mapped_value

# Main server loop to receive and process data
while True:
    data = connection.recv(4096)

    if not data:
        break
    else:
        inputs = pickle.loads(data)
        print(inputs)
        pca.channels[motor_1].duty_cycle = convert(inputs[0])
        pca.channels[motor_2].duty_cycle = convert(inputs[1])
        pca.channels[motor_3].duty_cycle = convert(inputs[2])
        pca.channels[motor_4].duty_cycle = convert(inputs[3])