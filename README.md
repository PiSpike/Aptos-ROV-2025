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
    * Copy the contents of the client script (top-side.py).
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
    * Power on the Raspberry Pi.

4.  **Verify I2C Connection (Optional):**
    * In the Terminal, run `sudo i2cdetect -y 1`.
    * You should see `40` (or another address if changed) in the output grid, confirming the Pi sees the PCA9685.

5.  **Get the Code:**
    * Open Thonny IDE or use `nano` (`nano bottom-side.py`).
    * Copy the contents of the server script (the first script in the original request, using `adafruit_pca9685`).
    * Save the file as `bottom-side.py` (e.g., in `/home/pi/`).

6.  **Set Up Virtual Environment (Recommended):**
    * Navigate to the directory where you saved `bottom-side.py`:
        ```bash
        cd /path/to/your/script # e.g., cd /home/pi/
        ```
    * Create the environment:
        ```bash
        python3 -m venv my_env
        ```
    * Activate the environment ( **Do this every time you open a new terminal for this project** ):
        ```bash
        source my_env/bin/activate
        ```
        Your prompt should now start with `(my_env)`.

7.  **Install Dependencies:**
    * Make sure the virtual environment is active (`(my_env)` is in the prompt).
    * Install the required libraries:
        ```bash
        pip install adafruit-circuitpython-pca9685 adafruit-circuitpython-servokit
        ```
        *(Note: `adafruit-blinka` should be installed automatically as a dependency)*

8.  **Find Raspberry Pi IP Address:**
    * In the Terminal, run:
        ```bash
        hostname -I
        ```
    * Note down the IP address displayed (e.g., `192.168.1.XX`).

9.  **Update Client Script:**
    * Go back to your **Windows PC**.
    * Edit `top-side.py`.
    * Replace `"192.168.88.250"` in the `s.connect(...)` line with the **actual IP address of your Raspberry Pi**.
    * Save the file.

10. **Install and Enable VNC (Optional Remote Desktop):**
    * In the Pi's Terminal:
        ```bash
        sudo apt update
        sudo apt install -y realvnc-vnc-server realvnc-vnc-viewer
        sudo raspi-config
        ```
    * Navigate to `Interface Options` -> `VNC`.
    * Select `<Yes>` to enable. Finish and reboot if needed.
    * On Windows, install RealVNC Viewer ([Download](https://www.realvnc.com/en/connect/download/viewer/)) and connect using the Pi's IP address.

---

## Running the Application

**Important:** The server (`bottom-side.py`) must be running *before* you start the client (`top-side.py`).

1.  **Start the Server (on Raspberry Pi):**
    * Open a Terminal on the Pi (directly or via VNC/SSH).
    * Navigate to the script directory (e.g., `cd /home/pi/`).
    * Activate the virtual environment:
        ```bash
        source my_env/bin/activate
        ```
    * Run the server script:
        ```bash
        python bottom-side.py
        ```
    * You should see the message: `Server is now running`.

2.  **Start the Client (on Windows PC):**
    * Ensure your joystick is plugged in.
    * Open Command Prompt or PowerShell.
    * Navigate to the script directory (e.g., `cd C:\Projects\JoystickControl`).
    * Run the client script:
        ```bash
        python top-side.py
        ```
    * The client should connect to the server. You will see joystick input data printed in the client terminal, and this data will be sent to the Pi. The Pi terminal will show the received data, and the connected motors/servos should respond.

3.  **Stopping:**
    * Press `Ctrl + C` in the client terminal (Windows).
    * Press `Ctrl + C` in the server terminal (Raspberry Pi).

---

## Troubleshooting

* **Connection Refused (Windows Client):**
    * Verify the IP address in `top-side.py` is correct and matches the Pi's current IP.
    * Ensure `bottom-side.py` is running on the Pi *before* starting `top-side.py`.
    * Check Windows Firewall isn't blocking the outbound connection from `python.exe`.
    * Make sure both devices are on the same local network.
* **`ModuleNotFoundError` (Pi or Windows):**
    * Pi: Make sure you have activated the virtual environment (`source my_env/bin/activate`) before running `pip install` or `python bottom-side.py`.
    * Install the missing library using `pip install <library_name>`.
* **I2C Errors / `IOError` (Pi Server):**
    * Double-check wiring between Pi and PCA9685 (SDA, SCL, VCC, GND).
    * Confirm I2C is enabled (`sudo raspi-config`).
    * Check device detection (`sudo i2cdetect -y 1`).
* **Motors/Servos Not Moving:**
    * Check the separate power supply for the PCA9685. Is it turned on? Is it adequate?
    * Verify motor/servo connections to the PCA9685 pins match the pin numbers in `bottom-side.py`.
    * Check the Pi's terminal output to see if data is being received correctly.
* **Joystick Not Detected (Windows Client):**
    * Ensure the joystick is plugged in before running `top-side.py`.
    * Check if Windows recognizes the joystick in the Control Panel.
    * Make sure `pygame` is installed (`pip install pygame`).
