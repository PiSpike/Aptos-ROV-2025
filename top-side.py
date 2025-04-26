import socket
import pickle
import pygame
import time

# Initialize socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.88.253", 5000))  # Change the IP address to the server's IP address

# Initialize Pygame and joystick
pygame.init()
pygame.joystick.init()

# Variables to control the main loop and joystick state
run = True
gotjoystick = False

# Initial claw angles
claw_angle = 50
claw_rotate = 90
syringe_angle = 90
camera_angle = 90

# Input array to store joystick inputs
input = [0] * 12
input[8] = claw_angle
input[9] = claw_rotate
input[10] = syringe_angle
input[11] = camera_angle
print(input)

def clamp(value):
    """Clamp a value between -1.0 and 1.0."""
    return max(-1.0, min(1.0, value))

def calculate_motor_pwm(forward_backward, left_right, yaw):
    """
    Calculate PWM values for four motors based on joystick input.
    """
    motor1_pwm = round(clamp(forward_backward - left_right - yaw), 3)
    motor2_pwm = round(clamp(forward_backward + left_right + yaw), 3)
    motor3_pwm = round(clamp(-forward_backward - left_right + yaw), 3)
    motor4_pwm = round(clamp(-forward_backward + left_right - yaw), 3)

    input[0] = motor1_pwm
    input[1] = motor2_pwm
    input[2] = motor3_pwm
    input[3] = motor4_pwm

    return {
        "motor1": motor1_pwm,
        "motor2": motor2_pwm,
        "motor3": motor3_pwm,
        "motor4": motor4_pwm,
    }

def calculate_lift(up_down, pitch, roll):
    """
    Calculate PWM values for lift motors based on joystick input.
    """
    motor5_pwm = round(clamp(up_down - roll), 3)
    motor6_pwm = round(clamp(up_down + roll), 3)
    motor7_pwm = round(clamp(up_down + pitch), 3)
    motor8_pwm = round(clamp(up_down - pitch), 3)

    input[4] = motor5_pwm
    input[5] = motor6_pwm
    input[6] = motor7_pwm
    input[7] = motor8_pwm

try:
    while run:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                gotjoystick = True
                print(joystick)

        if gotjoystick:
            # Initialize pitch and roll
            pitch = 0
            roll = 0

            # Check joystick buttons
            for button in range(17):
                pressed = joystick.get_button(button)
                if pressed:
                    if button == 9 and claw_angle <= 179:
                        claw_angle += 1
                    elif button == 8 and claw_angle >= 1:
                        claw_angle -= 1
                    if button == 11 and claw_rotate <= 179:
                        claw_rotate += 1
                    elif button == 10 and claw_rotate >= 1:
                        claw_rotate -= 1
                    if button == 4:
                        pitch = 1
                    elif button == 6:
                        pitch = -1
                    if button == 5:
                        roll = 1
                    elif button == 7:
                        roll = -1
                    if button == 14:
                        claw_angle = 65
                    if button == 13:
                        claw_angle = 100
                    if button == 12:
                        syringe_angle = 180
                    if button == 15:
                        syringe_angle = 0
                    if button == 1:
                        camera_angle = 0
                    if button == 2:
                        camera_angle = 180

                    input[8] = claw_angle
                    input[9] = claw_rotate
                    input[10] = syringe_angle
                    input[11] = camera_angle


            # Check joystick axes
            yaw_val = .5*joystick.get_axis(0)
            forward_backward = -joystick.get_axis(3)
            left_right = joystick.get_axis(2)
            up_down = joystick.get_axis(1)

            # Apply deadband to joystick input
            deadband = 0.05
            forward_backward = 0 if abs(forward_backward) < deadband else forward_backward
            left_right = 0 if abs(left_right) < deadband else left_right
            yaw_val = 0 if abs(yaw_val) < deadband else yaw_val
            up_down = 0 if abs(up_down) < deadband else up_down

            # Calculate motor speeds and lift
            motor_speeds = calculate_motor_pwm(forward_backward, left_right, yaw_val)
            calculate_lift(up_down, pitch, roll)
            print(input)

            # Send input data to the server
            data = pickle.dumps(input)
            s.send(data)
            time.sleep(0.02)

except KeyboardInterrupt:
    # Handle cleanup on exit
    print("\nCtrl + C pressed. Cleaning Up")
    joystick.quit()
    pygame.quit()
