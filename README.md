# ROV
MATE ROV Ranger Class



# For Setup on Raspberry Pi (bottom-side)
Download bottom-side.py onto raspberry pi
Connect to pi over VNC

Modules That Don't Need Installation (Built-in)

These modules are part of Python's standard library, so you don't need to install them separately using pip. They come included with your Python installation.

socket: Used for low-level network programming.
pickle: Used for serializing and de-serializing Python object structures (saving objects to files/bytes and loading them back).
time: Provides various time-related functions.
Modules That Need Installation (Third-Party)

These modules are not part of the standard library and need to be installed using Python's package installer, pip. It's highly recommended to use Python 3 and its corresponding pip3.

board: This is part of Adafruit's Blinka library, which provides CircuitPython support (hardware APIs) on Linux boards like Raspberry Pi, BeagleBone, etc.
adafruit_pca9685: This is the Adafruit CircuitPython library for controlling the PCA9685 16-Channel 12-bit PWM/Servo Driver. The package name usually follows the format adafruit-circuitpython-<libraryname>.
adafruit_servokit: This is the Adafruit CircuitPython library that provides a high-level interface for controlling multiple servos, often using the PCA9685 driver.
Installation Commands

You'll use pip3 (the package installer for Python 3) to install the third-party modules.

Prerequisites:

Ensure pip3 is installed:
On Debian/Ubuntu-based systems:
Bash

sudo apt update
sudo apt install python3-pip



(Highly Recommended) Use a Virtual Environment: This isolates project dependencies and avoids conflicts with system-wide packages.
Bash

# Create a virtual environment (e.g., named 'myenv')
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Now you can install packages within this environment
# To deactivate later, simply run: deactivate
Installation Command:

Once pip3 is ready (and preferably inside an activated virtual environment), you can install the required Adafruit libraries. pip will automatically handle dependencies, so installing adafruit-circuitpython-servokit might also pull in board and adafruit-circuitpython-pca9685 if they are listed as dependencies. However, it's good practice to list them explicitly if you know you need them directly.

Bash

pip3 install adafruit-circuitpython-servokit adafruit-circuitpython-pca9685 board
This command attempts to install adafruit-circuitpython-servokit.
It also explicitly requests adafruit-circuitpython-pca9685 and board. pip is smart enough to fetch them only once if they are dependencies of each other or already installed.
board relies on Adafruit_Blinka, which pip should install automatically as a dependency.
System Dependencies for Hardware Access:

Libraries like board, adafruit_pca9685, and adafruit_servokit interact with hardware interfaces (like I2C). You might need to:

Enable Hardware Interfaces: On Raspberry Pi, use sudo raspi-config to enable I2C (and SPI if needed). Other boards have different methods.
Install System Libraries: Blinka might require certain system development libraries or tools. Often, python3-smbus or i2c-tools are needed.
On Debian/Ubuntu: sudo apt install python3-smbus i2c-tools
On Fedora/CentOS/RHEL: sudo dnf install python3-smbus-cffi i2c-tools (Package names might vary slightly).
Permissions: Your user might need to be part of a group (like i2c or gpio) to access these hardware interfaces without using sudo.
Example: sudo adduser $USER i2c (You might need to log out and back in for the change to take effect).
