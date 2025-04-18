# Joystick Controlled Raspberry Pi Robot/Device

This project allows you to control motors and servos connected to a Raspberry Pi using a joystick connected to a Windows PC. Communication between the two systems happens over a local network connection.

* **`top-side.py` (Windows Client):** Reads joystick input via Pygame, processes it, and sends it over TCP/IP.
* **`bottom-side.py` (Raspberry Pi Server):** Listens for incoming TCP/IP connections, receives joystick data, and controls motors/servos connected to a PCA9685 servo driver board via I2C.

---

## Table of Contents

* [Hardware Requirements](#hardware-requirements)
* [Software Requirements](#software-requirements)
* [Setup Instructions](#setup-instructions)
    * [Windows Client (`top-side.py`) Setup](#windows-client-top-sidepy-setup)
    * [Raspberry Pi Server (`bottom-side.py`) Setup](#raspberry-pi-server-bottom-sidepy-setup)
* [Running the Application](#running-the-application)
* [Troubleshooting](#troubleshooting)

---

## Hardware Requirements

**Windows Client:**
1.  A Windows PC
2.  A USB Joystick compatible with Pygame/Windows

**Raspberry Pi Server:**
1.  Raspberry Pi (3, 4, Zero W/2 W, etc.) with Raspberry Pi OS installed and network connectivity (WiFi or Ethernet).
2.  SD Card for Raspberry Pi OS.
3.  Adafruit PCA9685 16-Channel Servo Driver board.
4.  Motors, Servos, and/or ESCs (Electronic Speed Controllers) as required by your project.
5.  Separate power supply capable of handling the current draw of your motors/servos ( **Do not power motors/servos directly from the Pi** ).
6.  Jumper wires for connecting the PCA9685 to the Raspberry Pi.
7.  Standard Raspberry Pi peripherals (Power Supply, Monitor, Keyboard, Mouse - for initial setup).

---

## Software Requirements

**Windows Client:**
1.  Python 3.x ([Download](https://www.python.org/downloads/))
2.  `pygame` Python library
3.  A Text Editor or IDE (e.g., VS Code [Download](https://code.visualstudio.com/))

**Raspberry Pi Server:**
1.  Raspberry Pi OS ([Download](https://www.raspberrypi.com/software/))
2.  Python 3 (usually pre-installed on Raspberry Pi OS)
3.  `pip` (Python package installer, usually pre-installed)
4.  `adafruit-circuitpython-pca9685` Python library
5.  `adafruit-circuitpython-servokit` Python library
6.  `adafruit-blinka` Python library (CircuitPython compatibility layer)
7.  A Text Editor (e.g., Thonny IDE - pre-installed, or `nano`)
8.  RealVNC Server (for optional remote desktop access)

---

## Setup Instructions

### Windows Client (`top-side.py`) Setup

1.  **Install Python:**
    * Download and install Python 3.x from [python.org](https://www.python.org/downloads/).
    * **Important:** During installation, ensure you check the box "Add Python X.Y to PATH".

2.  **Install Text Editor:**
    * Install a code editor like VS Code ([Download](https://code.visualstudio.com/)).
    * Install the Python extension for VS Code.

3.  **Get the Code:**
    * Create a new file in your text editor.
    * Copy the contents of the client script (the second script in the original request, the one using `pygame`).
    * Save the file as `top-side.py` in a convenient location (e.g., `C:\Projects\JoystickControl`).

4.  **Install Dependencies:**
    * Open Command Prompt (`cmd`) or PowerShell.
    * Install the required Python library:
        ```bash
        pip install pygame
        ```

5.  **Connect Joystick:**
    * Plug your USB joystick into your Windows PC.

6.  **Configure Server IP Address (Placeholder):**
    * Open `top-side.py` in your editor.
    * Locate the line:
        ```python
        s.connect(("192.168.88.250", 5000)) # Change the IP address to the server's IP address
        ```
    * You will replace `"192.168.88.250"` with the actual IP address of your Raspberry Pi later.

### Raspberry Pi Server (`bottom-side.py`) Setup

1.  **Initial Pi Setup & Updates:**
    * Ensure Raspberry Pi OS is installed and the Pi is connected to your network.
    * Open the Terminal.
    * Update your system:
        ```bash
        sudo apt update
        sudo apt full-upgrade -y
        ```

2.  **Enable I2C Interface:**
    * Run `sudo raspi-config`.
    * Navigate to `Interface Options` -> `I2C`.
    * Select `<Yes>` to enable I2C.
    * Finish and reboot if prompted.

3.  **Connect Hardware:**
    * **Power off the Raspberry Pi.**
    * Connect the PCA9685 board to the Pi's GPIO pins:
        * Pi `3.3V` -> PCA9685 `VCC`
        * Pi `SDA` (GPIO 2) -> PCA9685 `SDA`
        * Pi `SCL` (GPIO 3) -> PCA9685 `SCL`
        * Pi `GND` -> PCA9685 `GND`
    * Connect your **separate motor/servo power supply** to the PCA9685 `V+` and `GND` screw terminals.
    * Connect your motors/servos to the PWM pins (0-15) on the PCA9685.
